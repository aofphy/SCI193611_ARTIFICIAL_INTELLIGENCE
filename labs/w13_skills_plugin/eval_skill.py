#!/usr/bin/env python3
"""วัดว่า description ของ skill ทำให้มันถูกเรียกใช้ถูกจังหวะหรือไม่

ข้อผิดพลาดที่พบบ่อยที่สุดของ skill คือ **เนื้อหาดีแต่ description กว้าง**
ผลคือ skill ไม่เคยถูกเรียก และไม่มีข้อความผิดพลาดใด ๆ ให้เห็น
สคริปต์นี้ทำให้ปัญหานั้นวัดได้

ใช้:
    python eval_skill.py --self-check        # ทดสอบตรรกะ ไม่ต้องมีโมเดล
    python eval_skill.py                     # เลือกโมเดลให้เองตาม labs/llm.py
    python eval_skill.py --provider openrouter --model z-ai/glm-5.2:free
    python eval_skill.py --provider local --model qwen3:8b

โมเดลไหนก็ได้ที่ labs/llm.py รองรับ รวมถึงรุ่น :free ของ OpenRouter
ที่เรียกได้โดยไม่เสียเงิน ดูรายชื่อด้วย  python ../llm.py --free
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent))          # ให้หา labs/llm.py เจอ
import llm as api                             # noqa: E402
SKILL = HERE / "plugin" / "skills" / "lab-report" / "SKILL.md"

# คำขอทดสอบ: (ข้อความของผู้ใช้, ควรเรียก skill นี้หรือไม่)
CASES = [
    ("ช่วยตรวจรายงานปฏิบัติการสัปดาห์ที่ 10 ให้หน่อย", True),
    ("รายงานนี้ได้กี่คะแนนตามเกณฑ์", True),
    ("ตรวจให้หน่อยว่ารายงานผมขาดอะไรก่อนส่ง", True),
    ("ให้คะแนน report.md ตาม rubric", True),
    ("รายงานแล็บผมพร้อมส่งหรือยัง", True),
    ("ช่วยดีบักโค้ด PyTorch ให้หน่อย", False),
    ("อธิบายว่า attention ทำงานอย่างไร", False),
    ("รีวิวโค้ดใน agent.py ให้หน่อย", False),
    ("ช่วยรีวิวบทความวิจัยเรื่อง RAG ที่ผมกำลังเขียน", False),
    ("สัปดาห์ที่ 12 เรียนอะไร", False),
]

JUDGE = """คุณเป็นตัวเลือกเครื่องมือของผู้ช่วย AI
มี skill หนึ่งตัวที่ใช้ได้ตามคำอธิบายนี้

<skill_description>
{desc}
</skill_description>

ผู้ใช้พูดว่า: "{request}"

skill นี้ควรถูกเรียกใช้กับคำขอนี้หรือไม่
ตอบเพียงคำเดียวว่า YES หรือ NO ห้ามอธิบาย"""


def read_description(path=SKILL):
    """ดึงค่า description จาก YAML frontmatter ของ SKILL.md"""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        raise ValueError(f"{path} ไม่มี YAML frontmatter")
    body = m.group(1)
    d = re.search(r"^description:\s*(.*(?:\n[ \t]+.*)*)", body, re.M)
    if not d:
        raise ValueError(f"{path} ไม่มีฟิลด์ description")
    return " ".join(line.strip() for line in d.group(1).splitlines()).strip()


def api_judge(provider=None, model=None):
    """คืนฟังก์ชัน judge(prompt) -> str ที่ยิงผู้ให้บริการซึ่ง llm.py เลือกให้"""
    call = api.text_llm(provider, model, temperature=0)
    return lambda prompt: call(prompt)[0]


def keyword_judge(prompt):
    """ตัวตัดสินจำลองสำหรับ --self-check: เทียบคำสำคัญอย่างหยาบ"""
    req = re.search(r'ผู้ใช้พูดว่า: "(.*)"', prompt).group(1)
    hit = any(k in req for k in ("รายงาน", "rubric", "เกณฑ์", "report.md"))
    miss = any(k in req for k in ("โค้ด", "บทความ", "attention", "agent.py"))
    return "YES" if hit and not miss else "NO"


def evaluate(judge, desc, cases=CASES):
    rows, tp = [], 0
    for request, want in cases:
        raw = judge(JUDGE.format(desc=desc, request=request))
        got = "YES" in raw.upper().split("</THINK>")[-1][:40]
        rows.append((request, want, got))
        tp += got == want
    return tp / len(cases), rows


def report(acc, rows):
    print(f"{'ควรเรียก':9s} {'เรียกจริง':10s} คำขอ")
    for request, want, got in rows:
        mark = " " if want == got else "  <-- ผิด"
        print(f"{str(want):9s} {str(got):10s} {request[:46]}{mark}")
    fp = sum(got and not want for _, want, got in rows)
    fn = sum(want and not got for _, want, got in rows)
    print(f"\naccuracy = {acc:.2f}   เรียกเกิน (false positive) = {fp}   "
          f"ไม่เรียกทั้งที่ควร (false negative) = {fn}")
    if fn:
        print("-> description แคบหรือกำกวมเกินไป เพิ่มคำที่ผู้ใช้มักพูดจริง")
    if fp:
        print("-> description กว้างเกินไป เพิ่มประโยค 'ห้ามใช้กับ ...'")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=list(api.PROVIDERS))
    ap.add_argument("--model")
    ap.add_argument("--self-check", action="store_true")
    args = ap.parse_args()

    desc = read_description()
    print(f"description ({len(desc)} อักขระ):\n  {desc}\n")

    if args.self_check:
        acc, rows = evaluate(keyword_judge, desc)
        report(acc, rows)
        assert acc >= 0.8, f"ตัวตัดสินจำลองควรได้อย่างน้อย 0.8 แต่ได้ {acc}"
        print("\nOK: eval_skill self-check ผ่าน")
        return

    print(api.describe(api.resolve(args.provider, args.model)))
    try:
        acc, rows = evaluate(api_judge(args.provider, args.model), desc)
    except Exception as e:
        print(f"เรียกโมเดลไม่สำเร็จ ({type(e).__name__}: {e})")
        print("ทางเลือก: ตั้ง OPENROUTER_API_KEY แล้วใช้โมเดล :free, "
              "ติดตั้ง Ollama, หรือใช้ --self-check เพื่อทดสอบเฉพาะตรรกะ")
        return 1
    report(acc, rows)


if __name__ == "__main__":
    sys.exit(main() or 0)

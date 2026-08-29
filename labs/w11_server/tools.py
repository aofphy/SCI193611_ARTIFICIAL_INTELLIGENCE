"""ตรรกะล้วนของเซิร์ฟเวอร์ MCP ประจำรายวิชา

ไฟล์นี้ **ไม่ import แพ็กเกจ mcp** โดยตั้งใจ เพื่อให้ทดสอบฟังก์ชันทุกตัวได้
ด้วย Python ธรรมดา ส่วน `server.py` เป็นแค่ตัวห่อบาง ๆ ที่นำฟังก์ชันเหล่านี้
ไปลงทะเบียนกับ MCP

การแยกแบบนี้เป็นแนวปฏิบัติที่ควรทำกับเซิร์ฟเวอร์ MCP ทุกตัว:
แกนที่ทดสอบได้ + ชั้นโปรโตคอลที่บาง
"""
from __future__ import annotations

import math
import pathlib
import re
from collections import Counter

# ---------------------------------------------------------------- คลังเอกสาร

def repo_root() -> pathlib.Path:
    """หารากของรีโพรายวิชาจากตำแหน่งของไฟล์นี้"""
    for cand in pathlib.Path(__file__).resolve().parents:
        if (cand / "README.md").exists() and (cand / "slide").is_dir():
            return cand
    raise FileNotFoundError("ไม่พบรากของรีโพ")


THAI = re.compile(r"[\u0E00-\u0E7F]+")
LATIN = re.compile(r"[a-zA-Z0-9_.]+")


def tokenize(text: str, n: int = 3) -> list[str]:
    """ตัวแบ่งโทเคนแบบผสม: คำละตินตามช่องว่าง, ภาษาไทยเป็น character n-gram"""
    toks = [w.lower() for w in LATIN.findall(text)]
    for run in THAI.findall(text):
        toks += [run[i:i + n] for i in range(max(1, len(run) - n + 1))]
    return toks


def _chunks() -> list[dict]:
    text = (repo_root() / "README.md").read_text(encoding="utf-8")
    out, heading, buf, in_code = [], "(intro)", [], False

    def flush():
        body = "\n".join(buf).strip()
        if len(body) > 40:
            out.append({"heading": heading, "text": body[:2000]})

    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
        if line.startswith("#") and not in_code:
            flush()
            buf, heading = [], line.lstrip("#").strip()
        else:
            buf.append(line)
    flush()
    return out


_CACHE: list[dict] | None = None


def _corpus() -> list[dict]:
    global _CACHE
    if _CACHE is None:
        _CACHE = _chunks()
    return _CACHE


# ---------------------------------------------------------------- เครื่องมือ

def search_course(query: str, max_results: int = 3) -> str:
    """ค้นเนื้อหาประมวลรายวิชา SCI19 3611 (ตาราง 15 สัปดาห์, เกณฑ์คะแนน,
    โครงงาน, การเตรียมเครื่องมือ)

    ใช้เมื่อผู้ใช้ถามถึงรายละเอียดของรายวิชานี้
    ห้ามใช้กับคำถามทั่วไปที่ไม่เกี่ยวกับรายวิชา

    Args:
        query: คำค้น ควรใช้คำภาษาอังกฤษที่ปรากฏในเอกสาร เช่น
            'Midterm Examination', 'Grading', 'Prerequisites'
        max_results: จำนวนผลลัพธ์ 1 ถึง 5

    ข้อจำกัดที่รู้อยู่แล้ว: นี่คือการค้นด้วย **คำหลัก** ล้วน ๆ
    README ของรายวิชาเขียนเป็นภาษาอังกฤษเกือบทั้งหมด คำค้นภาษาไทยจึงมัก
    ไม่ตรงกับอะไรเลยและได้ผลลัพธ์ที่ไม่เกี่ยวข้อง การค้นข้ามภาษาต้องใช้
    embedding เชิงความหมาย ซึ่งเป็นเนื้อหาของสัปดาห์ที่ 10 (ดู labs/w10_rag.ipynb)
    """
    if not query.strip():
        return "query ว่างเปล่า ให้ระบุคำค้นอย่างน้อย 1 คำ"
    max_results = max(1, min(5, int(max_results)))

    docs = _corpus()
    tf = [Counter(tokenize(d["heading"] + " " + d["text"])) for d in docs]
    df = Counter(t for c in tf for t in c)
    q = tokenize(query)

    scored = []
    for d, c in zip(docs, tf):
        s = sum(math.log(1 + len(docs) / df[t]) * c[t] for t in q if t in c)
        scored.append((s, d))
    scored.sort(key=lambda x: -x[0])

    if scored[0][0] == 0:
        return f"ไม่พบเนื้อหาที่ตรงกับ {query!r} ในประมวลรายวิชา"
    return "\n\n".join(
        f"## {d['heading']}\n{d['text'][:600]}"
        for s, d in scored[:max_results] if s > 0)


ENERGY_TO_EV = {
    "J": 6.241509074e18,
    "kJ/mol": 0.01036410,
    "kcal/mol": 0.04336410,
    "Ry": 13.605693123,
    "Ha": 27.211386246,
    "cm-1": 1.239841984e-4,
    "K": 8.617333262e-5,
    "eV": 1.0,
}


def convert_energy(value: float, unit: str) -> str:
    """แปลงค่าพลังงานจากหน่วยที่กำหนดเป็นอิเล็กตรอนโวลต์ (eV)

    ใช้เมื่อผู้ใช้ต้องการเทียบพลังงานข้ามหน่วย เช่น ผลจากการคำนวณ DFT
    หรือค่าจากสเปกโทรสโกปี

    Args:
        value: ค่าตัวเลขที่ต้องการแปลง
        unit: หน่วยต้นทาง หนึ่งใน J, kJ/mol, kcal/mol, Ry, Ha, cm-1, K, eV
    """
    if unit not in ENERGY_TO_EV:
        return (f"ไม่รองรับหน่วย {unit!r} "
                f"หน่วยที่รองรับคือ {', '.join(ENERGY_TO_EV)}")
    try:
        v = float(value)
    except (TypeError, ValueError):
        return f"value ต้องเป็นตัวเลข แต่ได้ {value!r}"
    return f"{v} {unit} = {v * ENERGY_TO_EV[unit]:.6g} eV"


WEEKS = {
    1: "Introduction to AI", 2: "Intelligent Agents",
    3: "Problem Solving by Search", 4: "Adversarial Search",
    5: "Logic & Automated Planning", 6: "Probabilistic Reasoning",
    7: "Reasoning Over Time (HMM)", 8: "LLM ทำงานอย่างไร",
    9: "Prompting และ Context Engineering", 10: "RAG และฐานข้อมูลเวกเตอร์",
    11: "Model Context Protocol (MCP)", 12: "เอเจนต์ AI และการใช้เครื่องมือ",
    13: "Harness, AI Skills และ Plugins",
    14: "เวิร์กโฟลว์อัตโนมัติ จริยธรรม และความปลอดภัย",
    15: "นำเสนอโครงงานปลายภาค",
}


def get_week_topic(week: int) -> str:
    """คืนหัวข้อบรรยายของสัปดาห์ที่ระบุ

    ใช้เมื่อผู้ใช้ถามว่า "สัปดาห์ที่ N เรียนอะไร" หรือถามลำดับของเนื้อหา

    Args:
        week: หมายเลขสัปดาห์ 1 ถึง 15
    """
    try:
        w = int(week)
    except (TypeError, ValueError):
        return f"week ต้องเป็นจำนวนเต็ม แต่ได้ {week!r}"
    if w not in WEEKS:
        return f"สัปดาห์ต้องอยู่ระหว่าง 1 ถึง 15 แต่ได้ {w}"
    return f"สัปดาห์ที่ {w}: {WEEKS[w]}"


# ---------------------------------------------------------------- resource

def syllabus() -> str:
    """ประมวลรายวิชาฉบับเต็ม (README.md)"""
    return (repo_root() / "README.md").read_text(encoding="utf-8")


# ---------------------------------------------------------------- prompt

def review_report(text: str) -> str:
    """เทมเพลตตรวจรายงานปฏิบัติการของรายวิชา"""
    return f"""ตรวจรายงานปฏิบัติการต่อไปนี้ตามเกณฑ์ 4 ข้อ ให้คะแนนข้อละ 0 ถึง 5

1. ระเบียบวิธีถูกต้องและทำซ้ำได้
2. ผลลัพธ์มีหลักฐานรองรับ ไม่ใช่การกล่าวอ้างลอย ๆ
3. มีการอ้างอิงแหล่งข้อมูลครบถ้วน
4. ข้อสรุปสอดคล้องกับผลที่ได้จริง

สรุปท้ายด้วยข้อเสนอแนะที่ทำได้จริง 3 ข้อ

<report>
{text}
</report>"""


TOOLS = [search_course, convert_energy, get_week_topic]


if __name__ == "__main__":
    # self-check: รัน `python tools.py` เพื่อตรวจว่าเครื่องมือทุกตัวทำงาน
    assert "สัปดาห์ที่ 11" in get_week_topic(11)
    assert "1 ถึง 15" in get_week_topic(99)
    assert "ต้องเป็นจำนวนเต็ม" in get_week_topic("สิบเอ็ด")

    assert convert_energy(1, "Ha").endswith("27.2114 eV")
    assert "ไม่รองรับหน่วย" in convert_energy(1, "furlong")
    assert "ต้องเป็นตัวเลข" in convert_energy("มาก", "eV")

    assert "Schedule" in search_course("Midterm Examination")
    assert "Assessment" in search_course("Grading Assessment")
    assert "Prerequisites" in search_course("Prerequisites Setup")
    assert "ไม่พบเนื้อหา" in search_course("zzzqqqxxx")
    assert "ว่างเปล่า" in search_course("  ")
    assert len(search_course("week", 1).split("## ")) == 2, "max_results ต้องมีผล"

    assert "SCI19 3611" in syllabus()
    assert "<report>" in review_report("ทดสอบ")
    print("OK: เครื่องมือทั้งหมดผ่าน self-check")

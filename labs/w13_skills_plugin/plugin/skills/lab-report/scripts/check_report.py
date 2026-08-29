#!/usr/bin/env python3
"""ตรวจรายงานปฏิบัติการเชิงโครงสร้าง

สคริปต์นี้คือ **ระดับที่ 3** ของ skill: งานที่ตรวจด้วยกฎได้ ให้โปรแกรมทำ
อย่าให้โมเดลนับหัวข้อหรือนับการอ้างอิงเอง เพราะมันนับพลาดและเปลืองโทเคน

ใช้:  python check_report.py report.md
"""
import re
import sys
import pathlib

REQUIRED = ["ระเบียบวิธี", "ผล", "อภิปราย", "สรุป", "อ้างอิง"]
AI_MARKERS = ["การใช้ ai", "ai use", "แถลงการณ์การใช้", "ใช้เครื่องมือ ai"]
URL = re.compile(r"https?://\S+")
DOI = re.compile(r"10\.\d{4,9}/\S+")


def check(text):
    """คืนรายการ (ผ่านหรือไม่, ข้อความ) สำหรับทุกข้อที่ตรวจด้วยโปรแกรมได้"""
    low = text.lower()
    words = len(text.split())
    refs = len(set(URL.findall(text)) | set(DOI.findall(text)))
    missing = [h for h in REQUIRED if h not in text]

    return [
        (not missing, f"หัวข้อที่ต้องมี: ขาด {missing}" if missing else "หัวข้อครบทุกส่วน"),
        (words >= 300, f"ความยาว {words} คำ (ต้องอย่างน้อย 300)"),
        (refs >= 2, f"พบการอ้างอิงที่ตรวจสอบได้ {refs} รายการ (ต้องอย่างน้อย 2)"),
        (any(m in low for m in AI_MARKERS), "แถลงการณ์การใช้ AI"),
        ("```" in text or "|" in text,
         "มีตาราง กราฟ หรือบล็อกโค้ดแสดงผลจริง"),
    ]


def main(path):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    results = check(text)
    for ok, msg in results:
        print(f"[{'ผ่าน' if ok else 'ตก '}] {msg}")
    failed = sum(not ok for ok, _ in results)
    print(f"\nตรวจอัตโนมัติ: ผ่าน {len(results) - failed}/{len(results)} ข้อ")
    print("ส่วนที่เหลือ (คุณภาพของเนื้อหา) ให้ตัดสินตาม reference/rubric.md")
    return 1 if failed else 0


def _self_check():
    good = ("# ระเบียบวิธี\n" + "คำ " * 320 + "\n# ผล\n| a | b |\n"
            "# อภิปราย\n# สรุป\n# อ้างอิง\nhttps://a.example https://b.example\n"
            "## แถลงการณ์การใช้ AI\nใช้ Claude ช่วยตรวจไวยากรณ์")
    assert all(ok for ok, _ in check(good)), check(good)
    bad = "# สรุป\nสั้นมาก"
    assert not any(ok for ok, _ in check(bad)), check(bad)
    print("OK: check_report self-check ผ่าน")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        _self_check()
    else:
        sys.exit(main(sys.argv[1]))

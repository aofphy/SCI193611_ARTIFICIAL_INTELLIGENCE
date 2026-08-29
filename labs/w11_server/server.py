"""เซิร์ฟเวอร์ MCP ประจำรายวิชา SCI19 3611

ชั้นโปรโตคอลที่บางที่สุดเท่าที่ทำได้: ตรรกะทั้งหมดอยู่ใน `tools.py`
ไฟล์นี้ทำแค่ลงทะเบียนฟังก์ชันเหล่านั้นเข้ากับ MCP

ติดตั้ง:   pip install "mcp[cli]"
รัน:       python server.py
ตรวจสอบ:  npx @modelcontextprotocol/inspector python server.py
"""
from mcp.server.fastmcp import FastMCP

import tools

mcp = FastMCP("course-tools")

# FastMCP สร้าง JSON Schema จาก type hint และ docstring ของแต่ละฟังก์ชันให้เอง
# นี่คือเหตุผลที่ docstring ใน tools.py เขียนละเอียดพร้อมประโยค "ใช้เมื่อ ..."
for fn in tools.TOOLS:
    mcp.tool()(fn)


@mcp.resource("course://syllabus")
def syllabus() -> str:
    """ประมวลรายวิชา SCI19 3611 ฉบับเต็ม"""
    return tools.syllabus()


@mcp.resource("course://week/{week}")
def week_topic(week: str) -> str:
    """หัวข้อบรรยายของสัปดาห์ที่ระบุ"""
    return tools.get_week_topic(week)


@mcp.prompt()
def review_report(text: str) -> str:
    """เทมเพลตตรวจรายงานปฏิบัติการ"""
    return tools.review_report(text)


if __name__ == "__main__":
    mcp.run()          # ค่าเริ่มต้นคือการขนส่งแบบ stdio

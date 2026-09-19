"""เซิร์ฟเวอร์ MCP ค้นเว็บ (แล็บสัปดาห์ที่ 11.2)

ชั้นโปรโตคอลที่บางที่สุดเท่าที่ทำได้ ตรรกะทั้งหมดอยู่ใน `search_tools.py`
ตัวเซิร์ฟเวอร์อ่าน type hint กับ docstring ของแต่ละฟังก์ชันแล้วสร้าง JSON Schema ให้เอง

ติดตั้ง:   pip install "mcp[cli]"
รัน:       python server.py
ตรวจสอบ:  npx @modelcontextprotocol/inspector python server.py
ต่อโมเดล:  python agent.py "คำถามของคุณ"
"""
# แพ็กเกจ mcp เปลี่ยนชื่อคลาสนี้ตอนขึ้นเวอร์ชัน 2 หน้าตาการใช้งานเหมือนเดิมทุกอย่าง
# รองรับทั้งสองเวอร์ชันไว้ เพราะแต่ละเครื่องติดตั้งมาไม่เท่ากัน
try:
    from mcp.server.mcpserver import MCPServer as Server      # mcp 2.x
except ImportError:                                            # pragma: no cover
    from mcp.server.fastmcp import FastMCP as Server          # mcp 1.x

import search_tools

mcp = Server("web-search")

for fn in search_tools.TOOLS:
    mcp.tool()(fn)


if __name__ == "__main__":
    mcp.run()          # ค่าเริ่มต้นคือการขนส่งแบบ stdio

# Labs: Modern AI Track

ปฏิบัติการประจำสัปดาห์ของหลักสูตรปรับปรุง พ.ศ. 2569
สัปดาห์ที่ 8 ถึง 14 เป็นแทร็ก **การใช้ AI ในยุคปัจจุบัน** (LLM, RAG, MCP, Agent, Harness, Workflow)

**หลักการออกแบบแล็บชุดนี้**

- **ไม่ผูกกับผู้ให้บริการรายใด** โค้ดใช้ได้กับ Claude, Gemini, GPT, Qwen, GLM, Kimi และโมเดลเปิดน้ำหนักบนเครื่อง
- **รันได้โดยไม่ต้องมี API key** ทุกแล็บมีเส้นทางออฟไลน์ (โมเดลจำลอง, Ollama บนเครื่อง, หรือ fallback ที่ไม่ต้องใช้โมเดล)
  แล้วสลับไปโมเดลจริงได้ด้วยการตั้งตัวแปรสภาพแวดล้อม ไม่ต้องแก้โค้ด
- **มีทางเลือกที่ไม่เสียเงิน** ถ้าเครื่องแรมไม่พอจะรันโมเดลเอง ใช้รุ่น `:free`
  ของ [OpenRouter](https://openrouter.ai/) ได้ ดู [การตั้งค่าที่ใช้ร่วมกัน](#การตั้งค่าที่ใช้ร่วมกัน)
- **ทุกแล็บมี self-check** ที่ล้มเหลวถ้าตรรกะพัง ไม่ใช่แค่ตัวอย่างที่พิมพ์ผลออกมาสวย ๆ

| ที่อยู่ | สัปดาห์ | หัวข้อ | รันทันที | Colab |
| --- | --- | --- | --- | --- |
| [`llm.py`](./llm.py) | 8 ถึง 14 | ไคลเอนต์กลางที่ทุกแล็บใช้ร่วมกัน (รวมทางเลือกโมเดลฟรี) | ใช่ | ไม่มี |
| [`w05_logic_planning.ipynb`](./w05_logic_planning.ipynb) | 5 | Logic & Automated Planning (DPLL + STRIPS/BFS) | ใช่ | [open](https://colab.research.google.com/github/aofphy/SCI193611_ARTIFICIAL_INTELLIGENCE/blob/main/labs/w05_logic_planning.ipynb) |
| [`w08_llm_internals.ipynb`](./w08_llm_internals.ipynb) | 8 | Tokenizer, attention จากศูนย์, การสุ่มโทเคน | ใช่ (NumPy) | [open](https://colab.research.google.com/github/aofphy/SCI193611_ARTIFICIAL_INTELLIGENCE/blob/main/labs/w08_llm_internals.ipynb) |
| [`w09_prompting_context.ipynb`](./w09_prompting_context.ipynb) | 9 | Client หลายผู้ให้บริการ, ชุดประเมิน, การจัดการบริบท | ใช่ (โมเดลจำลอง) | [open](https://colab.research.google.com/github/aofphy/SCI193611_ARTIFICIAL_INTELLIGENCE/blob/main/labs/w09_prompting_context.ipynb) |
| [`w10_rag.ipynb`](./w10_rag.ipynb) | 10 | RAG บนเอกสารจริงของรายวิชา + BM25 + RRF + Recall@k | ใช่ | [open](https://colab.research.google.com/github/aofphy/SCI193611_ARTIFICIAL_INTELLIGENCE/blob/main/labs/w10_rag.ipynb) |
| [`w11_mcp_server.ipynb`](./w11_mcp_server.ipynb) + [`w11_server/`](./w11_server) | 11 | เซิร์ฟเวอร์ MCP จริง + JSON-RPC handshake ด้วยมือ | ใช่ (stdlib) | [open](https://colab.research.google.com/github/aofphy/SCI193611_ARTIFICIAL_INTELLIGENCE/blob/main/labs/w11_mcp_server.ipynb) |
| [`w12_agent.ipynb`](./w12_agent.ipynb) | 12 | ลูปเอเจนต์จากศูนย์ + ชั้นควบคุม + ชุดทดสอบ | ใช่ (โมเดลจำลอง) | [open](https://colab.research.google.com/github/aofphy/SCI193611_ARTIFICIAL_INTELLIGENCE/blob/main/labs/w12_agent.ipynb) |
| [`w13_skills_plugin/`](./w13_skills_plugin) | 13 | Skill + plugin + hook + การวัดว่า description ใช้ได้จริง | ใช่ | ไม่มี |
| [`w14_workflow_ethics/`](./w14_workflow_ethics) | 14 | เวิร์กโฟลว์อัตโนมัติ + threat model + แถลงการณ์การใช้ AI | ใช่ | ไม่มี |

## ตรวจว่าแล็บทั้งหมดยังทำงาน

```bash
python labs/w11_server/tools.py
python labs/w13_skills_plugin/plugin/skills/lab-report/scripts/check_report.py
python labs/w13_skills_plugin/plugin/hooks/block_secrets.py --self-check
python labs/w13_skills_plugin/eval_skill.py --self-check
python labs/w14_workflow_ethics/workflow.py --self-check
python labs/llm.py --self-check
```

## การตั้งค่าที่ใช้ร่วมกัน

แล็บสัปดาห์ที่ 8 ถึง 14 คุยกับโมเดลผ่านไฟล์เดียวคือ [`llm.py`](./llm.py)
(ใช้ stdlib ล้วน ไม่ต้องติดตั้งอะไร) มันเลือกผู้ให้บริการให้เองตามลำดับ
อาร์กิวเมนต์ที่ส่งเข้าไป, `LLM_PROVIDER`, key ตัวแรกที่เจอในสภาพแวดล้อม,
แล้วค่อยตกมาที่ Ollama บนเครื่อง

```bash
python labs/llm.py                  # ตอนนี้จะต่อไปที่ไหน ด้วยโมเดลอะไร
python labs/llm.py --free           # โมเดลฟรีบน OpenRouter ที่มีอยู่ตอนนี้
python labs/llm.py --free --tools   # เฉพาะตัวที่เรียกเครื่องมือได้ (สัปดาห์ 12)
python labs/llm.py --ask "สวัสดี"    # ยิงจริงหนึ่งครั้ง
python labs/llm.py --self-check     # ทดสอบตรรกะการเลือก ไม่ต่อเน็ต
```

เลือกทางใดทางหนึ่งจากสามทางนี้ ทำแล็บได้ครบเหมือนกัน

**1. โมเดลจำลองในสมุดบันทึก** ไม่ต้องตั้งค่าใด ๆ ทุกแล็บมีเส้นทางนี้เสมอ
ใช้ทำความเข้าใจตรรกะและวัดผลได้ครบ ยกเว้นคุณภาพคำตอบของโมเดลจริง

**2. โมเดลเปิดน้ำหนักบนเครื่องตัวเอง** ไม่มีค่าใช้จ่าย ข้อมูลไม่ออกจากเครื่อง
เหมาะกับข้อมูลที่เผยแพร่ไม่ได้ ต้องมีแรมพอสมควร

```bash
# ติดตั้งจาก https://ollama.com
ollama pull qwen3:8b
export LLM_PROVIDER=local
```

**3. API ฟรีจาก OpenRouter** เหมาะกับเครื่องที่แรมไม่พอจะรันโมเดลเอง
สมัครที่ [openrouter.ai](https://openrouter.ai/) แล้วสร้าง key

```bash
export OPENROUTER_API_KEY=...
export LLM_MODEL=z-ai/glm-5.2:free   # ตรึงโมเดล ดูรายชื่อด้วย --free
```

รุ่นที่ลงท้ายด้วย `:free` ไม่คิดเงิน แลกกับเพดานจำนวนคำขอต่อนาทีและต่อวัน
ซึ่งขึ้นกับว่าเคยเติมเครดิตไว้เท่าไร (ตัวเลขปัจจุบันดูที่
[เอกสาร limits](https://openrouter.ai/docs/api-reference/limits)
และของ key ตัวเองดูที่ `GET https://openrouter.ai/api/v1/key`)
เมื่อชนเพดาน `llm.py` จะรอแล้วลองใหม่ให้เองสามครั้ง

ข้อควรระวังของรุ่นฟรี สามข้อ

1. **ตรึงชื่อโมเดลเสมอเมื่อต้องเทียบผล** ถ้าไม่ตั้ง `LLM_MODEL` จะได้
   `openrouter/free` ซึ่งสุ่มโมเดลใหม่ทุกคำขอ สะดวกตอนเริ่ม แต่บางครั้ง
   สุ่มได้โมเดลเฉพาะทางที่ตอบไม่ตรงงาน และเทียบผลข้ามคำขอไม่ได้เลย
2. **ห้ามส่งข้อมูลส่วนบุคคลหรือข้อมูลที่ยังไม่เผยแพร่** OpenRouter มีสวิตช์
   แยกสำหรับรุ่นฟรีว่าจะยอมให้ส่งต่อไปยังผู้ให้บริการที่นำข้อมูลไปฝึกโมเดลหรือไม่
   ตรวจค่านี้ในหน้า privacy settings ของบัญชีตัวเองก่อนใช้งาน
   (โยงกับเนื้อหาสัปดาห์ที่ 14 โดยตรง)
3. **รายชื่อโมเดลฟรีเปลี่ยนบ่อย** ถ้าเจอ HTTP 404 ให้รัน `--free` ดูรายชื่อใหม่

**คีย์ของผู้ให้บริการอื่น** ตั้งเป็นตัวแปรสภาพแวดล้อม **ห้าม commit ขึ้น git เด็ดขาด**

```bash
export DASHSCOPE_API_KEY=...   # Qwen
export ZHIPU_API_KEY=...       # GLM
export MOONSHOT_API_KEY=...    # Kimi
export OPENAI_API_KEY=...      # GPT
export GEMINI_API_KEY=...      # Gemini
export ANTHROPIC_API_KEY=...   # Claude
```

คัดลอก [`.env.example`](./.env.example) ไปเป็น `.env` ของตัวเองได้
(`.env` อยู่ใน `.gitignore` แล้ว)

**ไลบรารีที่เป็นทางเลือก** (แล็บทำงานได้โดยไม่มีก็ได้ แต่จะดีขึ้นถ้ามี)

```bash
pip install transformers           # tokenizer จริง (สัปดาห์ 8)
pip install sentence-transformers  # embedding จริง (สัปดาห์ 10)
pip install "mcp[cli]"             # เซิร์ฟเวอร์ MCP จริง (สัปดาห์ 11)
```

## สื่อเสริม (นอกแกนหลัก 15 สัปดาห์)

[`legacy/`](./legacy) เก็บโน้ตบุ๊กจากหลักสูตรฉบับก่อน ใช้ประกอบได้ตามความเหมาะสม

| ไฟล์ | หัวข้อ |
| --- | --- |
| [`legacy/transformer_numpy.ipynb`](./legacy/transformer_numpy.ipynb) | Multi-head attention ฉบับเต็มด้วย NumPy (ต่อยอดจากสัปดาห์ที่ 8) |
| [`legacy/llm_finetune_lora.ipynb`](./legacy/llm_finetune_lora.ipynb) | Fine-tuning ด้วย LoRA (ต้องใช้ GPU) |
| [`legacy/rag_agent_tfidf.ipynb`](./legacy/rag_agent_tfidf.ipynb) | RAG + เอเจนต์ฉบับย่อ (แทนที่ด้วยสัปดาห์ที่ 10 และ 12) |
| [`legacy/generative_ai_diffusion.ipynb`](./legacy/generative_ai_diffusion.ipynb) | Diffusion และ generative AI (ต้องใช้ GPU) |

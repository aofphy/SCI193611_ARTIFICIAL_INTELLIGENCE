#!/usr/bin/env python3
"""ไคลเอนต์ LLM กลางสำหรับแล็บสัปดาห์ที่ 8 ถึง 14

ผู้ให้บริการเกือบทุกรายเปิด endpoint แบบเข้ากันได้กับ OpenAI
(`POST {base_url}/chat/completions`) จึงย้ายโมเดลได้โดยแก้แค่ base_url
กับชื่อโมเดล ไม่ต้องแก้โค้ดแล็บแม้แต่บรรทัดเดียว

ไฟล์นี้ใช้ urllib จาก stdlib ล้วน ไม่ต้อง pip install อะไรเลย

**ทางเลือกฟรี** สมัครที่ openrouter.ai แล้วเอา key ใส่ OPENROUTER_API_KEY
โมเดลที่ลงท้ายด้วย `:free` เรียกได้โดยไม่เสียเงิน แลกกับเพดานจำนวนคำขอ
ต่อนาทีและต่อวัน (ตัวเลขปัจจุบันดูที่ openrouter.ai/docs/api-reference/limits
และเช็คของ key ตัวเองได้ที่ GET https://openrouter.ai/api/v1/key)

ถ้าไม่ตั้ง LLM_MODEL จะได้ `openrouter/free` ซึ่งสุ่มโมเดลใหม่ทุกคำขอ
สะดวกตอนเริ่ม แต่บางครั้งสุ่มได้โมเดลเฉพาะทางที่ตอบไม่ตรงงาน
งานที่ต้องเทียบผลจึงควรตรึงชื่อโมเดลไว้ตัวเดียวตลอด

การเลือกผู้ให้บริการ ไล่ตามลำดับนี้
    1. อาร์กิวเมนต์ provider="..."
    2. ตัวแปรสภาพแวดล้อม LLM_PROVIDER
    3. ผู้ให้บริการรายแรกใน PROVIDERS ที่มี API key อยู่ในสภาพแวดล้อม
    4. ollama บนเครื่องตัวเอง (ไม่ต้องมี key)

ใช้:
    python llm.py                    # ตอนนี้จะต่อไปที่ไหน ด้วยโมเดลอะไร
    python llm.py --free             # โมเดลฟรีบน OpenRouter ที่มีอยู่ตอนนี้
    python llm.py --free --tools     # เฉพาะตัวที่เรียกเครื่องมือได้ (สัปดาห์ 12)
    python llm.py --ask "สวัสดี"      # ยิงจริงหนึ่งครั้ง
    python llm.py --self-check       # ทดสอบตรรกะการเลือก ไม่ต่อเน็ต
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import NamedTuple

# ชื่อ: (base_url, ตัวแปรสภาพแวดล้อมที่เก็บ key, โมเดลตั้งต้น)
# ลำดับในนี้คือลำดับที่ใช้เดา ถ้าไม่ได้ระบุผู้ให้บริการมา
PROVIDERS = {
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY",
                   "openrouter/free"),
    "gpt":    ("https://api.openai.com/v1", "OPENAI_API_KEY", "gpt-4o-mini"),
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai/",
               "GEMINI_API_KEY", "gemini-2.0-flash"),
    "qwen":   ("https://dashscope.aliyuncs.com/compatible-mode/v1",
               "DASHSCOPE_API_KEY", "qwen-plus"),
    "glm":    ("https://open.bigmodel.cn/api/paas/v4", "ZHIPU_API_KEY", "glm-4-plus"),
    "kimi":   ("https://api.moonshot.cn/v1", "MOONSHOT_API_KEY", "moonshot-v1-8k"),
    "local":  ("http://localhost:11434/v1", "OLLAMA_API_KEY", "qwen3:8b"),
}

MODELS_URL = "https://openrouter.ai/api/v1/models"

# ราคาสมมติต่อโทเคน โมเดลฟรีและโมเดลบนเครื่องไม่มีค่าใช้จ่ายจริง
# แต่ยังคิดราคานี้ไว้ เพื่อให้กลไกงบประมาณของสัปดาห์ที่ 14 ได้ทำงานจริง
TOKEN_PROXY = 2e-6

HINTS = {
    401: "API key ไม่ถูกต้องหรือยังไม่ได้ตั้งค่า",
    402: "เครดิตไม่พอ หรือยอดคงเหลือติดลบ",
    404: "ไม่มีโมเดลชื่อนี้ ลองดูรายชื่อด้วย python llm.py --free",
    429: "ชนเพดานจำนวนคำขอของรุ่นฟรี รอสักครู่แล้วค่อยลองใหม่",
}


class LLMError(RuntimeError):
    pass


class Config(NamedTuple):
    provider: str
    base_url: str
    api_key: str
    model: str


def resolve(provider=None, model=None, env=None) -> Config:
    """ตัดสินว่าจะยิงไปที่ไหน ตามลำดับที่อธิบายไว้บนหัวไฟล์"""
    env = os.environ if env is None else env
    provider = provider or env.get("LLM_PROVIDER") or _guess(env) or "local"
    if provider not in PROVIDERS:
        raise LLMError(f"ไม่รู้จักผู้ให้บริการ {provider!r} "
                       f"มีให้เลือก {list(PROVIDERS)}")
    base_url, key_env, default_model = PROVIDERS[provider]
    return Config(provider, base_url.rstrip("/"),
                  env.get(key_env, "not-needed"),
                  model or env.get("LLM_MODEL") or default_model)


def _guess(env):
    return next((p for p, (_, k, _) in PROVIDERS.items() if env.get(k)), None)


def describe(cfg: Config) -> str:
    """สรุปการตั้งค่าแบบปิดบัง key เอาไว้พิมพ์ในสมุดบันทึกได้อย่างปลอดภัย"""
    key = "ไม่ได้ตั้ง" if cfg.api_key == "not-needed" else f"ตั้งแล้ว ({len(cfg.api_key)} อักขระ)"
    return f"provider={cfg.provider}  model={cfg.model}  base_url={cfg.base_url}  key={key}"


def _post(url, key, payload, timeout, retries=3):
    """ยิงคำขอ พร้อมหลบเพดานคำขอด้วยการรอแบบทวีคูณ

    รุ่นฟรีใช้โควตาร่วมกันทั้งระบบ จึงเจอ 429 เป็นครั้งคราวแม้เราจะยิงไม่ถี่
    ส่วนใหญ่รอไม่กี่วินาทีก็ผ่าน จึงลองใหม่ให้อัตโนมัติแทนที่จะให้แล็บพังกลางคัน
    """
    req = urllib.request.Request(
        url, json.dumps(payload).encode(),
        {"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read()[:400].decode("utf-8", "replace")
            if e.code == 429 and attempt < retries - 1:
                wait = float(e.headers.get("Retry-After") or 2 ** (attempt + 1))
                print(f"  ชนเพดานคำขอ รออีก {wait:.0f} วินาทีแล้วลองใหม่",
                      file=sys.stderr)
                time.sleep(wait)
                continue
            raise LLMError(f"HTTP {e.code}: {HINTS.get(e.code, '')}\n{body}") from None


def complete(messages, provider=None, model=None, tools=None, timeout=120, **opts):
    """เรียกโมเดลหนึ่งครั้ง คืน (ข้อความของผู้ช่วย, usage)

    `messages` และ `tools` ใช้รูปแบบเดียวกับ OpenAI ทุกประการ
    """
    cfg = resolve(provider, model)
    payload = {"model": cfg.model, "messages": messages, **opts}
    if tools:
        payload["tools"] = tools
    data = _post(f"{cfg.base_url}/chat/completions", cfg.api_key, payload, timeout)
    msg = data["choices"][0]["message"]
    # โมเดลสายให้เหตุผลบางตัวคืน content ว่างแล้วใส่คำตอบไว้ใน reasoning
    if not msg.get("content"):
        msg["content"] = msg.get("reasoning") or ""
    return msg, data.get("usage") or {}


def chat(messages, **kw) -> str:
    """เวอร์ชันย่อสำหรับกรณีที่อยากได้แค่ข้อความ รับสตริงตรง ๆ ก็ได้"""
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    return complete(messages, **kw)[0]["content"]


def text_llm(provider=None, model=None, temperature=0.2, price=TOKEN_PROXY):
    """คืนฟังก์ชัน llm(prompt) -> (ข้อความ, ค่าใช้จ่าย) สำหรับแล็บ 13 และ 14"""
    cfg = resolve(provider, model)

    def llm(prompt):
        msg, usage = complete([{"role": "user", "content": prompt}],
                              provider=cfg.provider, model=cfg.model,
                              temperature=temperature)
        return msg["content"], usage.get("total_tokens", 200) * price
    return llm


def free_models(tools=None, timeout=30):
    """รายชื่อ (ชื่อโมเดล, ความยาวบริบท) ของโมเดลฟรีบน OpenRouter ตอนนี้

    รายชื่อเปลี่ยนแทบทุกเดือน จึงถามสดทุกครั้งแทนที่จะฝังไว้ในโค้ด
    endpoint นี้เปิดสาธารณะ ไม่ต้องใช้ API key
    ใส่ tools=True เพื่อเอาเฉพาะตัวที่เรียกเครื่องมือได้
    """
    with urllib.request.urlopen(MODELS_URL, timeout=timeout) as r:
        data = json.load(r)["data"]
    out = []
    for m in data:
        p = m.get("pricing") or {}
        if float(p.get("prompt", 1)) or float(p.get("completion", 1)):
            continue
        if tools is not None and \
                ("tools" in (m.get("supported_parameters") or [])) is not tools:
            continue
        out.append((m["id"], m.get("context_length") or 0))
    return sorted(out, key=lambda t: -t[1])


def _self_check():
    fake = {"OPENROUTER_API_KEY": "k"}
    assert resolve(env=fake).provider == "openrouter"
    assert resolve(env=fake).model == "openrouter/free"
    assert resolve(env={}).provider == "local", "ไม่มี key ต้องตกมาที่ ollama"
    assert resolve(env={"LLM_PROVIDER": "kimi", **fake}).provider == "kimi", \
        "LLM_PROVIDER ต้องชนะการเดา"
    assert resolve("gpt", env=fake).provider == "gpt", "อาร์กิวเมนต์ต้องชนะทุกอย่าง"
    assert resolve(env={**fake, "LLM_MODEL": "z-ai/glm-5.2:free"}).model \
        == "z-ai/glm-5.2:free"
    assert "k" not in describe(resolve(env=fake)).split("key=")[1], "ห้ามหลุด key"
    try:
        resolve("ไม่มีจริง", env={})
    except LLMError:
        pass
    else:
        raise AssertionError("ผู้ให้บริการที่ไม่รู้จักต้องโยน LLMError")
    print("OK: llm.py self-check ผ่าน")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=list(PROVIDERS))
    ap.add_argument("--model")
    ap.add_argument("--ask", help="ยิงคำถามจริงหนึ่งครั้ง")
    ap.add_argument("--free", action="store_true", help="รายชื่อโมเดลฟรีบน OpenRouter")
    ap.add_argument("--tools", action="store_true", help="กับ --free: เอาเฉพาะตัวที่เรียกเครื่องมือได้")
    ap.add_argument("--self-check", action="store_true")
    args = ap.parse_args()

    if args.self_check:
        _self_check()
        return 0

    if args.free:
        rows = free_models(tools=True if args.tools else None)
        print(f"โมเดลฟรีบน OpenRouter ตอนนี้ {len(rows)} ตัว "
              f"(เรียงตามความยาวบริบท)\n")
        for name, ctx in rows:
            print(f"  {name:<52} {ctx:>9,} โทเคน")
        print("\nตรึงตัวที่จะใช้ด้วย  export LLM_MODEL=<ชื่อโมเดล>")
        print("openrouter/free สุ่มโมเดลให้ทุกครั้ง สะดวกแต่ห้ามใช้ตอนเทียบผล")
        return 0

    cfg = resolve(args.provider, args.model)
    print(describe(cfg))
    if args.ask:
        print()
        print(chat(args.ask, provider=cfg.provider, model=cfg.model))
    return 0


if __name__ == "__main__":
    sys.exit(main())

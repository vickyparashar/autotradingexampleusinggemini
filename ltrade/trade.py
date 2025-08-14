"""
LangChain pipeline:
1) Capture screenshot via takescreenshot.capture()
2) Compress to JPEG
3) Base64 encode
4) Build HumanMessage
5) Invoke Gemini

Run: python analyze_screenshot_chain.py
"""

import base64
from pathlib import Path
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableLambda
from takescreenshot import capture

# ------------------------------
# Config (POC: keep key hardcoded)
# ------------------------------
GOOGLE_API_KEY = "AIzaSyA6BWCTvYCeuOf0u-4dtDZn6CB2pHpI9eg"  # Hardcode for POC
MODEL_NAME = "gemini-1.5-flash"

ARTIFACTS_DIR = Path(__file__).parent / "artifacts"
RAW_PATH = ARTIFACTS_DIR / "tradingview_chart.png"
COMPRESSED_PATH = ARTIFACTS_DIR / "tradingview_chart_compressed.jpg"
PROMPT_TEXT = "Chart analysis: return one-word 'Buy' or 'Sell' with confidence percentage (e.g., 'Buy – 75%') in a single word."

# ------------------------------
# Steps
# ------------------------------
def step_capture(_: None) -> Path:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    # Use module defaults (no params) for consistency; save to RAW_PATH
    # If you want to override, pass url/chrome_path/wait_seconds here.
    path = capture(out_path=RAW_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Screenshot not found at {path}")
    return path

def step_compress(path: Path, max_side: int = 1600, quality: int = 82) -> Path:
    with Image.open(path) as img:
        img = img.convert("RGB")
        img.thumbnail((max_side, max_side))
        img.save(
            COMPRESSED_PATH,
            format="JPEG",
            quality=quality,
            optimize=True,
            progressive=True,
            subsampling="4:2:0",
        )
    return COMPRESSED_PATH

def step_encode(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")

def step_build_message(b64: str):
    return [HumanMessage(content=[
        {"type": "text", "text": PROMPT_TEXT},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
    ])]

def step_invoke(messages):
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=GOOGLE_API_KEY)
    return llm.invoke(messages).content

# ------------------------------
# Chain composition
# ------------------------------
pipeline = (
    RunnableLambda(step_capture)
    | RunnableLambda(step_compress)
    | RunnableLambda(step_encode)
    | RunnableLambda(step_build_message)
    | RunnableLambda(step_invoke)
)

# ------------------------------
# Run
# ------------------------------
if __name__ == "__main__":
    try:
        output = pipeline.invoke(None)
        print(output)
    except Exception as e:
        print(f"[pipeline] ERROR: {e}")
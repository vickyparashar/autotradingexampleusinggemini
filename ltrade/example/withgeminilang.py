"""
LangChain Gemini Image Analysis - POC Implementation
"""

import base64
import io
from pathlib import Path
from typing import Union
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# ------------------------------
# 🔐 Config - POC use only
# ------------------------------
GOOGLE_API_KEY = "AIzaSyA6BWCTvYCeuOf0u-4dtDZn6CB2pHpI9eg"
MODEL_NAME = "gemini-1.5-flash"

# ------------------------------
# 📦 Utilities
# ------------------------------
def encode_image_to_base64(image_path: Union[str, Path]) -> str:
    """Load and encode an image to base64."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    with Image.open(path) as img:
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

def build_multimodal_message(prompt: str, image_base64: str) -> HumanMessage:
    """Construct a LangChain-compatible multimodal message."""
    return HumanMessage(content=[
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
    ])

# ------------------------------
# 🧠 LangChain Model Initialization
# ------------------------------
def get_gemini_model() -> ChatGoogleGenerativeAI:
    """Create and return a configured Gemini chat model."""
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY
    )

# ------------------------------
# 🚀 Application Entry Point
# ------------------------------
def analyze_image(image_path: str, prompt: str) -> None:
    """Run image analysis through Gemini model."""
    image_base64 = encode_image_to_base64(image_path)
    message = build_multimodal_message(prompt, image_base64)
    llm = get_gemini_model()
    response = llm.invoke([message])  # Could be swapped for chain() or stream()
    print(response.content)

# ------------------------------
# ▶ POC Execution
# ------------------------------
if __name__ == "__main__":
    IMAGE_PATH = r"C:\VickyJD\Tools\sampletool\tradingview_chart.jpeg"
    PROMPT = "describe the fruit in this image"
    analyze_image(IMAGE_PATH, PROMPT)
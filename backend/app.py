from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import base64
import tempfile
import os
from utils.ollama_helper import query_ollama_text_only
from utils.ollama_helper import query_ollama
from utils.dom_parser import extract_dom_summary
from test_executor import execute_playwright_code

app = FastAPI()

# Allow frontend access (React, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TestResponse(BaseModel):
    status: str
    steps: list
    raw_output: str
    playwright_code: str
    execution_output: Optional[str] = None
    execution_error: Optional[str] = None

def convert_steps_to_code(steps: list) -> str:
    formatted_steps = "\n".join(steps)
    prompt = (
        "You are a QA automation assistant. Convert the following test steps "
        "into executable Playwright Python code using the sync API:\n\n"
        f"{formatted_steps}\n\n"
        "Use Playwright's page object (e.g. page.goto, page.fill, page.click, page.expect_response, etc.)"
    )
    return query_ollama_text_only(prompt)

@app.post("/test")
async def run_multimodal_test(
    screenshot: UploadFile,
    prompt: str = Form(...),
    dom_html: Optional[str] = Form(None)
):
    print("✅ Received request!")
    print("Prompt:", prompt)
    # 1. Save and base64 encode the screenshot
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    tmp.write(await screenshot.read())
    tmp.close()

    with open(tmp.name, "rb") as f:
        b64_image = base64.b64encode(f.read()).decode("utf-8")

    # 2. Extract useful structure from DOM (optional)
    dom_summary = extract_dom_summary(dom_html) if dom_html else "None"

    # 3. Construct AI prompt
    full_prompt = (
        "You are a QA automation agent.\n"
        "Based on the functionality request, DOM structure, and screenshot, "
        "generate a sequence of test steps (one per line) that could be automated in Playwright.\n\n"
        f"Functionality Prompt:\n{prompt}\n\n"
        f"DOM Summary:\n{dom_summary}\n"
    )

    # 4. Query Ollama
    ai_output = query_ollama(prompt=full_prompt, image_base64=b64_image)
    playwright_code = convert_steps_to_code(ai_output.strip().splitlines())
    execution = execute_playwright_code(playwright_code)
    return TestResponse(
    status="executed",
    steps=ai_output.strip().splitlines(),
    raw_output=ai_output.strip(),
    playwright_code=playwright_code,
    execution_output=execution.get("stdout"),
    execution_error=execution.get("stderr") or execution.get("error")
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

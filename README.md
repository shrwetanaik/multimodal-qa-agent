# 🤖 Multimodal QA Agent

This is an AI-powered QA automation prototype that takes a screenshot, a natural language test prompt, and optional DOM HTML — then generates and executes Playwright test cases using LLMs (via Ollama + LLaVA).

### 🧠 Features
- Multimodal: Screenshot + Prompt + DOM
- LLM-powered test step and code generation
- Playwright test execution with result logs
- Frontend: React
- Backend: FastAPI
- Local models via Ollama (LLaVA, Llama3)

### 🚀 How to Run
1. `pip install -r backend/requirements.txt`
2. `playwright install`
3. `uvicorn backend.app:app --reload`
4. `cd frontend && npm install && npm start`


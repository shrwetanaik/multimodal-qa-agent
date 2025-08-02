import subprocess
import tempfile
import os

def execute_playwright_code(code: str) -> dict:
    print("📜 Executing Playwright code:")
    print(code)
    try:
        # Create a temp Python file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp:
            tmp.write(code)
            script_path = tmp.name

        # Run the script and capture output
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            timeout=20  # avoid long loops
        )
        print("🧪 Execution result:")
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "script_path": script_path
        }
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out"}
    except Exception as e:
        return {"error": str(e)}

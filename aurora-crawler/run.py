from aurora_platform.main import app
import uvicorn
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

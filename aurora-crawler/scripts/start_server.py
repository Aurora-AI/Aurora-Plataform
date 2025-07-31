import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import uvicorn
from aurora_platform.main import app

if __name__ == "__main__":
    print("Iniciando servidor Aurora Platform...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

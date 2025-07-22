import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.workers.detector import run_detection

if __name__ == "__main__":
    run_detection()

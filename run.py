from src.db import init_db
from src.detector import run_detector

if __name__ == "__main__":
    init_db()
    run_detector()
    
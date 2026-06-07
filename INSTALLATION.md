# Installation

Follow these steps to set up the project locally.

1. Clone the repository:

```bash
git clone https://github.com/kalpnabhatia139-sys/AI_Wildlife_Poaching_Detector.git
cd AI_Wildlife_Poaching_Detector
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# macOS / Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. (Optional) If you need to download models:

```bash
python download_model.py
```

5. Run the web dashboard:

```bash
python web_dashboard.py
```

6. Run detection (example):

```bash
python run.py
```

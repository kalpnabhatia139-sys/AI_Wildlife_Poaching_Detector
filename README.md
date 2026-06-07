# AI Wildlife Poaching Detector

An AI-powered system designed to detect and prevent wildlife poaching using YOLOv8 object detection.

## Features
- Real-time object detection using YOLOv8
- Webcam integration for live monitoring
- Email alerts for threats
- Web dashboard for monitoring
- Database logging of alerts

## Project Structure
```
├── src/
│   ├── alert.py        # Alert system
│   ├── config.py       # Configuration
│   ├── db.py          # Database operations
│   ├── detector.py    # Detection logic
│   └── utils.py       # Utility functions
├── models/            # Trained models
├── data/              # Dataset files
├── tests/             # Unit tests
├── web_dashboard.py   # Web interface
├── run.py             # Main entry point
└── requirements.txt   # Dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/AI_Wildlife_Poaching_Detector.git
cd AI_Wildlife_Poaching_Detector
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run Detection:
```bash
python run.py
```

### Start Web Dashboard:
```bash
python web_dashboard.py
```

### Run Tests:
```bash
pytest
```

## Requirements
See `requirements.txt` for all dependencies.

## License
[Your License Here]

## Author
[Your Name]

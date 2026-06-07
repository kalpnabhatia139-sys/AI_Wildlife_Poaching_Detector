# AI Wildlife Poaching Detector

An AI-powered system to detect and help prevent wildlife poaching using YOLOv8 object detection.

![CI](https://github.com/kalpnabhatia139-sys/AI_Wildlife_Poaching_Detector/actions/workflows/python-tests.yml/badge.svg)

## Features
- Real-time object detection using YOLOv8
- Webcam integration for live monitoring
- Email alerts for detected threats
- Web dashboard for monitoring and logs
- Database logging of alerts

## Project Structure
```
├── src/                # Application source code
├── models/             # Trained model files (ignored by git)
├── data/               # Dataset and supporting data
├── tests/              # Unit tests (pytest)
├── web_dashboard.py    # Web interface
├── run.py              # Main entry point for detection
└── requirements.txt    # Python dependencies
```

## Installation

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

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. (Optional) Download models if needed:

```bash
python download_model.py
```

## Usage

Run the detector:

```bash
python run.py
```

Start the web dashboard:

```bash
python web_dashboard.py
```

Run tests:

```bash
pytest
```

## Contributing
See `CONTRIBUTING.md` for contribution guidelines.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

## Author
kalpnabhatia139-sys

# Vision System

This module handles computer vision processing for the Scouty robot using OpenCV and MediaPipe.

## Features

- Object detection and tracking
- Person following using MediaPipe pose detection
- Camera interface for Raspberry Pi
- Real-time image processing

## Dependencies

- Python 3.7+
- OpenCV (cv2)
- MediaPipe
- NumPy

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from vision.detector import ObjectDetector
from vision.tracker import PersonTracker

# Initialize vision components
detector = ObjectDetector()
tracker = PersonTracker()
```

## Modules

- `camera.py` - Camera interface and capture
- `detector.py` - Object detection using OpenCV
- `tracker.py` - Person tracking using MediaPipe
- `processor.py` - Image preprocessing and utilities

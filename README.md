# EMG-Based Prosthesis Control Using Machine Learning

A real-time prosthesis control system that classifies EMG signals from a MYO armband using a Decision Tree machine learning model to perform 4 different pinch movements.

## 📋 Project Overview

This project implements an intelligent prosthesis control system that:
- Captures real-time EMG signals from a MYO armband worn on the forearm
- Classifies signals into 4 pinch movements using a Decision Tree classifier
- Controls servo motors on a robotic prosthetic hand
- Achieves **97-98% accuracy** on real EMG data

### Key Features
- **Machine Learning Model**: Decision Tree classifier (max_depth=32)
- **Hardware Control**: Arduino microcontroller with servo motor interface
- **Real-time Classification**: Fast signal processing and classification
- **Multi-movement Support**: 4 distinct pinch gestures
  - Pinch 1: Thumb (120°) + Index (90°)
  - Pinch 2: Thumb (130°) + Middle (90°)
  - Pinch 3: Thumb (170°) + Ring (90°)
  - Pinch 4: Thumb (180°) + Pinky (90°)

## 🔧 Technical Stack

| Component | Technology |
|-----------|-----------|
| **ML Framework** | Python, scikit-learn |
| **Sensor** | MYO Armband (8 EMG sensors) |
| **Microcontroller** | Arduino (Uno/Mega) |
| **Actuators** | Servo Motors (SG90 or equivalent) |
| **Communication** | Serial (UART) |

## 📁 Project Structure

```
Upper-LimbProsthetic-Arm-Control-Using-Machine-Learning/
├── README.md
├── LICENSE                        # MIT License
├── CONTRIBUTING.md
├── requirements.txt               # Python dependencies
├── .gitignore
├── python/
│   ├── signal_processing.py       # EMG filtering, normalisation, feature extraction
│   └── emg_classifier.py          # Decision Tree classifier (train / predict / save / load)
├── arduino/
│   └── prosthesis_controller.ino  # Servo control over serial
├── docs/
│   ├── INSTALLATION.md
│   └── USAGE.md
└── tests/
    ├── test_signal_processing.py
    └── test_classifier.py
```

> **Status:** the repository contains the processing and classification modules,
> the Arduino controller and tests. The training / evaluation / real-time scripts
> that `docs/INSTALLATION.md` and `docs/USAGE.md` refer to (`train_model.py`,
> `evaluate_model.py`, `real_time_prediction.py`, ...) and pre-trained models are
> not included yet; the examples below use the modules directly.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Arduino IDE
- MYO SDK/drivers installed
- Arduino board (Uno/Mega) with servo motors

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ammardaher/Upper-LimbProsthetic-Arm-Control-Using-Machine-Learning.git
   cd Upper-LimbProsthetic-Arm-Control-Using-Machine-Learning
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Load the Arduino sketch**
   - Open `arduino/prosthesis_controller.ino` in the Arduino IDE
   - Select your board type and COM port
   - Upload to the microcontroller

### Usage

**Features and classification in Python**
```python
import sys; sys.path.insert(0, "python")
from signal_processing import process_emg_batch
from emg_classifier import EMGClassifier

# signals: (n_samples, 8 channels, n_points) at 200 Hz; labels: 0-3 (Pinch 1-4)
X = process_emg_batch(signals, sampling_rate=200)
clf = EMGClassifier(max_depth=32)
clf.train(X, labels)
print(clf.evaluate(X_test, y_test))   # held-out features / labels
clf.save_model("models/decision_tree_model.pkl")
```

**Driving the hand (serial, 9600 baud)**

| Command | Action |
|---|---|
| `0`-`3` | Pinch 1-4 |
| `R` | rest position |
| `D` | toggle debug output |

The sketch returns to rest if no command arrives for 1 s, so the host should
resend the current class continuously while a gesture is held.

## 📊 Performance Metrics

- **Accuracy**: 97-98% on test dataset
- **Latency**: < 100ms per classification
- **Dataset Size**: 12,000 signals processed
- **Classifier**: Decision Tree (max_depth=32)
- **Input Features**: 8 EMG channels from MYO armband

## 🔌 Hardware Connections

The servo pins are defined at the top of `arduino/prosthesis_controller.ino` (`SERVO_PIN_*`).

**Basic Arduino Pinout:**
- Servo 1 (Thumb): Pin 9
- Servo 2 (Index): Pin 10
- Servo 3 (Middle): Pin 11
- Servo 4 (Ring): Pin 12
- Servo 5 (Pinky): Pin 13
- MYO Serial RX: Pin 0
- MYO Serial TX: Pin 1

## 📚 Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions
- **[Usage Guide](docs/USAGE.md)** - How to run the system (parts describe scripts not yet in the repository, see Status above)

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

The classifier tests are skipped automatically if scikit-learn is not installed.

## 🔬 Model Training

Train on your own recordings with the modules shown under Usage: build the
feature matrix with `process_emg_batch`, then call `EMGClassifier.train`,
`evaluate` and `save_model`.

## 🛠️ Troubleshooting

### MYO Not Connecting
- Ensure MYO SDK is installed
- Check Bluetooth connection

### Poor Classification Accuracy
- Re-calibrate MYO armband
- Check for signal noise/interference
- Retrain model with more diverse data
- Verify electrode placement

### Servo Motors Not Moving
- Check Arduino connections
- Verify servo power supply
- Send `0`-`3` / `R` from the Arduino Serial Monitor (9600 baud) to test each servo

## 📈 Future Improvements

- [ ] Add more movement classes (wrist rotation, finger flexion)
- [ ] Implement adaptive threshold tuning
- [ ] Add IMU data for better gesture recognition
- [ ] Deploy on edge devices (Raspberry Pi, Jetson Nano)
- [ ] Develop mobile app for parameter tuning
- [ ] Add real-time feedback sensors to prosthesis
- [ ] Implement feedback control loop

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute
- Report bugs and issues
- Suggest new features
- Improve documentation
- Add new ML algorithms
- Optimize performance
- Expand test coverage

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👤 Author

**Salman Daher**  
National Center for the Distinguished, Syria  
EMG-Based Prosthesis Control Research Project

## 🙏 Acknowledgments

- Dataset from [Donati et al. (2019)](https://zenodo.org/record/3194792)
- MYO armband by Thalmic Labs
- scikit-learn machine learning library
- Arduino community

## 📞 Contact & Support

- **Issues**: Use GitHub Issues for bug reports
- **Discussions**: Use GitHub Discussions for questions

## 📖 References

1. Donati, E. (2019). EMG from forearm datasets for hand gestures recognition. Zenodo. https://doi.org/10.5281/zenodo.3194792
2. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825-2830.
3. Miry, M. Z.-F. (n.d.). Artificial Human Arm Driven by EMG Signal. InTech.
4. Robinson, J. (2019). Using a Prosthetic Device. WebMD.

---

**Last Updated**: December 2025  
**Status**: Active Development  
**Version**: 1.0.0

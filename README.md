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
emg-prosthesis-control/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
├── CONTRIBUTING.md                    # Contribution guidelines
├── .gitignore                         # Git ignore rules
│
├── python/
│   ├── emg_classifier.py             # Decision Tree classifier model
│   ├── signal_processing.py          # EMG signal filtering & feature extraction
│   ├── train_model.py                # Model training script
│   ├── evaluate_model.py             # Model evaluation & testing
│   ├── real_time_prediction.py       # Real-time classification from MYO
│   └── utils.py                      # Helper functions
│
├── arduino/
│   ├── prosthesis_controller.ino     # Main Arduino sketch
│   ├── servo_control.cpp             # Servo motor control library
│   ├── serial_handler.cpp            # Serial communication handler
│   └── config.h                      # Hardware configuration
│
├── data/
│   ├── training_data/                # EMG datasets for training
│   │   └── README.md
│   ├── test_data/                    # Test datasets
│   │   └── README.md
│   └── raw_signals/                  # Raw EMG recordings
│       └── README.md
│
├── models/
│   ├── decision_tree_model.pkl       # Trained classifier (serialized)
│   ├── model_metadata.json           # Model parameters & performance
│   └── scaler.pkl                    # Signal scaler for normalization
│
├── docs/
│   ├── INSTALLATION.md               # Setup & installation guide
│   ├── USAGE.md                      # How to use the system
│   ├── HARDWARE_SETUP.md             # Hardware wiring & assembly
│   ├── CALIBRATION.md                # MYO armband calibration
│   ├── TROUBLESHOOTING.md            # Common issues & solutions
│   └── API.md                        # Code API documentation
│
├── tests/
│   ├── test_classifier.py            # Unit tests for ML model
│   ├── test_signal_processing.py     # Signal processing tests
│   └── test_serial_communication.py  # Serial communication tests
│
└── examples/
    ├── basic_classification.py       # Simple classification example
    ├── real_time_demo.py             # Real-time EMG demo
    └── hardware_test.ino             # Arduino hardware test sketch
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Arduino IDE
- MYO SDK/drivers installed
- Arduino board (Uno/Mega) with servo motors

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/emg-prosthesis-control.git
   cd emg-prosthesis-control
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Load Arduino sketch**
   - Open `arduino/prosthesis_controller.ino` in Arduino IDE
   - Select your board type and COM port
   - Upload to microcontroller

4. **Download pre-trained model**
   - Models are in `models/` directory
   - Or train your own with `python/train_model.py`

### Usage

**Real-time Classification**
```bash
python python/real_time_prediction.py
```

**Test with existing data**
```bash
python python/evaluate_model.py
```

## 📊 Performance Metrics

- **Accuracy**: 97-98% on test dataset
- **Latency**: < 100ms per classification
- **Dataset Size**: 12,000 signals processed
- **Classifier**: Decision Tree (max_depth=32)
- **Input Features**: 8 EMG channels from MYO armband

## 🔌 Hardware Connections

See `docs/HARDWARE_SETUP.md` for detailed wiring diagrams and pin configurations.

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
- **[Usage Guide](docs/USAGE.md)** - How to run the system
- **[Hardware Setup](docs/HARDWARE_SETUP.md)** - Wiring & assembly
- **[Calibration Guide](docs/CALIBRATION.md)** - MYO armband calibration
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues
- **[API Documentation](docs/API.md)** - Code reference

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

## 🔬 Model Training

To train a new model with your own data:

```bash
python python/train_model.py \
  --data data/training_data/emg_signals.csv \
  --output models/custom_model.pkl \
  --max_depth 32 \
  --test_size 0.2
```

## 🛠️ Troubleshooting

### MYO Not Connecting
- Ensure MYO SDK is installed
- Check Bluetooth connection
- See `docs/TROUBLESHOOTING.md`

### Poor Classification Accuracy
- Re-calibrate MYO armband
- Check for signal noise/interference
- Retrain model with more diverse data
- Verify electrode placement

### Servo Motors Not Moving
- Check Arduino connections
- Verify servo power supply
- Test with `examples/hardware_test.ino`

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
- **Email**: your.email@example.com

## 📖 References

1. Donati, E. (2019). EMG from forearm datasets for hand gestures recognition. Zenodo. https://doi.org/10.5281/zenodo.3194792
2. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825-2830.
3. Miry, M. Z.-F. (n.d.). Artificial Human Arm Driven by EMG Signal. InTech.
4. Robinson, J. (2019). Using a Prosthetic Device. WebMD.

---

**Last Updated**: December 2025  
**Status**: Active Development  
**Version**: 1.0.0

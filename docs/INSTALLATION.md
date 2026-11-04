# Installation and Setup Guide

Complete guide to set up the EMG-Based Prosthesis Control system.

## Prerequisites

### Hardware
- Arduino Uno or Mega microcontroller
- MYO Armband (original Thalmic Labs or compatible)
- 5x Servo Motors (SG90 or similar - 5V, ~2kg torque)
- Power supply (suitable for servo current draw, typically 2A @ 5V)
- USB cable for Arduino programming
- Breadboard and jumper wires
- Resistors/capacitors for filtering (optional)

### Software
- Python 3.8 or higher
- Arduino IDE (version 1.8.13 or later)
- Git (for cloning repository)

### OS Support
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+)

## Step 1: System Requirements

### Python Installation

**Windows:**
```bash
# Download from https://www.python.org/downloads/
# Run installer and ensure "Add Python to PATH" is checked
python --version
```

**macOS:**
```bash
brew install python3
python3 --version
```

**Linux:**
```bash
sudo apt-get install python3 python3-pip
python3 --version
```

### Arduino IDE

1. Download from https://www.arduino.cc/en/software
2. Install following platform-specific instructions
3. Launch Arduino IDE

## Step 2: Repository Setup

```bash
# Clone the repository
git clone https://github.com/ammardaher/Upper-LimbProsthetic-Arm-Control-Using-Machine-Learning.git
cd Upper-LimbProsthetic-Arm-Control-Using-Machine-Learning

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

## Step 3: MYO Armband Setup

### Install MYO SDK

1. Download MYO SDK from https://support.getmyo.com/hc/en-us/articles/360018409152
2. Extract and install following platform instructions
3. Install MYO drivers

### Pair MYO with Computer

**Windows:**
1. Download and run MYO Connect
2. Put MYO armband on forearm
3. Wait for device discovery
4. Follow pairing instructions in MYO Connect

**macOS/Linux:**
```bash
# Install via pip if available
pip install myo

# Or follow manual SDK installation
```

### Calibrate MYO Armband

1. Launch MYO Connect
2. Go to Calibration
3. Follow on-screen instructions:
   - Point hand forward with palm down
   - Make a fist
   - Open hand wide
   - Thumb up
   - Pinky out
4. Save calibration

## Step 4: Arduino Setup

### Install Arduino Boards

1. Open Arduino IDE
2. Go to **Tools > Board > Boards Manager**
3. Search for "Arduino AVR Boards"
4. Click Install (should already be installed)

### Load and Verify Sketch

1. Open Arduino IDE
2. File > Open
3. Navigate to `arduino/prosthesis_controller.ino`
4. Select Board:
   - Tools > Board > Arduino AVR Boards > Arduino Uno (or your board)
5. Select Port:
   - Tools > Port > COM3 (or /dev/ttyUSB0 on Linux)
6. Click Upload (Ctrl+U)

**Expected output:**
```
Sketch uses 5,234 bytes of program storage space.
Maximum is 32,256 bytes.
Global variables use 563 bytes of dynamic memory.
```

## Step 5: Hardware Assembly

### Servo Motor Connections

```
Arduino Pin -> Servo Pin
    9       -> Thumb servo PWM (orange)
    10      -> Index servo PWM (orange)
    11      -> Middle servo PWM (orange)
    12      -> Ring servo PWM (orange)
    13      -> Pinky servo PWM (orange)
    
GND (Arduino) -> All servo GND (black)
5V (Arduino)  -> All servo VCC (red) [via power supply]
```

### Power Supply Connection

**Important:** Do NOT power servos directly from Arduino 5V pin (insufficient current).

1. Connect external 5V power supply to breadboard
2. Connect power supply GND to Arduino GND (common ground)
3. Connect power supply 5V to servo VCC rail

### Serial Communication (MYO to Arduino)

For USB connection:
- USB cable connects MYO to Arduino via serial adapter
- Arduino RX (pin 0) <- MYO TX
- Arduino TX (pin 1) <- MYO RX

## Step 6: Python Environment

### Verify Installation

```bash
# Test Python
python --version

# Test dependencies
python -c "import sklearn; print(sklearn.__version__)"
python -c "import numpy; print(numpy.__version__)"
python -c "import serial; print('pyserial OK')"
```

### Download Pre-trained Model

The trained Decision Tree model is in `models/` directory:
- `decision_tree_model.pkl` - Main classifier
- `model_metadata.json` - Model parameters

If not present, train new model:
```bash
python python/train_model.py
```

## Step 7: Test Your Setup

### Arduino Test

1. Connect Arduino to computer via USB
2. Open Arduino IDE
3. Tools > Serial Monitor (Ctrl+Shift+M)
4. Set baud rate to 9600
5. Type commands:
   - `0` - Execute Pinch 1
   - `1` - Execute Pinch 2
   - `R` - Return to rest
   - `D` - Toggle debug

You should see:
```
EMG Prosthesis Controller - Initializing...
All servos initialized - Ready for commands
Commands: 0-3 (pinch 1-4), R (rest), D (debug toggle)
-> Pinch 1 executed
```

### Python Test

```bash
cd python

# Test signal processing
python -c "from signal_processing import EMGSignalProcessor; print('Signal processor OK')"

# Test classifier
python -c "from emg_classifier import EMGClassifier; clf = EMGClassifier(); print('Classifier OK')"

# Run real-time demo (requires MYO)
python real_time_prediction.py
```

### Full System Test

```bash
# Terminal 1: Start Python classification
cd python
python real_time_prediction.py

# Terminal 2: Monitor Arduino
arduino_serial_monitor.py

# Manual test: Send commands to Arduino
# Arduino should receive classification results and move servos
```

## Troubleshooting

### Arduino Upload Fails

**Error: "Board not found"**
- Check USB cable
- Verify board selection in Tools > Board
- Try different COM port

**Error: "Permission denied"**
- Linux: `sudo usermod -a -G dialout $USER`
- Restart and reconnect Arduino

### MYO Not Detecting

- Ensure MYO is charged
- Re-pair in MYO Connect
- Check Bluetooth is enabled
- Move MYO away from metal objects

### Servos Not Moving

- Verify Arduino sketch uploaded successfully
- Check power supply voltage (should be 5V)
- Test individual servo with Arduino servo sweep example
- Check servo connection pins match code

### Poor EMG Signal

- Ensure MYO armband is snug but comfortable
- Relax forearm muscles initially
- Perform calibration again
- Check for EMI (power supplies, motors nearby)

### Python Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check versions
pip list

# If specific package fails:
pip install scikit-learn==1.3.2 --no-cache-dir
```

## Next Steps

1. **Calibration** - See `CALIBRATION.md`
2. **Usage** - See `USAGE.md`
3. **Train Custom Model** - See `python/train_model.py`
4. **Troubleshooting** - See `TROUBLESHOOTING.md`

## Support

For issues:
1. Check `TROUBLESHOOTING.md`
2. Review `docs/` directory
3. Open GitHub Issue with:
   - Error message
   - OS and Python version
   - Arduino board type
   - Steps to reproduce

---

**Congratulations!** Your EMG prosthesis control system is ready.

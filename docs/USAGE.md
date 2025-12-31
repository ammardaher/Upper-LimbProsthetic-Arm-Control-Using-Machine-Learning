# Usage Guide

How to use the EMG-Based Prosthesis Control System.

## Quick Start

### 1. Start Arduino Serial Monitor

```bash
# Option A: Arduino IDE Serial Monitor
# Tools > Serial Monitor (Ctrl+Shift+M)
# Set baud rate to 9600

# Option B: Python serial monitor
python scripts/serial_monitor.py
```

### 2. Start Python Classification

```bash
cd python
python real_time_prediction.py
```

### 3. Perform Gestures

Wear the MYO armband and perform hand gestures:
- **Pinch 1**: Thumb touching index finger
- **Pinch 2**: Thumb touching middle finger
- **Pinch 3**: Thumb touching ring finger
- **Pinch 4**: Thumb touching pinky finger

The system will:
1. Capture EMG signals from MYO
2. Extract features
3. Classify gesture using Decision Tree
4. Send command to Arduino
5. Move prosthesis servo motors

## Command Reference

### Serial Commands

Send to Arduino via Serial Monitor:

| Command | Action |
|---------|--------|
| `0` | Execute Pinch 1 (Thumb + Index) |
| `1` | Execute Pinch 2 (Thumb + Middle) |
| `2` | Execute Pinch 3 (Thumb + Ring) |
| `3` | Execute Pinch 4 (Thumb + Pinky) |
| `R` | Return to rest position |
| `D` | Toggle debug output on/off |

### Servo Angles

```
Rest Position:      [0, 0, 0, 0, 0]
Pinch 1: Thumb+Idx  [120, 90, 0, 0, 0]
Pinch 2: Thumb+Mid  [130, 0, 90, 0, 0]
Pinch 3: Thumb+Rng  [170, 0, 0, 90, 0]
Pinch 4: Thumb+Pin  [180, 0, 0, 0, 90]
```

## Workflow Examples

### Example 1: Manual Testing

```python
# python/test_manual.py
from emg_classifier import EMGClassifier
import joblib

# Load pre-trained model
clf = EMGClassifier()
clf.load_model('models/decision_tree_model.pkl')

# Test on sample data
import numpy as np
test_sample = np.random.randn(8)  # 8 EMG channels

prediction, confidence = clf.get_confidence(test_sample.reshape(1, -1))
print(f"Predicted: Pinch {prediction[0] + 1}, Confidence: {confidence[0]:.2f}")
```

### Example 2: Real-time Classification

```bash
cd python
python real_time_prediction.py
```

Monitor output:
```
Connected to MYO armband
Listening for gestures...
[14:32:45] Pinch 1 detected - Confidence: 0.98 -> Sending command '0' to Arduino
[14:32:52] Pinch 3 detected - Confidence: 0.95 -> Sending command '2' to Arduino
[14:32:58] Rest detected -> Sending command 'R' to Arduino
```

### Example 3: Evaluate Model Performance

```bash
python python/evaluate_model.py
```

Output:
```
Model Evaluation Results
=======================
Accuracy:  0.9798
Precision: 0.9801
Recall:    0.9795
F1-Score:  0.9798

Confusion Matrix:
     Pinch1  Pinch2  Pinch3  Pinch4
P1    [2340]   [32]     [12]     [16]
P2      [28] [2356]     [9]      [7]
P3      [18]    [14]  [2355]     [13]
P4      [14]     [8]     [24]   [2354]

Per-class Metrics:
Pinch 1: Precision=0.98, Recall=0.97, F1=0.98
Pinch 2: Precision=0.98, Recall=0.98, F1=0.98
Pinch 3: Precision=0.98, Recall=0.98, F1=0.98
Pinch 4: Precision=0.98, Recall=0.97, F1=0.98
```

## Advanced Usage

### Train Custom Model

```bash
python python/train_model.py \
  --data data/training_data/emg_dataset.csv \
  --output models/custom_model.pkl \
  --max_depth 32 \
  --test_size 0.2 \
  --random_state 42
```

### Extract Features Only

```python
from signal_processing import EMGSignalProcessor
import numpy as np

processor = EMGSignalProcessor(sampling_rate=200, n_channels=8)

# Raw EMG signal
raw_signal = np.random.randn(800)  # 4 seconds at 200 Hz

# Extract features
features = processor.extract_all_features(raw_signal, window_size=50)
print(f"Feature vector shape: {features.shape}")
print(f"Features: {features}")
```

### Batch Processing

```python
from signal_processing import process_emg_batch
import numpy as np

# Batch of signals: (n_samples, n_channels, n_points)
signals = np.random.randn(100, 8, 800)

# Process all
features = process_emg_batch(signals, sampling_rate=200)
print(f"Processed {features.shape[0]} signals")
print(f"Feature matrix shape: {features.shape}")
```

### Calibration for New User

```python
# python/calibrate.py
from emg_classifier import EMGClassifier
from signal_processing import EMGSignalProcessor
import numpy as np

print("EMG Prosthesis Calibration")
print("=" * 40)

processor = EMGSignalProcessor()

# Collect reference signals for each movement
movements = ["Pinch 1", "Pinch 2", "Pinch 3", "Pinch 4"]
calibration_data = {}

for movement in movements:
    print(f"\nPrepare to perform: {movement}")
    input("Press ENTER when ready...")
    
    # Collect 30 seconds of signal (would connect to MYO in real implementation)
    # raw_signal = myo_stream.get_signal(duration=30)
    
    # Extract features
    features = processor.extract_all_features(raw_signal)
    calibration_data[movement] = features
    
    print(f"Captured {len(features)} samples for {movement}")

# Save calibration
print("\nCalibration complete!")
```

## Performance Optimization

### Reduce Latency

```python
# Use faster inference
clf = EMGClassifier(max_depth=16)  # Shallower tree = faster
clf.load_model('models/decision_tree_model_fast.pkl')

# Prediction is now <50ms per sample
```

### Reduce Power Consumption

```python
# Process fewer channels if possible
processor = EMGSignalProcessor(n_channels=4)  # Use 4 channels instead of 8

# Use smaller window sizes
features = processor.extract_all_features(signal, window_size=25)  # 25 instead of 50
```

## Debugging

### Enable Debug Output

In Arduino Serial Monitor:
```
D          # Toggle debug mode ON
0          # Send command
-> Pinch 1 executed   # Debug output shows command received
D          # Toggle debug mode OFF
```

### Check Signal Quality

```python
# python/check_signal_quality.py
import numpy as np
from signal_processing import EMGSignalProcessor

processor = EMGSignalProcessor()

# Get sample signal
raw = np.array([...])  # Your raw EMG data

# Check signal statistics
filtered = processor.bandpass_filter(raw)
print(f"Signal RMS: {np.sqrt(np.mean(filtered**2))}")
print(f"Signal range: {filtered.min():.3f} to {filtered.max():.3f}")
print(f"Signal std: {np.std(filtered):.3f}")

# Visualize
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(raw)
plt.title('Raw Signal')
plt.subplot(1, 2, 2)
plt.plot(filtered)
plt.title('Filtered Signal')
plt.tight_layout()
plt.show()
```

## Common Tasks

### Task: Test One Servo

```bash
# Arduino IDE > Examples > Servo > Sweep
# Modify to test single servo
// Sweep servo on pin 9
Servo myservo;
myservo.attach(9);
myservo.write(90);  // Center position
```

### Task: Measure Classification Latency

```python
import time
from emg_classifier import EMGClassifier
import numpy as np

clf = EMGClassifier()
clf.load_model('models/decision_tree_model.pkl')

# Test data
X = np.random.randn(1000, 8)

# Measure
start = time.time()
predictions = clf.predict(X)
elapsed = time.time() - start

print(f"Classified {X.shape[0]} samples in {elapsed:.3f}s")
print(f"Average latency: {(elapsed/X.shape[0])*1000:.2f}ms per sample")
```

### Task: Generate Feature Matrix for Testing

```python
from signal_processing import EMGSignalProcessor
import numpy as np
import pandas as pd

processor = EMGSignalProcessor()

# Generate synthetic EMG data
n_samples = 1000
n_channels = 8
n_points = 800

features = []
labels = []

for label in range(4):  # 4 classes
    for _ in range(250):  # 250 samples per class
        # Generate synthetic signal
        signal = np.random.randn(n_channels, n_points)
        feature = processor.extract_all_features(signal)
        features.append(feature)
        labels.append(label)

# Save as CSV
df = pd.DataFrame(features)
df['label'] = labels
df.to_csv('test_features.csv', index=False)
print(f"Generated {len(features)} feature vectors")
```

## Troubleshooting Usage

### "No predictions"
- Check MYO armband is paired
- Verify real_time_prediction.py is running
- Check serial port is correct
- Ensure Arduino Serial Monitor is closed (ports can't be shared)

### "High latency"
- Reduce window size in signal processor
- Use shallower decision tree
- Close other serial monitoring applications
- Check USB connection quality

### "Inconsistent predictions"
- Recalibrate MYO armband
- Ensure proper electrode contact
- Perform movements more slowly
- Train model with more diverse data

---

**Need help?** See TROUBLESHOOTING.md or check GitHub Issues.

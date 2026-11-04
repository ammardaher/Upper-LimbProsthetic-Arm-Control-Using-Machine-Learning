"""
Signal Processing Module
Handles EMG signal filtering, normalization, and feature extraction
"""

import numpy as np
from scipy import signal
from typing import Tuple


class EMGSignalProcessor:
    """Process and extract features from raw EMG signals."""
    
    def __init__(self, sampling_rate: int = 200, n_channels: int = 8):
        """
        Initialize the signal processor.
        
        Args:
            sampling_rate: EMG sampling rate in Hz (default: 200 for MYO)
            n_channels: Number of EMG channels (default: 8 for MYO)
        """
        self.sampling_rate = sampling_rate
        self.n_channels = n_channels
    
    @staticmethod
    def bandpass_filter(signal_data: np.ndarray,
                       lowcut: float = 20,
                       highcut: float = 95,
                       order: int = 4,
                       fs: int = 200) -> np.ndarray:
        """
        Apply bandpass filter to EMG signal.

        Args:
            signal_data: Raw EMG signal
            lowcut: Low frequency cutoff in Hz
            highcut: High frequency cutoff in Hz. Must be below the Nyquist
                frequency (fs / 2); the MYO samples at 200 Hz, so the usable
                EMG band ends just under 100 Hz.
            order: Filter order
            fs: Sampling frequency

        Returns:
            Filtered signal
        """
        nyquist = fs / 2
        if not 0 < lowcut < highcut < nyquist:
            raise ValueError(
                f"Need 0 < lowcut < highcut < fs/2 ({nyquist} Hz); "
                f"got lowcut={lowcut}, highcut={highcut}, fs={fs}"
            )
        low = lowcut / nyquist
        high = highcut / nyquist
        
        b, a = signal.butter(order, [low, high], btype='band')
        filtered = signal.filtfilt(b, a, signal_data)
        
        return filtered
    
    @staticmethod
    def normalize_signal(signal_data: np.ndarray) -> np.ndarray:
        """
        Normalize signal to zero mean and unit variance.
        
        Args:
            signal_data: Input signal
        
        Returns:
            Normalized signal
        """
        mean = np.mean(signal_data)
        std = np.std(signal_data)
        
        if std == 0:
            return signal_data - mean
        
        return (signal_data - mean) / std
    
    @staticmethod
    def extract_rms(signal_data: np.ndarray, window_size: int = 50) -> np.ndarray:
        """
        Extract Root Mean Square (RMS) features.
        
        Args:
            signal_data: Input signal
            window_size: Size of sliding window
        
        Returns:
            RMS values
        """
        n_windows = len(signal_data) - window_size + 1
        rms = np.zeros(n_windows)
        
        for i in range(n_windows):
            window = signal_data[i:i + window_size]
            rms[i] = np.sqrt(np.mean(window ** 2))
        
        return rms
    
    @staticmethod
    def extract_mav(signal_data: np.ndarray, window_size: int = 50) -> np.ndarray:
        """
        Extract Mean Absolute Value (MAV) features.
        
        Args:
            signal_data: Input signal
            window_size: Size of sliding window
        
        Returns:
            MAV values
        """
        n_windows = len(signal_data) - window_size + 1
        mav = np.zeros(n_windows)
        
        for i in range(n_windows):
            window = signal_data[i:i + window_size]
            mav[i] = np.mean(np.abs(window))
        
        return mav
    
    @staticmethod
    def extract_variance(signal_data: np.ndarray, window_size: int = 50) -> np.ndarray:
        """
        Extract variance features.
        
        Args:
            signal_data: Input signal
            window_size: Size of sliding window
        
        Returns:
            Variance values
        """
        n_windows = len(signal_data) - window_size + 1
        var = np.zeros(n_windows)
        
        for i in range(n_windows):
            window = signal_data[i:i + window_size]
            var[i] = np.var(window)
        
        return var
    
    @staticmethod
    def extract_wl(signal_data: np.ndarray) -> float:
        """
        Extract Waveform Length (WL) feature.
        
        Args:
            signal_data: Input signal
        
        Returns:
            Waveform length value
        """
        return np.sum(np.abs(np.diff(signal_data)))
    
    @staticmethod
    def extract_ssc(signal_data: np.ndarray) -> float:
        """
        Extract Slope Sign Changes (SSC) feature.
        
        Args:
            signal_data: Input signal
        
        Returns:
            Number of slope sign changes
        """
        ssc = 0
        for i in range(1, len(signal_data) - 1):
            if ((signal_data[i] > signal_data[i-1] and signal_data[i] > signal_data[i+1]) or
                (signal_data[i] < signal_data[i-1] and signal_data[i] < signal_data[i+1])):
                ssc += 1
        
        return ssc
    
    def extract_all_features(self, signal_data: np.ndarray, window_size: int = 50) -> np.ndarray:
        """
        Extract all features from signal.
        
        Args:
            signal_data: Input signal (N samples,) or (N samples, n_channels)
            window_size: Window size for sliding window features
        
        Returns:
            Feature vector
        """
        # Handle multi-channel signals
        if signal_data.ndim == 2:
            features = []
            for ch in range(signal_data.shape[1]):
                ch_features = self.extract_all_features(signal_data[:, ch], window_size)
                features.extend(ch_features)
            return np.array(features)
        
        # Filter
        filtered = self.bandpass_filter(signal_data, fs=self.sampling_rate)
        
        # Normalize
        normalized = self.normalize_signal(filtered)
        
        # Extract features
        rms = self.extract_rms(normalized, window_size)
        mav = self.extract_mav(normalized, window_size)
        var = self.extract_variance(normalized, window_size)
        wl = self.extract_wl(normalized)
        ssc = self.extract_ssc(normalized)
        
        # Aggregate features
        features = np.array([
            np.mean(rms), np.std(rms),
            np.mean(mav), np.std(mav),
            np.mean(var), np.std(var),
            wl, ssc
        ])
        
        return features


def process_emg_batch(signals: np.ndarray, 
                     sampling_rate: int = 200) -> np.ndarray:
    """
    Process batch of EMG signals and extract features.
    
    Args:
        signals: Batch of signals of shape (n_samples, n_channels, n_points)
        sampling_rate: Sampling rate in Hz
    
    Returns:
        Feature matrix of shape (n_samples, n_features)
    """
    processor = EMGSignalProcessor(sampling_rate=sampling_rate, 
                                   n_channels=signals.shape[1])
    
    features = []
    for signal_data in signals:
        # Each sample is (n_channels, n_points); extract_all_features expects
        # (n_points, n_channels), so transpose before extracting per channel.
        feature_vector = processor.extract_all_features(signal_data.T)
        features.append(feature_vector)
    
    return np.array(features)


if __name__ == "__main__":
    print("Signal Processing Module")
    print("Import this module for EMG signal processing functions")

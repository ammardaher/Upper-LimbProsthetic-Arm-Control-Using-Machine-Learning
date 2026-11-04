"""Tests for python/signal_processing.py (run with: pytest tests/)."""
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python"))

from signal_processing import EMGSignalProcessor, process_emg_batch  # noqa: E402

FS = 200  # MYO armband sampling rate


def _emg_like(n_points=400, n_channels=8, seed=0):
    rng = np.random.default_rng(seed)
    return rng.standard_normal((n_points, n_channels))


def test_bandpass_default_cutoffs_work_at_myo_rate():
    x = _emg_like()[:, 0]
    y = EMGSignalProcessor.bandpass_filter(x, fs=FS)
    assert y.shape == x.shape
    assert np.all(np.isfinite(y))


def test_bandpass_rejects_cutoff_at_or_above_nyquist():
    x = _emg_like()[:, 0]
    with pytest.raises(ValueError):
        EMGSignalProcessor.bandpass_filter(x, highcut=100, fs=FS)
    with pytest.raises(ValueError):
        EMGSignalProcessor.bandpass_filter(x, lowcut=50, highcut=40, fs=FS)


def test_bandpass_attenuates_out_of_band_tone():
    t = np.arange(2000) / FS
    in_band = np.sin(2 * np.pi * 50 * t)
    low_tone = np.sin(2 * np.pi * 2 * t)
    y = EMGSignalProcessor.bandpass_filter(in_band + low_tone, fs=FS)
    core = slice(200, -200)  # ignore filter edge effects
    assert np.std(y[core] - in_band[core]) < 0.1


def test_normalize_signal_zero_mean_unit_variance():
    x = 3.0 + 5.0 * _emg_like()[:, 0]
    y = EMGSignalProcessor.normalize_signal(x)
    assert abs(np.mean(y)) < 1e-9
    assert abs(np.std(y) - 1.0) < 1e-9


def test_normalize_constant_signal_does_not_divide_by_zero():
    y = EMGSignalProcessor.normalize_signal(np.full(10, 4.0))
    assert np.allclose(y, 0.0)


def test_window_features_match_direct_computation():
    x = np.array([1.0, -2.0, 3.0, -4.0, 5.0])
    assert np.allclose(EMGSignalProcessor.extract_rms(x, window_size=2),
                       [np.sqrt(2.5), np.sqrt(6.5), np.sqrt(12.5), np.sqrt(20.5)])
    assert np.allclose(EMGSignalProcessor.extract_mav(x, window_size=2),
                       [1.5, 2.5, 3.5, 4.5])
    assert np.allclose(EMGSignalProcessor.extract_variance(x, window_size=2),
                       [2.25, 6.25, 12.25, 20.25])


def test_waveform_length_and_slope_sign_changes():
    x = np.array([0.0, 1.0, 0.0, 1.0, 0.0])
    assert EMGSignalProcessor.extract_wl(x) == 4.0
    assert EMGSignalProcessor.extract_ssc(x) == 3


def test_extract_all_features_single_and_multi_channel():
    proc = EMGSignalProcessor(sampling_rate=FS)
    single = proc.extract_all_features(_emg_like()[:, 0])
    assert single.shape == (8,)
    multi = proc.extract_all_features(_emg_like(n_channels=8))
    assert multi.shape == (8 * 8,)
    assert np.all(np.isfinite(multi))


def test_process_emg_batch_shape_is_per_channel():
    # (n_samples, n_channels, n_points), as documented
    batch = np.stack([_emg_like(seed=s).T for s in range(3)])
    feats = process_emg_batch(batch, sampling_rate=FS)
    assert feats.shape == (3, 8 * 8)


def test_process_emg_batch_matches_per_sample_extraction():
    proc = EMGSignalProcessor(sampling_rate=FS)
    sample = _emg_like(seed=7)  # (n_points, n_channels)
    feats = process_emg_batch(sample.T[np.newaxis], sampling_rate=FS)
    assert np.allclose(feats[0], proc.extract_all_features(sample))

import numpy as np
from pyentrp import entropy as ent

def compute_rms(sliding_windows):
    rms_values = np.zeros(len(sliding_windows))
    for i, sliding_window in enumerate(sliding_windows):
        rms_values[i] = np.sqrt(np.mean(sliding_window**2))
    return rms_values

def compute_perm_entropy(sliding_windows, dim, delay):
    perm_entropies = np.zeros(len(sliding_windows))
    for i, x in enumerate(sliding_windows):
        perm_entropies[i] = ent.permutation_entropy(x, order=dim, delay=delay)
    return perm_entropies

def sliding_window(signal, win_size, overlap, fs):
    signal_length = len(signal)
    num_windows = int(np.floor((signal_length - win_size) / overlap)) + 1

    time_vector = np.zeros(num_windows)

    sliding_windows = np.zeros((num_windows, win_size))
    for i in range(num_windows):
        start_idx = i * overlap
        end_idx = start_idx + win_size
        if end_idx > signal_length:
            end_idx = signal_length
        window_data = signal[start_idx:end_idx]
        sliding_windows[i, :len(window_data)] = window_data
        time_vector[i] = (start_idx + end_idx) / (2 * fs)

    return sliding_windows, time_vector
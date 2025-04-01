import numpy as np
np.set_printoptions(suppress=True) # Suppresses e+/- annotation

import os
import matplotlib.pyplot as plt
from utils.signal_data import signal
from utils.rms_permutation_analysis import sliding_window, compute_rms, compute_perm_entropy
signals = {}

# Signal Parameters
fs = 20 # Frequency Sampling The machine used for the EHG data is 20 Hz/s


# Sliding Window Parameters
win_size = 200
overlap = 100

# Permutation Entropy
dim = 3;  # Embedding Dimension
delay = 1; # Time delay


for s_type in os.listdir('data/'):
    s_type_path = f"data/{s_type}/"
    signals[s_type] = []
    for s_file in os.listdir(s_type_path):
        s_file_path = f"data/{s_type}/{s_file}"
        plot_s_file_path = f"figures/{s_type}/{s_file}"
        filename = s_file.split('.')[0]
        s = signal()
        s.load_data(s_file_path) 
        ehg_signal = np.array(s.data['S1']['filter_3'])
        # s.display_info()
        sliding_windows, time_vector = sliding_window(ehg_signal, win_size, overlap, fs)
        rms_values = compute_rms(sliding_windows)
        entropy_signal = compute_perm_entropy(sliding_windows, dim, delay)
        pe_threshold = np.mean(entropy_signal) - 0.5 * np.std(entropy_signal)
        rms_threshold = np.mean(rms_values) + 1.0 * np.std(rms_values)
        
        contractions = (entropy_signal < pe_threshold) & (rms_values > rms_threshold)

        t = np.arange(len(ehg_signal)) / fs  # Create time vector for frequency
    
        plt.figure(figsize=(12, 10))
        
        # 1. Raw Signal Plot
        plt.subplot(4, 1, 1)
        plt.plot(t, ehg_signal, 'b')
        plt.ylabel('Amplitude')
        plt.xlabel('Time (seconds)')
        plt.title(f'PRETERM EHG Signal [{filename}]')
        plt.grid(True)
        
        # 2. RMS Plot
        plt.subplot(4, 1, 2)
        plt.plot(time_vector, rms_values, 'r-', linewidth=1)
        plt.ylabel('RMS')
        plt.xlabel('Time (seconds)')
        plt.title('Root Mean Square (RMS)')
        plt.grid(True)
        
        # 3. Permutation Entropy Plot
        plt.subplot(4, 1, 3)
        plt.plot(time_vector, entropy_signal, 'r-', linewidth=1)
        plt.ylabel('Entropy')
        plt.title(f'Permutation Entropy d={dim}')
        plt.grid(True)
        
        # 4. Contractions Plot
        plt.subplot(4, 1, 4)
        plt.plot(time_vector, contractions, 'b-', linewidth=1)
        plt.title('Contraction Detections')
        plt.xlabel('Time (seconds)')
    
        fig_name = f"figures/{s_type}/{filename}.png"
        plt.tight_layout()  # Prevent label overlap
        plt.savefig(fig_name) # Stores 
        plt.close()



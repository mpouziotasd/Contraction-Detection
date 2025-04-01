import numpy as np
# import plotly.graph_objects as go
import matplotlib.pyplot as plt

class signal:
    def __init__(self):
        """
            When using filtered channels, note that the first and last 180 seconds of the signals 
            should be ignored since these intervals contain transient effects of the filters.

        """
        self.data = {
            "signal_type": "",  # Pre-term  term
            "S1": {
                "unfiltered": [],  # Unfiltered first channel S1
                "filter_1": [],  # Filtered using a 4-pole band-pass Butterworth filter from 0.08Hz to 4Hz
                "filter_2": [],  # Filtered using a 4-pole band-pass Butterworth filter from 0.3Hz to 3Hz
                "filter_3": [],  # Filtered using a 4-pole band-pass Butterworth filter from 0.3Hz to 4Hz
            },
            "S2": {
                "unfiltered": [],  # Unfiltered second channel S2
                "filter_1": [],  # Filtered using a 4-pole band-pass Butterworth filter from 0.08Hz to 4Hz
                "filter_2": [],  # Filtered using a 4-pole band-pass Butterworth filter from 0.3Hz to 3Hz
                "filter_3": [],  # Filtered using a 4-pole band-pass Butterworth filter from 0.3Hz to 4Hz
            },
            "S3": {
                "unfiltered": [],  # Unfiltered third channel S3
                "filter_1": [],  # Filtered using a 4-pole band-pass Butterworth filter from 0.08Hz to 4Hz
                "filter_2": [],  # Filtered using a 4-pole band-pass Butterworth filter from 0.3Hz to 3Hz
                "filter_3": [],  # Filtered using a 4-pole band-pass Butterworth filter from 0.3Hz to 4Hz
            },
        }

    def set_signal_type(self, type):
        self.data['signal_type'] = type

    def load_data(self, s_file_path):
        data = np.loadtxt(s_file_path)
        for row in data:
            self.data['S1']['unfiltered'].append(int(row[1]))
            self.data['S1']['filter_1'].append(int(row[2]))
            self.data['S1']['filter_2'].append(int(row[3]))
            self.data['S1']['filter_3'].append(int(row[4]))

            self.data['S2']['unfiltered'].append(int(row[5]))
            self.data['S2']['filter_1'].append(int(row[6]))
            self.data['S2']['filter_2'].append(int(row[7]))
            self.data['S2']['filter_3'].append(int(row[8]))

            self.data['S3']['unfiltered'].append(int(row[9]))
            self.data['S3']['filter_1'].append(int(row[10]))
            self.data['S3']['filter_2'].append(int(row[11]))
            self.data['S3']['filter_3'].append(int(row[12]))

    
    def plot_signals(self, image_file_path):
        fig = plt.figure(layout='constrained', figsize=(10, 6))
        subfigs = fig.subfigures(1, 2, wspace=0.1)

        axes_unfiltered = subfigs[0].subplots(3, 1)

        for (channel, ax) in zip(['S1', 'S2', 'S3'], axes_unfiltered):
            ax.plot(self.data[channel]['unfiltered'], linewidth=0.5)
            ax.set_ylabel('Amplitude')
            ax.set_title(f'Unfiltered Signal for {channel}', fontsize=10)

        axes_unfiltered[-1].set_xlabel('Time')
        
        axes = subfigs[1].subplots(3, 1)

        for (channel, ax) in zip(['S1', 'S2', 'S3'], axes):
            ax.plot(self.data[channel]['filter_1'], label=f'Filter 1 (0.08-4Hz)', linewidth=0.5)
            ax.plot(self.data[channel]['filter_2'], label=f'Filter 2 (0.3-3Hz)', linewidth=0.5)
            ax.plot(self.data[channel]['filter_3'], label=f'Filter 3 (0.3-4Hz)', linewidth=0.5)
            ax.set_ylabel('Amplitude')
            ax.legend(loc='upper right', fontsize=8)
            ax.set_title(f'Filtered Signals for {channel}', fontsize=10)

        axes[-1].set_xlabel('Time')
        
        
        plt.savefig(image_file_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {image_file_path}")

    # The Bummocks (Unused)
    def display_info(self): # Not Used
        """
        Print the signal data in a readable format.
        """
        print(f"Signal Type: {self.data['signal_type']}")
        for channel, filters in self.data.items():
            if channel != "signal_type":
                print(f"\n{channel}:")
                for filter_type, values in filters.items():
                    print(f"  {filter_type}: {values[:10]}{'...' if len(values) > 10 else ''}")
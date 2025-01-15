import librosa
import numpy as np
import matplotlib.pyplot as plt


filepath = r'C:\Users\a1033\Desktop\Contemporary\susan.flac'
signal, sample_rate = librosa.load(filepath, sr=None)
print(f"length of data: {len(signal)}")
print(f"sample rate of data: {sample_rate}")

# figure
quotient, remainder = divmod(len(signal), sample_rate)

# 定义窗口大小
window_size = 1 * sample_rate  # 例如1秒的窗口
num_windows = len(signal) // window_size

# 合并图像到单张图中
plt.figure(figsize=(15, 10))

for i in range(0, len(signal) // window_size, 10):
# for i in range(num_windows):
    start = i * window_size
    end = start + window_size
    window_data = signal[start:end]

    # plt.subplot(num_windows, 1, i + 1)
    plt.figure(figsize=(10, 4))
    plt.plot(window_data)
    plt.title(f'Window {i + 1}')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()

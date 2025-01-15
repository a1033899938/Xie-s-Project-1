import numpy as np
import matplotlib.pyplot as plt



# 示例信号参数
sampling_rate = 44100
duration = 1.0
n_samples = int(sampling_rate * duration)
t = np.linspace(0, duration, n_samples, endpoint=False)

# 创建一个简单的正弦波信号
frequency = 440
signal = 0.5 * np.sin(2 * np.pi * frequency * t)

# 执行傅里叶变换
fft_result = np.fft.fft(signal)
fft_freqs = np.fft.fftfreq(len(signal), 1 / sampling_rate)

# 计算相位
fft_phase = np.angle(fft_result)

# 只保留正频率部分
half_n = len(fft_freqs) // 2
fft_freqs = fft_freqs[:half_n]
fft_magnitude = np.abs(fft_result)[:half_n]
fft_phase = fft_phase[:half_n]

# 可视化
plt.figure(figsize=(12, 8))

# 幅度谱
plt.subplot(3, 1, 1)
plt.plot(fft_freqs, fft_magnitude)
plt.title('Frequency Domain Magnitude')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')

# 相位谱
plt.subplot(3, 1, 2)
plt.plot(fft_freqs, fft_phase)
plt.title('Frequency Domain Phase')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Phase [Radians]')

# 原始信号
plt.subplot(3, 1, 3)
plt.plot(t[:100], signal[:100])
plt.title('Time Domain Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()

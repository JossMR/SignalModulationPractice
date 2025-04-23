import numpy as np
import matplotlib.pyplot as plt

# Generate binary data
def generate_binary_data(message):
    binary = ''.join(format(ord(c), '08b') for c in message)
    return np.array([int(b) for b in binary])

# ASK modulation
def ask_modulation(binary, frequency, bit_time):
    t = np.linspace(0, len(binary) * bit_time, int(len(binary) * bit_time * 1000))
    carrier = np.sin(2 * np.pi * frequency * t)
    ask_signal = np.repeat(binary, int(bit_time * 1000)) * carrier
    return t, ask_signal

# FSK modulation
def fsk_modulation(binary, f0, f1, bit_time):
    t = np.linspace(0, len(binary) * bit_time, int(len(binary) * bit_time * 1000))
    fsk_signal = np.zeros_like(t)
    for i, bit in enumerate(binary):
        f = f1 if bit == 1 else f0
        fsk_signal[i * int(bit_time * 1000):(i + 1) * int(bit_time * 1000)] = np.sin(2 * np.pi * f * t[i * int(bit_time * 1000):(i + 1) * int(bit_time * 1000)])
    return t, fsk_signal

# PSK modulation
def psk_modulation(binary, frequency, bit_time):
    t = np.linspace(0, len(binary) * bit_time, int(len(binary) * bit_time * 1000))
    carrier = np.sin(2 * np.pi * frequency * t)
    psk_signal = np.copy(carrier)
    for i, bit in enumerate(binary):
        if bit == 0:
            psk_signal[i * int(bit_time * 1000):(i + 1) * int(bit_time * 1000)] *= -1
    return t, psk_signal

# Plot the signals
def plot_signals(binary, bit_time, t, ask_signal, fsk_signal, psk_signal):
    plt.figure(figsize=(12, 6))

    # Binary Signal
    plt.subplot(4, 1, 1)
    t_bin = np.linspace(0, len(binary) * bit_time, len(binary) + 1)
    binary_extended = np.repeat(binary, 2)
    t_bin_extended = np.repeat(t_bin, 2)[1:-1]
    plt.step(t_bin_extended, binary_extended, where='post', color='red', linewidth=0.5)
    plt.title("Binary Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()

    # ASK Modulated Signal
    plt.subplot(4, 1, 2)
    plt.plot(t, ask_signal, color='blue', linewidth=0.5)
    plt.title("ASK Modulated Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()

    # FSK Modulated Signal
    plt.subplot(4, 1, 3)
    plt.plot(t, fsk_signal, color='green', linewidth=0.5)
    plt.title("FSK Modulated Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()

    # PSK Modulated Signal
    plt.subplot(4, 1, 4)
    plt.plot(t, psk_signal, color='magenta', linewidth=0.5)
    plt.title("PSK Modulated Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()

    plt.tight_layout()
    plt.show()

message = "Hello World"
bit_time = 0.01
frequency = 5000
f0 = 2000
f1 = 5000

# Generate binary data
binary = generate_binary_data(message)

# ASK Modulation
t, ask_signal = ask_modulation(binary, frequency, bit_time)

# FSK Modulation
t, fsk_signal = fsk_modulation(binary, f0, f1, bit_time)

# PSK Modulation
t, psk_signal = psk_modulation(binary, frequency, bit_time)

# Plot signals
plot_signals(binary, bit_time, t, ask_signal, fsk_signal, psk_signal)
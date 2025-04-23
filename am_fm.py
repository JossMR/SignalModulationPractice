import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import librosa
import soundfile as sf
import os
import sounddevice as sd

def loadAudio(soundWav):
    # 1. Read file
    try:
        # Read with librosa
        audio, sampleRate = librosa.load(soundWav, sr=None, mono=False)
    except:
        sampleRate, audio = wavfile.read(soundWav)
        if audio.dtype == np.int16:
            audio = audio / 32768.0
        elif audio.dtype == np.int32:
            audio = audio / 2147483648.0
    
    # Convert stereo to mono
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=0)
    
    # Normalize audio after conversion
    audio = audio / np.max(np.abs(audio))
    
    
    # Signal data
    duration = len(audio) / sampleRate
    time = np.linspace(0, duration, len(audio))
    
    print(f"Duración: {duration:.2f} segundos")
    print(f"Número de muestras: {len(audio)}")
    
    return audio, sampleRate, time

# 2. Define the carrier wave
def createCarrier(time, carrierFrequency):
    # Create a sine wave at the specified frequency
    carrier = np.sin(2 * np.pi * carrierFrequency * time) 
    return carrier

# 3. Implement AM modulation
def modularAm(audio, carrier, time):
    # Normalize the audio signal
    normalizedAudio = audio / np.max(np.abs(audio))
    
    factorMod = 0.8
    
    # Add an offset to prevent the signal from being inverted
    signalMod = 1 + factorMod * normalizedAudio
    
    # Modulate the amplitude of the carrier
    amSignal = signalMod * carrier
    
    return amSignal, normalizedAudio

# 4. Implement FM modulation
def modularFm(audio, time, sampleRate, carrierFrequency):
    # Normalize the audio signal
    normalizedAudio = audio / np.max(np.abs(audio))
    
    # FM modulation parameters
    frequencyDeviation = 300  # Hz
    
    sensitivity = 2 * np.pi * frequencyDeviation / sampleRate
    cumulativePhase = np.cumsum(normalizedAudio) * sensitivity
    
    # Generate the FM signal
    fmSignal = np.sin(2 * np.pi * carrierFrequency * time + cumulativePhase)
    
    return fmSignal

# 5. Play audio from the signal
def playSignal(signal, sampleRate):
    print("Reproduciendo señal...")
    sd.play(signal, samplerate=sampleRate)
    sd.wait()  # Wait for playback to finish
    print("Reproducción terminada.")

# Function to display all signals in a single view
def visualizeSignals(normalizedAudio, amSignal, fmSignal, time, sampleRate):
    plt.figure(figsize=(12, 6))
    
    # Original Sign
    plt.subplot(3, 1, 1)
    plt.plot(time, normalizedAudio, color='green', linewidth=1.5)
    plt.title('Señal Original')
    plt.xlabel('tiempo (segundos)')
    plt.ylabel('Amplitud')
    plt.grid(True)
    
    # Am Signal
    plt.subplot(3, 1, 2)
    plt.plot(time, amSignal, color='red', linewidth=1.5)
    plt.title('Señal Modulada AM')
    plt.xlabel('tiempo (segundos)')
    plt.ylabel('Amplitud')
    plt.grid(True)
    
    # Fm Signal
    plt.subplot(3, 1, 3)
    plt.plot(time, fmSignal, color='blue', linewidth=1.5)
    plt.title('Señal Modulada FM')
    plt.xlabel('tiempo (segundos)')
    plt.ylabel('Amplitud')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

# WAV file path
soundWav = "sound.wav"

# Check if the file exists
if not os.path.exists(soundWav):
    print(f"Error: El archivo {soundWav} no existe.")
    exit()

# Load file
audio, sampleRate, time = loadAudio(soundWav)

# Trim the audio
maxDuration = 2
if len(audio) / sampleRate > maxDuration:
    print(f"Recortando audio a {maxDuration} segundos para el análisis.")
    audio = audio[:int(maxDuration * sampleRate)]
    time = time[:int(maxDuration * sampleRate)]

# 2. Define the carrier wave
carrierFrequency = 5
carrier = createCarrier(time, carrierFrequency)

# 3. Implement AM modulation
amSignal, normalizedAudio = modularAm(audio, carrier, time)

# 4. Implement FM modulation
fmSignal = modularFm(audio, time, sampleRate, carrierFrequency)

visualizeSignals(normalizedAudio, amSignal, fmSignal, time, sampleRate)

# Options to play audio
while True:
    print("\nSeleccione una opcion para reproducir:")
    print("1. Señal Original")
    print("2. Señal modulada Am")
    print("3. Señal modulada Fm")
    print("4. Salir")
    option=input("Opcion: ")
    if option == "1":
        playSignal(normalizedAudio, sampleRate)
    elif option == "2":
        playSignal(amSignal, sampleRate)
    elif option == "3":
        playSignal(fmSignal, sampleRate)
    elif option == "4":
        break
        

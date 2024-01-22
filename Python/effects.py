import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import wave
import struct
from scipy.io import wavfile
from IPython.display import Audio

def plot_2D_signal(data, title, xlabel, ylabel, figsize):
    plt.figure(num=None, figsize=figsize, dpi=100, facecolor='w', edgecolor='k')
    t = np.linspace(0., duration, data.shape[0])
    plt.plot(t, data[:, 0], label="Kanal L")
    plt.plot(t, data[:, 1], label="Kanal R")
    plt.legend()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def plot_1D_signal(data, title, xlabel, ylabel, figsize):
    plt.figure(num=None, figsize=figsize, dpi=100, facecolor='w', edgecolor='k')
    t = np.arange(len(data)) / samplerate
    plt.plot(t, data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def sound_file_to_c_array(sound_file_path, output_file_path):
    with wave.open(sound_file_path, 'rb') as wav_file:
       # Read audio data as a list of floats
        audio_data = struct.unpack('<{}h'.format(wav_file.getnframes()), wav_file.readframes(wav_file.getnframes()))

    # Write C header file with the audio data array
    with open(output_file_path, 'w') as header_file:
        header_file.write("#ifndef SOUND_ARRAY_H\n")
        header_file.write("#define SOUND_ARRAY_H\n\n")
        header_file.write("const int sound_wav[] = {")
        header_file.write(', '.join(map(str, audio_data)))
        header_file.write("};\n")
        header_file.write("const unsigned int sound_wav_len = sizeof(sound_wav);\n\n")
        header_file.write("#endif  // SOUND_ARRAY_H\n")

sound_file = './guitar_sound.wav'
samplerate, source_audio = wavfile.read(sound_file)
print(f"Sample rate of audio: {samplerate}Hz")
print(f"Number of channels = {source_audio.shape[1]}")
duration = source_audio.shape[0] / samplerate
print(f"Duration = {duration}s")

plot_2D_signal(source_audio, "Prikaz originalnog audio signala u vremenskom domenu", "Vrijeme [s]", "Amplituda", (20, 5))

left_channel = source_audio[:, 0]
rigth_channel = source_audio[:, 1]
equal_channels = (left_channel == rigth_channel).all()
if equal_channels:
    print("Channels are equal!")
else:
    print("Channels are not equal!")

source_audio_mono = np.array([(x[0] + x[1])//2 for x in source_audio], dtype=np.int16)
wavfile.write("./source_audio_mono.wav", samplerate, source_audio_mono.astype(np.int16))
sound_file_path = './source_audio_mono.wav'
output_file_path = 'sound_array.h'
sound_file_to_c_array(sound_file_path, output_file_path)

delay_time = 0.25
delayed_samples = int(delay_time * samplerate)
gain = .3
delay_audio = np.zeros(len(source_audio_mono))

for i in range(len(source_audio_mono)):
    if(i - delayed_samples) >= 0:
        delayed_value = source_audio_mono[i - delayed_samples]
    else:
        delayed_value = 0
    delay_audio[i] = source_audio_mono[i] + gain * delayed_value

plot_1D_signal(delay_audio, "Audio signal nakon primjene delay efekta","Vrijeme [s]", "Amplituda", (20, 5) )

delayed_output_file = "./delay_effect_pygen.wav"
wavfile.write(delayed_output_file, samplerate, delay_audio.astype(np.int16))

multiple_delay = np.zeros(len(source_audio_mono))

for i in range(len(source_audio_mono)):
    if (i - delayed_samples) >= 0:
        delayed_value = multiple_delay[i - delayed_samples]
    else:
        delayed_value = 0
    multiple_delay[i] = source_audio_mono[i] - gain * delayed_value

plot_1D_signal(delay_audio, "Audio signal nakon primjene visestrukog delay (echo) efekta","Vrijeme [s]", "Amplituda", (20, 5) )

multiple_delay_file = "./multiple_delay_pygen.wav"
wavfile.write(multiple_delay_file, samplerate, multiple_delay.astype(np.int16))

import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import wave
import struct
from scipy.io import wavfile

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
        header_file.write("const unsigned int sound_wav_len = sizeof(sound_wav)/sizeof(int);\n\n")
        header_file.write("#endif \n")

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

compression = np.zeros(len(source_audio_mono))
for i in range(1, len(source_audio_mono)):
    comporession[i] = gain * source_audio_mono[i] + (1 - gain) * compression[i - 1]

plot_1D_signal(compression, "Audio signal nakon primjene compression efekta","Vrijeme [s]", "Amplituda", (20, 5) )
compression_file = "./compression_pygen.wav"
wavfile.write(compression_file, samplerate, compression.astype(np.int16))

threshold = 500
noise_gate = np.zeros(len(source_audio_mono))
noise_gate = np.where(np.abs(source_audio_mono) >= threshold, source_audio_mono, 0)
plot_1D_signal(noise_gate, "Audio signal nakon primjene Noise Gate efekta sa Thresholdom 500","Vrijeme [s]", "Amplituda", (20, 5) )
noise_gate_file = "./noise_gate_pygen.wav"
wavfile.write(noise_gate_file, samplerate, noise_gate.astype(np.int16))

pedal_position = 0.7
volume_pedal = np.zeros(len(source_audio_mono))
for i in range(len(source_audio_mono)):
    volume_pedal[i] = source_audio_mono[i] * pedal_position
plot_1D_signal(volume_pedal, "Audio signal nakon primjene Volume Pedal efekta sa faktorom 0.7","Vrijeme [s]", "Amplituda", (20, 5) )
volume_pedal_file = "./volume_pedal_pygen.wav"
wavfile.write(volume_pedal_file, samplerate, volume_pedal.astype(np.int16))

saturation_factor = 0.5
tape_saturation = np.zeros(len(source_audio_mono))
tape_saturation = np.tanh(source_audio_mono * saturation_factor)
plot_1D_signal(tape_saturation, "Audio signal nakon primjene Tape Saturation efekta sa faktorom saturacije 0.5","Vrijeme [s]", "Amplituda", (20, 5) )
tape_saturation_file = "./tape_saturation_pygen"
wavfile.write(tape_saturation_file, samplerate, tape_saturation.astype(np.int16))

octave_up = np.zeros(len(source_audio_mono))
octave_up = source_audio_mono + gain * np.abs(source_audio_mono)
plot_1D_signal(octave_pedal, "Audio signal nakon primjene Octave Pedal efekta sa faktorom 0.7","Vrijeme [s]", "Amplituda", (20, 5))
octave_up_file = "./octave_up_pygen"
wavfile.write(octave_up_file, samplerate, octave_pedal.astype(np.int16))

envelope_filter = np.zeros(len(source_audio_mono)
envelope = 0.0
alpha = 0.1
dt = 1 / samplerate
for i in range(1, len(source_audio_mono)):
    envelope += alpha * (np.abs(source_audio_mono[i] - envelope) * dt
    envelope_filter[i] = envelope_filter[i - 1] + envelope * dt * source_audio_mono[i]
plot_1D_signal(envelope_filter, "Audio signal nakon primjene Envelope Filter efekta sa faktorom Alfa 0.1","Vrijeme [s]", "Amplituda", (20, 5))
envelope_filter_file = "./envelope_filter_pygen"
wavfile.write(envelope_filter_file, samplerate, envelope_filter.astype(np.int16))

depth = 0.9
flfo = 5.
tremolo = np.zeros(len(source_audio_mono))
def m_function(n):
    return 1 + depth * np.cos(2 * np.pi * flfo / samplerate)
for i in range(len(source_audio_mono)):
    tremolo[i] = source_audio_mono[i] * m_function(i)
plot_1D_signal(tremolo, "Audio signal nakon primjene Tremolo efekta sa faktorom A 0.9 i frekvencije FLO 5 Hz","Vrijeme [s]", "Amplituda", (20, 5))
tremolo_file = "./tremolo_filter_pygen"
wavfile.write(tremolo_file, samplerate, tremolo.astype(np.int16))

Gi = 0.005
Go = 2000.
override = np.zeros(len(source_audio_mono))
for i in range(len(source_audio_mono)):
    x = source_audio_mono[i]
    if Gi * x <= -1:
        override[i] = Go * -2/3
    elif Gi * x >= -1 and Gi * x < 1:
        override[i] = Go * (Go * x - np.power(Gi*x, 3)/3)
    else:
        override[i] = Go * 2/3
plot_1D_signal(override, "Audio signal nakon primjene Override (Soft Clipping) efekta sa faktorima Gi = 0.005 i Go = 2000","Vrijeme [s]", "Amplituda", (20, 5))
override_file = "./override_filter_pygen"
wavfile.write(override_file, samplerate, override.astype(np.int16))

distorsion = np.zeros(len(source_audio_mono))
for i in range(len(source_audio_mono)):
    x = source_audio_mono[i]
    if Gi * x <= -1:
        distorsion[i] = - Go
    elif Gi * x >= -1 and Gi * x < 1:
        distorsion[i] = Go * Gi * x
    else:
        distorsion[i] = Go
plot_1D_signal(distorsion, "Audio signal nakon primjene Distorsion (Hard Clipping) efekta sa faktorima Gi = 0.005 i Go = 2000","Vrijeme [s]", "Amplituda", (20, 5))
distorsion_file = "./distorsion_filter_pygen"
wavfile.write(distorsion_file, samplerate, distorsion.astype(np.int16))
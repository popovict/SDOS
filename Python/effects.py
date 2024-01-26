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

####################################################################################################
# Ucitavanje i prikaz originalnog audio signala
####################################################################################################
sound_file = './guitar_sound.wav'
samplerate, source_audio = wavfile.read(sound_file)
print(f"Sample rate of audio: {samplerate}Hz")
print(f"Number of channels = {source_audio.shape[1]}")
duration = source_audio.shape[0] / samplerate
print(f"Duration = {duration}s")
plot_2D_signal(source_audio, "Prikaz originalnog audio signala u vremenskom domenu", "Vrijeme [s]", "Amplituda", (20, 5))
####################################################################################################
# Generisanje mono signala, eksportovanje .wav fajla, upisivanje u .h fajl 
####################################################################################################
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
####################################################################################################
# Implementacija Delay efekta sa datim parametrima, prikaz, eksportovanje .wav fajla.
# Citanje tekstualnog fajla sa obradjenim odmjercima iz CCES, prikaz, eksportovanje .wav fajla.
# Prikaz signala greske.
####################################################################################################
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

plot_1D_signal(delay_audio, "Audio signal nakon primjene delay efekta","Vrijeme [s]", "Amplituda", (20, 5))
delayed_output_file = "./delay_effect_pygen.wav"
wavfile.write(delayed_output_file, samplerate, delay_audio.astype(np.int16))

file = open("./delayed_signal.txt", "r")
lines = file.readlines()
file.close()
temp = [int(line.strip()) for line in lines]
c_delay = np.array(temp)
plot_1D_signal(c_delay, "Audio signal nakon primjene delay efekta na ADSP-21489 platformi","Vrijeme [s]", "Amplituda", (20, 5))
c_delay_output_file = "./delay_effect_cgen.wav"
wavfile.write(c_delay_output_file, samplerate, c_delay.astype(np.int16))
error_signal = np.abs(delay_audio - c_delay)
plot_1D_signal(error_signal, "Signal greske prilikom primjene Delay efekta","Vrijeme [s]", "Amplituda", (20, 5))
####################################################################################################
# Implementacija Echo (Multiple delay) efekta, prikaz, eksportovanje .wav fajla.
# Citanje tekstualnog fajla sa obradjenim odmjercima iz CCES, prikaz, eksportovanje .wav fajla.
# Prikaz signala greske.
####################################################################################################
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

file = open("./echo_effect.txt", "r")
lines = file.readlines()
file.close()
temp = [int(line.strip()) for line in lines]
c_echo = np.array(temp)
plot_1D_signal(c_echo, "Audio signal nakon primjene visestrukog delay (echo) efekta na ADSP-21489 platformi","Vrijeme [s]", "Amplituda", (20, 5))
c_echo_output_file = "./echo_effect_cgen.wav"
wavfile.write(c_echo_output_file, samplerate, c_echo.astype(np.int16))
error_signal = np.abs(multiple_delay - c_echo)
plot_1D_signal(error_signal, "Signal greske nakon primjene visestrukog Delay (Echo) efekta","Vrijeme [s]", "Amplituda", (20, 5))
####################################################################################################
# Implementacija Compressor efekta, prikaz, eksportovanje .wav fajla.
# Citanje tekstualnog fajla sa obradjenim odmjercima iz CCES, prikaz, eksportovanje .wav fajla.
# Prikaz signala greske.
####################################################################################################
compression = np.zeros(len(source_audio_mono))
for i in range(1, len(source_audio_mono)):
    compression[i] = gain * source_audio_mono[i] + (1 - gain) * compression[i - 1]

plot_1D_signal(compression, "Audio signal nakon primjene Compressor efekta","Vrijeme [s]", "Amplituda", (20, 5) )
compression_file = "./compressor_pygen.wav"
wavfile.write(compression_file, samplerate, compression.astype(np.int16))

file = open("./compressor_effect.txt", "r")
lines = file.readlines()
file.close()
temp = [int(line.strip()) for line in lines]
c_compressor = np.array(temp)
plot_1D_signal(c_compressor, "Audio signal nakon primjene Compressor efekta na ADSP-21489 platformi","Vrijeme [s]", "Amplituda", (20, 5))
c_compressor_output_file = "./compressor_effect_cgen.wav"
wavfile.write(c_compressor_output_file, samplerate, c_compressor.astype(np.int16))
error_signal = np.abs(compression - c_compressor)
plot_1D_signal(error_signal, "Signal greske nakon primjene Compressor efekta","Vrijeme [s]", "Amplituda", (20, 5))
####################################################################################################
# Implementacija Noise Gate efekta, prikaz, eksportovanje .wav fajla.
# Citanje tekstualnog fajla sa obradjenim odmjercima iz CCES, prikaz, eksportovanje .wav fajla.
# Prikaz signala greske.
####################################################################################################
threshold = 500
noise_gate = np.zeros(len(source_audio_mono))
noise_gate = np.where(np.abs(source_audio_mono) >= threshold, source_audio_mono, 0)
plot_1D_signal(noise_gate, "Audio signal nakon primjene Noise Gate efekta sa Thresholdom 500","Vrijeme [s]", "Amplituda", (20, 5) )
noise_gate_file = "./noise_gate_pygen.wav"
wavfile.write(noise_gate_file, samplerate, noise_gate.astype(np.int16))

file = open("./noise_gate_effect.txt", "r")
lines = file.readlines()
file.close()
temp = [int(line.strip()) for line in lines]
c_noise_gate = np.array(temp)
plot_1D_signal(c_noise_gate, "Audio signal nakon primjene Noise Gate efekta na ADSP-21489 platformi","Vrijeme [s]", "Amplituda", (20, 5))
c_noise_gate_output_file = "./noise_gate_cgen.wav"
wavfile.write(c_noise_gate_output_file, samplerate, c_noise_gate.astype(np.int16))
error_signal = np.abs(noise_gate - c_noise_gate)
plot_1D_signal(error_signal, "Signal greske nakon primjene Noise Gate efekta","Vrijeme [s]", "Amplituda", (20, 5))
####################################################################################################
# Implementacija Volume Pedal efekta, prikaz, eksportovanje .wav fajla.
# Citanje tekstualnog fajla sa obradjenim odmjercima iz CCES, prikaz, eksportovanje .wav fajla.
# Prikaz signala greske.
####################################################################################################
pedal_position = 0.7
volume_pedal = np.zeros(len(source_audio_mono))
for i in range(len(source_audio_mono)):
    volume_pedal[i] = source_audio_mono[i] * pedal_position
plot_1D_signal(volume_pedal, "Audio signal nakon primjene Volume Pedal efekta sa faktorom 0.7","Vrijeme [s]", "Amplituda", (20, 5) )
volume_pedal_file = "./volume_pedal_pygen.wav"
wavfile.write(volume_pedal_file, samplerate, volume_pedal.astype(np.int16))

file = open("./volume_pedal_effect.txt", "r")
lines = file.readlines()
file.close()
temp = [int(line.strip()) for line in lines]
c_volume_pedal = np.array(temp)
plot_1D_signal(c_volume_pedal, "Audio signal nakon primjene Volume Pedal efekta na ADSP-21489 platformi","Vrijeme [s]", "Amplituda", (20, 5))
c_volume_pedal_output_file = "./volume_pedal_cgen.wav"
wavfile.write(c_volume_pedal_output_file, samplerate, c_volume_pedal.astype(np.int16))
error_signal = np.abs(volume_pedal - c_volume_pedal)
plot_1D_signal(error_signal, "Signal greske nakon primjene Volume Pedal efekta","Vrijeme [s]", "Amplituda", (20, 5))
####################################################################################################
# Implementacija Tape Saturation efekta, prikaz, eksportovanje .wav fajla.
# Citanje tekstualnog fajla sa obradjenim odmjercima iz CCES, prikaz, eksportovanje .wav fajla.
# Prikaz signala greske.
####################################################################################################
saturation_factor = 0.7
tape_saturation = np.zeros(len(source_audio_mono))
tape_saturation = np.tanh(source_audio_mono * saturation_factor)
normalized_signal = tape_saturation / np.max(np.abs(tape_saturation))
plot_1D_signal(normalized_signal, "Audio signal nakon primjene Tape Saturation efekta sa faktorom saturacije 0.7","Vrijeme [s]", "Amplituda", (20, 5) )
tape_saturation_file = "./tape_saturation_pygen.wav"
wavfile.write(tape_saturation_file, samplerate, (normalized_signal*32767).astype(np.int16))

file = open("./tape_saturation_effect.txt", "r")
lines = file.readlines()
file.close()
temp = [int(line.strip()) for line in lines]
c_tape_saturation = np.array(temp)
normalized_signal_1 = c_tape_saturation / np.max(np.abs(c_tape_saturation))
plot_1D_signal(normalized_signal_1, "Audio signal nakon primjene Tape Saturation efekta na ADSP-21489 platformi","Vrijeme [s]", "Amplituda", (20, 5))
c_tape_saturation_file = "./tape_saturation_cgen.wav"
wavfile.write(c_tape_saturation_file, samplerate, (normalized_signal_1*32767).astype(np.int16))
error_signal = np.abs(normalized_signal - normalized_signal_1)
plot_1D_signal(error_signal, "Signal greske nakon primjene Tape Saturation efekta","Vrijeme [s]", "Amplituda", (20, 5))
####################################################################################################
# Implementacija Octave Up efekta, prikaz, eksportovanje .wav fajla.
# Citanje tekstualnog fajla sa obradjenim odmjercima iz CCES, prikaz, eksportovanje .wav fajla.
# Prikaz signala greske.
####################################################################################################
octave_up = np.zeros(len(source_audio_mono))
octave_up = source_audio_mono + gain * np.abs(source_audio_mono)
plot_1D_signal(octave_up, "Audio signal nakon primjene Octave Pedal efekta sa faktorom 0.7","Vrijeme [s]", "Amplituda", (20, 5))
octave_up_file = "./octave_up_pygen.wav"
wavfile.write(octave_up_file, samplerate, octave_up.astype(np.int16))

file = open("./octave_up_effect.txt", "r")
lines = file.readlines()
file.close()
temp = [int(line.strip()) for line in lines]
c_octave_up = np.array(temp)
plot_1D_signal(c_octave_up, "Audio signal nakon primjene Octave Up efekta na ADSP-21489 platformi","Vrijeme [s]", "Amplituda", (20, 5))
c_octave_up_file = "./octave_up_cgen.wav"
wavfile.write(c_octave_up_file, samplerate, c_octave_up.astype(np.int16))
error_signal = np.abs(octave_up - c_octave_up)
plot_1D_signal(error_signal, "Signal greske nakon primjene Octave Up efekta","Vrijeme [s]", "Amplituda", (20, 5))
####################################################################################################
# Implementacija Envelope Filter efekta, prikaz, eksportovanje .wav fajla.
# Citanje tekstualnog fajla sa obradjenim odmjercima iz CCES, prikaz, eksportovanje .wav fajla.
# Prikaz signala greske.
####################################################################################################
envelope_filter = np.zeros(len(source_audio_mono))
envelope = 0.0
alpha = 0.1
dt = 1 / samplerate
for i in range(1, len(source_audio_mono)):
    envelope += alpha * (np.abs(source_audio_mono[i] - envelope)) * dt
    envelope_filter[i] = envelope_filter[i - 1] + envelope * dt * source_audio_mono[i]
plot_1D_signal(envelope_filter, "Audio signal nakon primjene Envelope Filter efekta sa faktorom Alfa 0.1","Vrijeme [s]", "Amplituda", (20, 5))
envelope_filter_file = "./envelope_filter_pygen.wav"
wavfile.write(envelope_filter_file, samplerate, envelope_filter.astype(np.int16))

file = open("./envelope_filter.txt", "r")
lines = file.readlines()
file.close()
temp = [int(line.strip()) for line in lines]
c_envelope_filter = np.array(temp)
plot_1D_signal(c_envelope_filter, "Audio signal nakon primjene Envelope Filter efekta na ADSP-21489 platformi","Vrijeme [s]", "Amplituda", (20, 5))
c_envelope_filter_output_file = "./envelope_effect_cgen.wav"
wavfile.write(c_envelope_filter_output_file, samplerate, c_envelope_filter.astype(np.int16))
error_signal = np.abs(envelope_filter - c_envelope_filter)
plot_1D_signal(error_signal, "Signal greske nakon primjene Envelope Filter efekta","Vrijeme [s]", "Amplituda", (20, 5))
####################################################################################################
# Implementacija Tremolo efekta, prikaz, eksportovanje .wav fajla.
# Citanje tekstualnog fajla sa obradjenim odmjercima iz CCES, prikaz, eksportovanje .wav fajla.
# Prikaz signala greske.
####################################################################################################
depth = 0.9
flfo = 5.
tremolo = np.zeros(len(source_audio_mono))
def m_function(n):
    return 1 + depth * np.cos(2 * np.pi * n * flfo / samplerate)
for i in range(len(source_audio_mono)):
    tremolo[i] = source_audio_mono[i] * m_function(i)
plot_1D_signal(tremolo, "Audio signal nakon primjene Tremolo efekta sa faktorom A 0.9 i frekvencije FLO 5 Hz","Vrijeme [s]", "Amplituda", (20, 5))
tremolo_file = "./tremolo_filter_pygen.wav"
wavfile.write(tremolo_file, samplerate, tremolo.astype(np.int16))

file = open("./tremolo_effect.txt", "r")
lines = file.readlines()
file.close()
temp = [int(line.strip()) for line in lines]
c_tremolo = np.array(temp)
plot_1D_signal(c_tremolo, "Audio signal nakon primjene Tremolo efekta na ADSP-21489 platformi","Vrijeme [s]", "Amplituda", (20, 5))
c_tremolo_output_file = "./tremolo_effect_cgen.wav"
wavfile.write(c_tremolo_output_file, samplerate, c_tremolo.astype(np.int16))
error_signal = np.abs(tremolo - c_tremolo)
plot_1D_signal(error_signal, "Signal greske nakon primjene Tremolo efekta","Vrijeme [s]", "Amplituda", (20, 5))
####################################################################################################
# Implementacija Override (Soft Clipping) efekta, prikaz, eksportovanje .wav fajla.
# Citanje tekstualnog fajla sa obradjenim odmjercima iz CCES, prikaz, eksportovanje .wav fajla.
# Prikaz signala greske.
####################################################################################################
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
override_file = "./override_filter_pygen.wav"
wavfile.write(override_file, samplerate, override.astype(np.int16))

file = open("./override_effect.txt", "r")
lines = file.readlines()
file.close()
temp = [int(line.strip()) for line in lines]
c_override = np.array(temp)
plot_1D_signal(c_override, "Audio signal nakon primjene Override efekta na ADSP-21489 platformi","Vrijeme [s]", "Amplituda", (20, 5))
c_override_output_file = "./override_effect_cgen.wav"
wavfile.write(c_override_output_file, samplerate, c_override.astype(np.int16))
error_signal = np.abs(override - c_override)
#plot_1D_signal(error_signal, "Signal greske nakon primjene Override efekta","Vrijeme [s]", "Amplituda", (20, 5))
####################################################################################################
# Implementacija Distorsion (Hard Clipping) efekta, prikaz, eksportovanje .wav fajla.
# Citanje tekstualnog fajla sa obradjenim odmjercima iz CCES, prikaz, eksportovanje .wav fajla.
# Prikaz signala greske.
####################################################################################################
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
distorsion_file = "./distorsion_filter_pygen.wav"
wavfile.write(distorsion_file, samplerate, distorsion.astype(np.int16))

file = open("./distorsion_effect.txt", "r")
lines = file.readlines()
file.close()
temp = [int(line.strip()) for line in lines]
c_distorsion = np.array(temp)
plot_1D_signal(c_distorsion, "Audio signal nakon primjene Distorsion efekta na ADSP-21489 platformi","Vrijeme [s]", "Amplituda", (20, 5))
c_distorsion_output_file = "./distorsion_effect_cgen.wav"
wavfile.write(c_distorsion_output_file, samplerate, c_distorsion.astype(np.int16))
error_signal = np.abs(distorsion - c_distorsion)
plot_1D_signal(error_signal, "Signal greske nakon primjene Distorsion efekta","Vrijeme [s]", "Amplituda", (20, 5))
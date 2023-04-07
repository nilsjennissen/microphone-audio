import plotext
import numpy as np
import pyaudio
import struct
import wave
import time
import os
from tkinter import TclError
from audio_get_channels import get_cur_mic
from scipy.fftpack import fft

import matplotlib

def audio_spectrum(num_seconds):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    chunk = 4410
    channels = 1
    fs = 44100
    seconds = num_seconds
    sample_format = pyaudio.paInt16
    filename = os.path.join(script_dir, "audio_output.wav")

    print(f'\n... Recording {seconds} seconds of audio initialized ...\n')

    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    input_device_index=get_cur_mic(),
                    frames_per_buffer=chunk,
                    input=True)


    x = np.arange(0, chunk)
    x_fft = np.linspace(0, fs / 2, chunk // 2 + 1)

    frames = []
    start_time = time.time()

    while time.time() - start_time < seconds:
        plotext.clt()
        plotext.cld()
        plotext.clc()

        data = stream.read(chunk, False)
        frames.append(data)
        data_int = struct.unpack(str(2 * chunk) + 'B', data)
        data_np = np.array(data_int, dtype='b')[::2] + 128

        y_freq = data_np
        spec = fft(data_int)
        y_spec = np.abs(np.fft.rfft(data_int)) / chunk

        # plotext.subplots(2, 1)
        # plotext.subplot(1, 1)
        plotext.plot(x, y_freq, color="white", marker="braille")
        # marker braille, fhd, hd, sd, dot, dollar,euro, bitcoin, at, heart, smile, queen, king,

        plotext.plot_size(200, 15)
        plotext.ylim(0, 300)
        plotext.xlabel(f' {seconds} seconds recording   | Elapsed time: {round(time.time() - start_time, 1)} seconds, Time left: {round(seconds - (time.time() - start_time), 1)} seconds')
        plotext.yfrequency(2)
        plotext.xfrequency(0)
        plotext.xlim(0, 4410)
        plotext.horizontal_line(128, color="red", yside="top")

        # plotext.subplot(2, 1)
        # plotext.plot_size(200, 15)
        # plotext.plot(x_fft, y_spec, color="white", marker="braille")
        # plotext.ylim(0, 1)
        # plotext.xfrequency(2)
        # plotext.yfrequency(2)
        # plotext.xaxes("log")
        plotext.show()


    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    print('\n... Finished recording ...')

audio_spectrum(10)
#!/usr/bin/env python3

import os
import sys
import shutil
import pydub
import wave
import numpy as np
import scipy.fftpack as fft
import scipy.signal as signal

base_path = os.getcwd()
filename = " ".join(sys.argv[1:])
name = filename.split(".")[0]
extension = filename.split(".")[1]
audio = pydub.AudioSegment.from_file(filename, extension)

if os.path.exists("wavs"):
    shutil.rmtree("wavs")
os.mkdir("wavs")  # original music converted to wav and split to mono
wavs_path = os.path.join(base_path, "wavs")
channels = audio.split_to_mono()
if os.path.exists("process"):
    shutil.rmtree("process")
os.mkdir("process")  # unmerged mono wav
process_path = os.path.join(base_path, "process")

os.chdir(os.path.join(base_path, "wavs"))
names = []
for i, e in enumerate(channels):
    unrend_name = f"{name}_{i}.wav"
    names.append(unrend_name)
    rend_path = os.path.join(process_path, unrend_name)

    e.export(unrend_name, format="wav")  # convert channel to wav
    parent: wave.Wave_read = wave.open(unrend_name, "rb")
    open(rend_path, "x")
    ext: wave.Wave_write = wave.open(rend_path, "wb")
    ext.setparams(parent.getparams())  # copy settings from original music
    bits_per_frame = parent.getsampwidth()
    all_bytes = parent.readframes(-1)
    length = len(all_bytes)//bits_per_frame
    array = np.empty(length)
    for i in range(0, length, 1):
        array[i] = int.from_bytes(all_bytes[i*bits_per_frame:(i+1)*bits_per_frame],  # ampletude at this point
                                  byteorder='little',
                                  signed=True)
    array = fft.fft(array)
    array2 = np.empty(length*2, np.complex128)
    for j in range(length):
        array2[j*2] = array[j]
        if j != length-1:
            array2[j*2+1] = (array[j]+array[j+1])/2
    array = np.real(fft.ifft(array2)).astype(int)
    array[array > 2147483647] = 2147483647  # int overflow check
    for i in range(0, length*2, 1):
        ext.writeframesraw(array[i].item().to_bytes(bits_per_frame,
                                                    byteorder='little',
                                                    signed=True))
    ext.close()
processed = []
os.chdir(base_path)
os.chdir("process")
for e in names:
    processed.append(pydub.AudioSegment.from_wav(e))
os.chdir(base_path)
pydub.AudioSegment.from_mono_audiosegments(  # merge processed monos into master
    *processed).export(f"{name}_ext.wav", format="wav")
shutil.rmtree(os.path.join(base_path, "wavs"))
shutil.rmtree(os.path.join(base_path, "process"))

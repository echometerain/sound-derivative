#!/usr/bin/env python3
# put audio file in same directory (eg. hot milk)
# run "./sd.py hot milk.mp3"

import os
import sys
import shutil
import pydub
import wave

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
os.mkdir("process")  # unmerged mono wav derivatives
process_path = os.path.join(base_path, "process")

os.chdir(os.path.join(base_path, "wavs"))
names = []
for i, e in enumerate(channels):
    last_frame = 0
    unrend_name = f"{name}_{i}.wav"
    names.append(unrend_name)
    rend_path = os.path.join(process_path, unrend_name)

    e.export(unrend_name, format="wav")  # convert channel to wav
    parent: wave.Wave_read = wave.open(unrend_name, "rb")
    open(rend_path, "x")
    deri: wave.Wave_write = wave.open(rend_path, "wb")
    deri.setparams(parent.getparams())  # copy settings from original music
    bits_per_frame = parent.getsampwidth()
    all_bytes = parent.readframes(-1)
    for i in range(0, len(all_bytes)-2, bits_per_frame):
        frame = int.from_bytes(all_bytes[i:i+2],  # ampletude at this point
                               byteorder='little',
                               signed=True)
        # get rate of change
        deri.writeframesraw(((frame-last_frame)//2).to_bytes(bits_per_frame,
                                                             byteorder='little',
                                                             signed=True))
        last_frame = frame
    parent.close()
    deri.close()
processed = []
os.chdir(base_path)
os.chdir("process")
for e in names:
    processed.append(pydub.AudioSegment.from_wav(e))
os.chdir(base_path)
pydub.AudioSegment.from_mono_audiosegments(  # merge processed monos into master
    *processed).export(f"{name}_deri.wav", format="wav")
shutil.rmtree(os.path.join(base_path, "wavs"))
shutil.rmtree(os.path.join(base_path, "process"))

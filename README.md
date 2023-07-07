# sound-derivative
some sound experiments

- `sd.py`: takes derivatives of sound (laplace high pass)
  - https://dsp.stackexchange.com/questions/83412/why-does-the-derivative-of-an-audio-file-act-like-a-high-pass-filter
- `ftc_low.py`: appends zero values into the frequency domain at nyquist, resulting in the the signal being stretched, therefore being slowed and pitch shifted down
- `ftc_fade_2x.py`: doubles the amount of values the frequency domain by taking the average of every two values, repeats the signal but introduces a crossfade for some reason 
- `ftc_fade_3x.py`: same thing as `ftc_fade_2x.py` but triples the amount of samples

process wave files by placing them into this dir and then running `python script.py ./filename.wav`

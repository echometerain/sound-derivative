# sound-derivative
some sound experiments

- `sd.py`: takes derivatives of sound (laplace high pass)
- `ftc_low.py`: appends zero values into the frequency domain at nyquist, resulting in the the signal being pitch shifted down
- `ftc_fade.py`: doubles the amount of values the frequency domain by taking the average of every two values, repeats the signal but introduces a crossfade for some reason 

process wave files by placing them into this dir and then running `python script.py ./filename.wav`
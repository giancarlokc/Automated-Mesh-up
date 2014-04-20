import librosa
import numpy as np
from numpy.linalg import norm

n_fft = 4096
hop_length = 1024

src = "/Media/panic-sweat-4s.wav"
paths = ["/Media/protest-hair-4s.wav", "/Media/protest-lavie-4s.wav", "/Media/protest-tandem-4s.wav"]

def mix(src_path, tgt_paths, n_fft = 4096, hop_length = 1024):
  src_signal, sr = librosa.load(src_path)
  src_stft = librosa.stft(src_signal, n_fft, hop_length)
  src_mag, src_phase = librosa.magphase(src_stft)
  targets = {}
  for path in tgt_paths:
    signal, _ = librosa.load(path)
    D_tgt = librosa.stft(signal, n_fft, hop_length)
    tgt_mag, _ = librosa.magphase(D_tgt)
    targets[path] = tgt_mag
  length = len(src_stft[0])
  for i in range(len(src_mag)):
    distance = None
    closest = src_mag[i]*0
    for target in targets.values():
      try:
        cap = min(len(target[i]), length)
        new_dist = norm(target[i][:cap] - src_mag[i][:cap])
        if new_dist < distance or distance == None:
          distance = new_dist
          closest = target[i]
      except IndexError:
        del targets[target]
    maxsrc = max(src_stft[i])
    maxtgt = max(closest)
    src_mag[i][:cap] += closest[:cap]
    src_mag[i][:cap] = maxsrc * src_mag[i][:cap] / (maxsrc+maxtgt)
  signal = librosa.istft(src_mag * src_phase)
  #2*sr to compensate for stereo file?
  librosa.output.write_wav(src_path[:-4]+"-mix.wav", signal, 2*sr)

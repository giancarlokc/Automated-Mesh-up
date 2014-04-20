import librosa
import numpy as np
from numpy.linalg import norm

n_fft = 4096
hop_length = 1024

src_path = "/Media/panic-sweat-4s.wav"
tgt_paths = ["/Media/protest-hair-4s-mono.wav", 
             "/Media/protest-lavie-4s-mono.wav", 
             "/Media/protest-tandem-4s-mono.wav"]

def mix(src_path, tgt_paths, n_fft = 4096, hop_length = 1024):
  #STFT from source
  src_signal, sr = librosa.load(src_path)
  src_stft = librosa.stft(src_signal, n_fft, hop_length)
  src_mag, src_phase = librosa.magphase(src_stft)
  targets = {}
  
  #STFT from paths
  for path in tgt_paths:
    signal, _ = librosa.load(path)
    D_tgt = librosa.stft(signal, n_fft, hop_length)
    tgt_mag, _ = librosa.magphase(D_tgt)
    targets[path] = tgt_mag
  length = len(src_stft[0])
  
  #Compute distances
  for i in range(len(src_mag)):
    print i
    distance = None
    closest = src_mag[i]*0
    for target in targets.values():
      try:
        cap = min(len(target[i]), len(src_mag[i]))
        new_dist = norm(target[i][:cap] - src_mag[i][:cap])
        if new_dist < distance or distance == None:
          distance = new_dist
          closest = target[i]
      except IndexError:
        print 'Target', target
        del targets[target]
    cap = min(len(closest) , len(src_mag[i]))   
    #Avarage of source and target
    """
    print 'cap', len(src_mag[i][:cap])
    print 'mag', len(src_mag[i][:cap])
    print 'cls', len(closest[:cap])
    """

    src_mag[i][:cap] += closest[:cap]
    src_mag[i][:cap] *= 0.5
    
    """
    #Add source and target then scale to source's maximum
    maxsrc = max(src_mag[i])
    maxtgt = max(closest)
    src_mag[i][:cap] += closest[:cap]
    src_mag[i][:cap] = maxsrc * src_mag[i][:cap] / (maxsrc+maxtgt)
    """
  signal = librosa.istft(src_mag * src_phase)
  librosa.output.write_wav(src_path[:-4]+"-mix.wav", signal, 2*sr)
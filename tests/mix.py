import librosa
import numpy as np
from numpy.linalg import norm

n_fft = 4096
hop_length = 1024

src_path = "/Media/panic-sweat-4s.wav"
tgt_path = "/Media/protest-hair-4s-mono.wav"
tgt_paths = ["/Media/protest-hair-4s-mono.wav", 
             "/Media/protest-lavie-4s-mono.wav", 
             "/Media/protest-tandem-4s-mono.wav"]

class Spectra:
  magnitude = None
  phase = None
  sr = None
  def __init__(self, magnitude, phase, sr):
    self.magnitude = magnitude
    self.phase = phase
    self.sr = sr

def mix(src_path, tgt_paths, n_fft = 4096, hop_length = 1024):
  #STFT from source
  src_signal, sr = librosa.load(src_path)
  src_stft = librosa.stft(src_signal, n_fft, hop_length)
  src_mag, src_phase = librosa.magphase(src_stft)
  src_spectra = Spectra(src_mag, src_phase, sr)
  targets = {}
  
  #STFT from paths
  for path in tgt_paths:
    signal, sr = librosa.load(path)
    D_tgt = librosa.stft(signal, n_fft, hop_length)
    tgt_mag, tgt_phase = librosa.magphase(D_tgt)
    tgt_spectra = Spectra(tgt_mag, tgt_phase, sr)
    targets[path] = tgt_spectra    
  length = len(src_stft[0])
  
  #Compute distances
  for i in range(len(src_spectra.magnitude)):
    print i
    distance = None
    closest = src_spectra.magnitude*0
    for target in targets.values():
      try:
        cap = min(len(target.magnitude[i]), len(src_spectra.magnitude[i]))
        new_dist = norm(target.magnitude[i][:cap] - src_mag[i][:cap])
        if new_dist < distance or distance == None:
          distance = new_dist
          closest = target
      except IndexError:
        print 'IDX Error'
    cap = min(len(closest.magnitude[i]) , len(src_mag[i]))   
    #Add magnitudes and phases
    src_spectra.magnitude[i][:cap] += closest.magnitude[i][:cap]  
    src_spectra.phase[i][:cap] += closest.phase[i][:cap]
  #Average magnitudes and phases
  src_spectra.magnitude *= 0.5
  src_spectra.phase *= 0.5  
    
  signal = librosa.istft(src_spectra.magnitude * src_spectra.phase)
  librosa.output.write_wav(src_path[:-4]+"-mix.wav", signal, 2*sr)

def mix_strategies(src, tgt):
  src_signal, sr = librosa.load(src)
  src_stft = librosa.stft(src_signal, n_fft, hop_length)
  src_mag, src_phase = librosa.magphase(src_stft)
  src_spectra = Spectra(src_mag, src_phase, sr)

  tgt_signal, sr = librosa.load(tgt)
  tgt_stft = librosa.stft(tgt_signal, n_fft, hop_length)
  tgt_mag, tgt_phase = librosa.magphase(tgt_stft)
  tgt_spectra = Spectra(tgt_mag, tgt_phase, sr)

  for i in range(len(src_spectra.magnitude)):
    #Average of magnitude and Phase
    cap = min(len(src_spectra.magnitude[i]), len(tgt_spectra.magnitude[i]))
    src_spectra.magnitude[i][:cap] += tgt_spectra.magnitude[i][:cap]  
    src_spectra.phase[i][:cap] += tgt_spectra.phase[i][:cap]

  src_spectra.magnitude *= 0.5
  src_spectra.phase *= 0.5
  new_spectra = src_spectra  
  new_signal = librosa.istft(new_spectra.magnitude * new_spectra.phase)
  librosa.output.write_wav(src[:-4]+"-mix.wav", new_signal, 2*new_spectra.sr)

  """
  #Magnitude spectra average of source and target
  src_mag[i][:cap] += closest[:cap]
  src_mag[i][:cap] *= 0.5
  
  #Add source and target then scale to source's maximum
  maxsrc = max(src_mag[i])
  maxtgt = max(closest)
  src_mag[i][:cap] += closest[:cap]
  src_mag[i][:cap] = maxsrc * src_mag[i][:cap] / (maxsrc+maxtgt)
  
  #Substitute by magnitude of closest spectogram's 
  src_mag[i][:cap] = closest.magnitude[i][:cap]
  src_phase[i][:cap] = closest.phase[i][:cap]
  """


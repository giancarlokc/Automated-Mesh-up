import librosa
import numpy as np
from numpy.linalg import norm
from wrappers import *

n_fft = 4096
hop_length = 1024

src_path = "/Media/stroppa-rub-60s.wav"
tgt_path = "/Media/protest-hair-4s-mono.wav"
tgt_paths = ["/Media/sade-ordinary-40s.wav", 
             "/Media/skrillex-weekends-40s.wav",
             "/Media/unvisage-40s.wav"]

class Sound:
  spectra = None
  chromagram = None
  mfcc = None

  def __init__(self, path):
      self.path = path
      signal, sr = librosa.load(path)      
      self.signal = signal
      self.sr = sr

  def getChromagram(self, n_fft = 4096, hop_length = 1024):
    if self.chromagram == None:      
      if self.spectra == None:
        stft = librosa.stft(self.signal, n_fft, hop_length)
        self.spectra = Spectra(stft, self.sr, n_fft, hop_length)
      self.chromagram = librosa.feature.chromagram(S=self.spectra.getMagnitude())    
    return self.chromagram
  
  def getMfcc(self):
    #IMPLEMENT
    if self.mfcc == None:
      self.mfcc = librosa.feature.mfcc(y=self.signal, sr=self.sr)    
    return self.mfcc
  
  def getSpectra(self, n_fft = 4096, hop_length = 1024):
    if self.spectra == None:
      stft = librosa.stft(self.signal, n_fft, hop_length)
      self.spectra = Spectra(stft, self.sr, n_fft, hop_length)
    elif self.spectra.n_fft != n_fft or self.spectra.hop_length != hop_length:
      stft = librosa.stft(self.signal, n_fft, hop_length)
      return Spectra(stft, self.sr, n_fft, hop_length)
    return self.spectra

class Spectra:
  stft = None
  sr = None
  n_fft = None
  hop_length = None

  def __init__(self, stft, sr, n_fft, hop_length):
    self.stft = stft
    self.sr = sr
    self.n_fft = n_fft
    self.hop_length = hop_length

  def getMagnitude(self, idx = None):
    if idx == None:
      return np.abs(self.stft)
    return np.abs(self.stft[idx])
  
  def getPhase(self, idx = None):
    if idx == None:
      return np.angle(self.stft)
    return np.angle(self.stft[idx])


def mix_by_spectogram(src_path, tgt_paths, n_fft = 4096, hop_length = 1024):
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

def mix_by_chromagram(src_path, tgt_paths, n_fft = 4096, hop_length = 1024):
  print "create source sound"
  src_sound = Sound(src_path)
  targets = {}

  print "create target sounds"
  if isinstance(tgt_paths, list):
    for path in tgt_paths:
      tgt_sound = Sound(tgt_path)
      targets[path] = tgt_sound
  else:
    tgt_sound = Sound(tgt_paths)
    targets[tgt_paths] = tgt_sound

  #zeros chromagram
  zeros = src_sound.getChromagram()[0]*0
  
  #IMPLEMENT cut all arrays such that they have same length!
  print "create temporary magnitude and phase containers"
  tmp_mag = None
  tmp_phase = None

  ratio = len(src_sound.getSpectra().getMagnitude()) / len(src_sound.getChromagram()[0])
  print "block size", ratio

  #Compute distances
  print "compute distances"
  for i in range(len(src_sound.getChromagram()[0]) -1):
    print "computing frame block", i
    distance = None
    closest = zeros
    for target in targets.values():      
      try:
        new_dist = norm(np.transpose(target.getChromagram())[i] - np.transpose(src_sound.getChromagram())[i])
        if new_dist < distance or distance == None:
          distance = new_dist
          closest = target.spectra
      except IndexError:
        print 'IDX Error'
    try:
      cap = min(len(closest.getMagnitude(i)) , len(src_sound.spectra.getMagnitude(i)))
      #Add magnitudes and phases
      for j in range(ratio):
        if tmp_mag == None:
          tmp_mag = src_sound.spectra.getMagnitude(i*ratio + j)[:cap] + closest.getMagnitude(i*ratio+j)[:cap]
          tmp_phase = src_sound.spectra.getPhase(i*ratio +j)[:cap] + closest.getPhase(i*ratio + j)[:cap]
        else: 
          tmp_mag = np.vstack((tmp_mag, src_sound.spectra.getMagnitude(i*ratio +j)[:cap] + closest.getMagnitude(i*ratio+j)[:cap]))
          tmp_phase = np.vstack((tmp_phase, src_sound.spectra.getPhase(i*ratio +j)[:cap] + closest.getPhase(i*ratio + j)[:cap]))    
    except AttributeError:
      print 'Attribute Error'
    
  #Average magnitudes and phases
  tmp_mag *= 0.5
  tmp_phase *= 0.5  
    
  signal = librosa.istft(tmp_mag * tmp_phase)
  librosa.output.write_wav(src_sound.path[:-4]+"-mix.wav", signal, 2*src_sound.sr)


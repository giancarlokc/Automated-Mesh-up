import librosa
import numpy as np
import matplotlib.pyplot as plt

n_fft = 4096
hop_length = 1024

plt.ion()

filepath = "/Media/protest-lavie-4s-harm.wav"
filepath2 = "/Media/protest-lavie-4s.wav"
cmap = plt.cm.jet

def decompose_save(filepath, kernel_size=(7,15), n_fft = 4096, hop_length = 1024):
  signal, sr = librosa.load(filepath)
  D = librosa.stft(signal, n_fft, hop_length)  
  H, P = librosa.decompose.hpss(D, kernel_size=(7,15))
  signal_harm = librosa.istft(H)
  signal_perc = librosa.istft(P)
  librosa.output.write_wav(filepath[:-4]+"-harm.wav", signal_harm, sr)
  librosa.output.write_wav(filepath[:-4]+"-perc.wav", signal_perc, sr)

def decompose(filepath, kernel_size=(7,15), n_fft = 4096, hop_length = 1024):
  signal, sr = librosa.load(filepath)
  D = librosa.stft(signal, n_fft, hop_length)  
  H, P = librosa.decompose.hpss(D, kernel_size=(7,15))
  signal_harm = librosa.istft(H)
  signal_perc = librosa.istft(P)
  return signal_harm, signal_perc

def get_percussive(filepath, kernel_size=(7,15), n_fft = 4096, hop_length = 1024):
  signal, sr = librosa.load(filepath)
  D = librosa.stft(signal, n_fft, hop_length)  
  _, P = librosa.decompose.hpss(D, kernel_size=(7,15))
  signal_perc = librosa.istft(P)  
  return signal_perc

def get_harmonic(filepath, kernel_size=(7,15), n_fft = 4096, hop_length = 1024):
  signal, sr = librosa.load(filepath)
  D = librosa.stft(signal, n_fft, hop_length)  
  H, _ = librosa.decompose.hpss(D, kernel_size=(7,15))
  signal_harm = librosa.istft(H)
  return signal_harm

def pcm2float(sig, dtype=np.float64): 
    sig = np.asarray(sig)
    assert sig.dtype.kind == 'i', "'sig' must be an array of signed integers!"
    dtype = np.dtype(dtype)
    return sig.astype(dtype) / dtype.type(-np.iinfo(sig.dtype).min)

def get_chromagram(filepath, n_fft = 4096, hop_length = 1024):
  signal, sr = librosa.load(filepath)
  D = librosa.stft(signal, n_fft, hop_length)  
  C = librosa.feature.chromagram(S=D)
  return C

def get_chromagram_hpss(filepath, n_fft = 4096, hop_length = 1024, kernel_size=(7,15), downsample=True):
  signal, sr = librosa.load(filepath)
  D = librosa.stft(signal, n_fft, hop_length)  
  C = librosa.feature.chromagram(S=D)
  return C

def plot_chromagram_hpss(filepath, kernel_size=(7,15), n_fft = 4096, hop_length = 1024, downsample=True):
  global cmap
  signal, sr = librosa.load(filepath)
  if downsample:
    signal = librosa.resample(signal, sr, sr/2)
  D = librosa.stft(signal, n_fft, hop_length)
  H, _ = librosa.decompose.hpss(D, kernel_size)
  C = librosa.feature.chromagram(S=H)
  librosa.display.specshow(C, y_axis='chroma', x_axis='time', cmap=cmap)

def plot_chromagram(filepath, n_fft = 4096, hop_length = 1024, win_length=2048):
  global cmap
  signal, sr = librosa.load(filepath)
  D = librosa.stft(signal, n_fft, hop_length)
  C = librosa.feature.chromagram(S=D)
  librosa.display.specshow(C, y_axis='chroma', x_axis='time', cmap=cmap)

def plot_spectrogram(filepath, n_fft = 4096, hop_length = 1024):
  signal, sr = librosa.load(filepath)
  D = np.abs(librosa.stft(signal, n_fft, hop_length))
  librosa.display.specshow(D, sr=sr, y_axis='linear', x_axis='time', cmap=cmap)

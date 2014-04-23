# examples_similarity.py 
# Bregman distance function examples
#
# Copyright (C) 2011 Mike Casey
# Dartmouth College, Hanover, NH
# All Rights Reserved
#

from bregman.suite import *
import os
import os.path
from pylab import *


def ex_1a(x, y, ttl=''):
    """
    Self-similarity matrix of signal x, using CQFT featurs
    """
    p = default_feature_params()
    p['nhop'] = 2205
    p['feature'] = 'mfcc'
    F = Features(x, p) 
    F2 = Features(y, p)
    D = distance.euc_normed(F.X.T,F2.X.T)
    imagesc(D)
    title(ttl)
    return D

def ex_1b(x, ttl=''):
    """
    Self-similarity matrix of signal x, using overlapping stacked CQFT features (shingles)
    """    
    p = default_feature_params()
    p['nhop'] = 2205
    F = Features(x, p)
    X = adb.stack_vectors(F.X.T, 5, 1)
    D = distance.euc_normed(X,X)
    imagesc(D)
    title(ttl)
    return D

def ex_2a(x, ttl=''):
    """
    Self-similarity matrix of signal x, using CHROMA features
    """
    p = default_feature_params()
    p['nhop'] = 2205
    p['feature'] = 'chroma'
    F = Features(x, p) 
    D = distance.euc_normed(F.X.T,F.X.T)
    imagesc(D)
    title(ttl)
    return D

def ex_2b(x, ttl=''):
    """
    Self-similarity matrix of signal x, using overlapping stacked CHROMA features (shingles)
    """    
    p = default_feature_params()
    p['nhop'] = 2205
    p['feature'] = 'chroma'
    F = Features(x, p)
    X = adb.stack_vectors(F.X.T, 5, 1)
    D = distance.euc_normed(X,X)
    imagesc(D)
    title(ttl)
    return D

def ex_3a(x, y, ttl=''):
    """
    Cross similarity matrix of two signals, using CHROMA features
    """
    p = default_feature_params()
    p['nhop'] = 2205
    p['feature'] = 'chroma'
    F = Features(x,p)
    print F.all
    G = Features(y,p)
    D = distance.corr_coeff(F.X.T,G.X.T)
    imagesc(D.T)
    title(ttl)
    xlabel('x vectors')
    ylabel('y vectors')
    return D

if __name__ == "__main__":
#    audio_file_1 = os.path.split(bregman.__file__)[0]+os.sep+'audio'+os.sep+'gmin.wav'
    audio_file_1 = os.path.join(".","george.wav")
    audio_file_2 = os.path.join(".","george.wav")
    x, sr_x, fmt_x = wavread(audio_file_1)
    y, sr_y, fmt_y = wavread(audio_file_2)    
    
#    F = LogFrequencySpectrum(x)
#    F.MFCC # if log cepstrum invoked, contains the MFCC feature matrix
#    print F.sample_rate
#    F.feature_plot(normalize=True)

    ex_1a(x, y, 'Self Similarity Matrix: CQFT')
#    ex_1b(x, 'Self Similarity Matrix: stacked CQFT')

#    ex_2a(x, 'Self Similarity Matrix: CHROMA')
#    ex_2b(x, 'Self Similarity Matrix: stacked CHROMA')

    # Cross similarity examples require a second audio file. 
    # Warp x to create a simulated alternate performance y
#    y = concatenate([resample(x[:len(x)/4], len(x)/4/2),
#                    resample(x[len(x)/4:len(x)/2], len(x)/4),
#                    resample(x[len(x)/2:3*len(x)/4], 2*len(x)/4),
#                     x[3*len(x)/4:]])
    
#    matrixD = ex_3a(x,y, 'Cross Similarity Matrix: CHROMA')
#    raw_input()
#    p, q, D = distance.dtw(matrixD)
#    print p
#    print q
#    imagesc(D.T)
    raw_input()

import numpy as np
import matplotlib.pyplot as plt
import sys, os
from glob2 import glob
import re

def PlotLoss():
    DirName = 'LOSS'
    figall, axall = plt.subplots(2,1)

    for f in glob(os.path.join(DirName, '*.OUT')):
        print(f'Plotting: {f}')
        approx = re.search('BSE-([a-zA-Z]*)-TDA', f)[1]
        orientation = re.search('full\_([a-zA-Z0-9]*)\.OUT', f)[1]
        x = np.genfromtxt(f)
        plt.figure()
        plt.plot(x[:,0], x[:,1], x[:,0], x[:,2])
        plt.legend(['L(Q,$\omega$)', 'S(Q,$\omega$)'])
        plt.title(f)
        plt.xlabel('eV')
        plt.ylabel('L(Q,$\omega$), S(Q,$\omega$)*1000')
        plt.savefig(f+'.png', dpi=300)

        axall[0].plot(x[:,0], x[:,1], '-', label=f'{approx} {orientation} L(Q,$\omega$)')
        axall[1].plot(x[:,0], x[:,2], '-', label=f'{approx} {orientation} S(Q,$\omega$)')

    plt.title('All Sigma')
    axall[1].set_xlabel('eV')
    axall[0].set_ylabel('L(Q,$\omega$)')
    axall[1].set_ylabel('S(Q,$\omega$)')
    axall[0].legend()
    axall[1].legend()
    figall.tight_layout()
    print(f'Plotting: {os.path.join(DirName, "All spectra.png")}')
    figall.savefig(os.path.join(DirName, f'{approx} All spectra.png'), dpi=300)

def PlotSigmas():
    DirName = 'SIGMA'
    figall, axall = plt.subplots(2,1)

    for f in glob(os.path.join(DirName, '*.OUT')):
        print(f'Plotting: {f}')
        approx = re.search('BSE-([a-zA-Z]*)-TDA', f)[1]
        orientation = re.search('full\_([a-zA-Z0-9]*)\.OUT', f)[1]
        x = np.genfromtxt(f)
        plt.figure()
        plt.plot(x[:,0], x[:,1], x[:,0], x[:,2])
        plt.legend(['Real', 'Imag'])
        plt.title(f)
        plt.xlabel('eV')
        plt.ylabel('$\sigma$')
        plt.savefig(f+'.png', dpi=300)

        axall[0].plot(x[:,0], x[:,1], '-', label=f'{approx} {orientation} Real')
        axall[1].plot(x[:,0], x[:,2], '-', label=f'{approx} {orientation} Imag')

    plt.title('All Sigma')
    axall[1].set_xlabel('eV')
    axall[0].set_ylabel('Re($\sigma$)')
    axall[1].set_ylabel('Im($\sigma$)')
    axall[0].legend()
    axall[1].legend()
    figall.tight_layout()
    print(f'Plotting: {os.path.join(DirName, "All spectra.png")}')
    figall.savefig(os.path.join(DirName, f'{approx} All spectra.png'), dpi=300)

def PlotEpsilon():
    DirName = 'EPSILON'
    figall, axall = plt.subplots(2,1)

    for f in glob(os.path.join(DirName, '*.OUT')):
        print(f'Plotting: {f}')
        approx = re.search('BSE-([a-zA-Z]*)-TDA', f)[1]
        orientation = re.search('full\_([a-zA-Z0-9]*)\.OUT', f)[1]
        x = np.genfromtxt(f)
        plt.figure()
        plt.plot(x[:,0], x[:,1]-1, x[:,0], x[:,2])
        plt.legend(['Re($\epsilon$)-1', 'Im($\epsilon$)'])
        plt.title(f)
        plt.xlabel('eV')
        plt.ylabel('$\epsilon$')
        plt.savefig(f+'.png', dpi=300)

        axall[0].plot(x[:,0], x[:,1]-1, '-', label=f'{approx} {orientation} Real')
        axall[1].plot(x[:,0], x[:,2], '-', label=f'{approx} {orientation} Imag')

    plt.title('All Sigma')
    axall[1].set_xlabel('eV')
    axall[0].set_ylabel('Re($\epsilon$)-1')
    axall[1].set_ylabel('Im($\epsilon$)')
    axall[0].legend()
    axall[1].legend()
    figall.tight_layout()
    print(f'Plotting: {os.path.join(DirName, "All spectra.png")}')
    figall.savefig(os.path.join(DirName, f'{approx} All spectra.png'), dpi=300)

if __name__ == '__main__':
    PlotSigmas() 
    PlotLoss() 
    PlotEpsilon() 

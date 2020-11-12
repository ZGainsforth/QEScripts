import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os

s = np.genfromtxt('Fe.out.socabs.dat')
a = np.genfromtxt('FeAtomicLiterature.csv', delimiter=',')
a[:,1] -= np.min(a[:,1])
a[:,1] /= np.max(a[:,1])
a[:,1] *= np.max(s[:,1])

scalefac = st.slider('Multiply theory energy axis by:', 0.95, 1.05, 1.00, 0.0001)
addfac = st.slider('Add eV to teory energy axis by:', -10.0, 10.0, 0.0, 0.1)

fig = plt.figure()
plt.plot(a[:,0], a[:,1], label='Experimental')
plt.plot(s[:,0]*scalefac+addfac, s[:,1], label='DFT/ROCIS isotropic')
plt.plot(s[:,0]*scalefac+addfac, s[:,2], label='DFT/ROCIS x')
plt.plot(s[:,0]*scalefac+addfac, s[:,3], label='DFT/ROCIS y')
plt.plot(s[:,0]*scalefac+addfac, s[:,4], label='DFT/ROCIS z')
plt.xlim(700,730)
plt.legend()
st.write(fig)

if st.button("rerun"):
    st.experimental_rerun()

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os

RefSpec = True
Mode = "singlet"

s11 = np.genfromtxt(os.path.join(f'EPSILON', f'EPSILON_BSE-{Mode}-TDA-BAR_SCR-full_OC11.OUT'), skip_header=18)
s22 = np.genfromtxt(os.path.join(f'EPSILON', f'EPSILON_BSE-{Mode}-TDA-BAR_SCR-full_OC22.OUT'), skip_header=18)
s33 = np.genfromtxt(os.path.join(f'EPSILON', f'EPSILON_BSE-{Mode}-TDA-BAR_SCR-full_OC33.OUT'), skip_header=18)
s = s11.copy()
s[:,2] += s22[:,2]
s[:,2] += s33[:,2]

if RefSpec:
    a = np.genfromtxt('CO2 TIY.txt', delimiter=',')
    a[:,1] -= np.min(a[:,1])
    a[:,1] /= np.max(a[:,1])
    a[:,1] *= np.max(s[:,2])

scalefac = st.slider('Multiple BSE energy axis by:', 1.01, 1.1, 1.035, 0.0002)

fig = plt.figure()
plt.plot(s[:,0]*scalefac, s[:,2], label='bse')
if RefSpec:
    plt.plot(a[:,0], a[:,1], label='exp')
# plt.xlim(700,730)
plt.legend()
st.write(fig)

if st.button("rerun"):
    st.experimental_rerun()

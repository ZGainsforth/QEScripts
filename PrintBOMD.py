import argparse
import numpy as np
import matplotlib.pyplot as plt
import re
import time
import streamlit as st
import glob2 as glob
import pandas as pd
import plotly.express as px

def GetTimeSteps(OutFileText):
    Steps = re.findall(r'iteration\s*=\s*([0-9]+)', OutFileText)
    Times = re.findall(r'time\s*=\s*([0-9.]*) pico-seconds', OutFileText)
    Steps = np.array(Steps).astype(int)
    Times = np.array(Times).astype(float)
    return(Steps, Times)

def GetTempsAndEnergies(OutFileText):
    Ekin = re.findall(r'kinetic energy \(Ekin\)\s*=\s*([0-9.]*) Ry', OutFileText)
    Temps = re.findall(r'temperature\s*=\s*([0-9.]*) K', OutFileText)
    E = re.findall(r'Ekin \+ Etot \(const\)\s*=\s*([0-9.-]*) Ry', OutFileText)
    # Return Temps, E, Ekin, note that the temperature string also occurs at the start, so skip the first.
    return np.array(Temps).astype(float)[1:], np.array(E).astype(float), np.array(Ekin).astype(float)

def GetPressures(OutFileText):
    Pressures = re.findall(r'P=\s*([0-9.-]*)', OutFileText)
    return np.array(Pressures).astype(float)

OutFileList = glob.glob('*.out')
OutputFile = st.selectbox('Molecular Dynamics Output File:', OutFileList)

# print(f'Loading {args.OutputFile}')
with open(OutputFile, 'r') as f:
    OutFileText = f.read()

# Get all the data as numpy arrays from the molecular dynamics output file that we may want to plot.
Steps, Times = GetTimeSteps(OutFileText)
Temps, Etot, Ekin = GetTempsAndEnergies(OutFileText)
Pressures = GetPressures(OutFileText)

st.write(f'Total Number of steps completed: {Steps[-1]}')

# Also, give the total CPU time and time/step.
CPUTimes = re.findall(r'total cpu time spent up to now is\s*([0-9.]*) secs', OutFileText)
st.write(f'Total CPU time spent: {CPUTimes[-1]}')
st.write(f'CPU time per step: {float(CPUTimes[-1])/Steps[-1]:0.2f} seconds or {3600/(float(CPUTimes[-1])/Steps[-1]):0.2f} steps/hour.')

print(Steps, Times, Temps, Etot, Ekin, Pressures)

Data = pd.DataFrame({'Steps': Steps, 'Times': Times, 'Temps': Temps, 'Etot': Etot, 'Ekin': Ekin, 'Pressures': Pressures})
Data.set_index('Times')

# st.line_chart(Data['Temps'])
st.write(px.line(Data, x='Times', y='Temps', labels={'Times':'Picoseconds', 'Temps':'Kelvin'}, title='Temperature'))
st.write(px.line(Data, x='Times', y='Pressures', labels={'Times':'Picoseconds', 'Pressures':'kbar'}, title='Pressure'))
st.write(px.line(Data, x='Times', y='Etot', labels={'Times':'Picoseconds', 'Etot':'Rydberg'}, title='Total Energy (Etot)'))


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
    TimeSteps = re.findall(r'it =\s*([0-9]+)\s*time =\s*([0-9.]*) pico-seconds', OutFileText)
    (Steps, Times) = zip(*TimeSteps)
    Steps = np.array(Steps).astype(int)
    Times = np.array(Times).astype(float)
    return(Steps, Times)

def GetTempsAndEnergies(OutFileText):
    # TempsAndEnergies = re.findall(r'Ekin =\s*([0-9.]*) Ry\s*T =\s*([0-9.]) K\s*Etot =\s*([0-9.]*)', OutFileText)
    TempsAndEnergies = re.findall(r'Ekin =\s*([0-9.]*) Ry\s*T =\s*([0-9.]*) K\s*Etot =\s*([0-9.-]*)', OutFileText)
    TempsAndEnergies = np.array(TempsAndEnergies).astype(float)
    # Return Temps, Etot, Ekin
    return TempsAndEnergies[:,1], TempsAndEnergies[:,2], TempsAndEnergies[:,0]

def GetPressures(OutFileText):
    Pressures = re.findall(r'P=\s*([0-9.-]*)', OutFileText)
    return np.array(Pressures).astype(float)

# parser = argparse.ArgumentParser("Print results of pw.x Born-Oppenheimer molecular dynamics run.")
# parser.add_argument("OutputFile", type=str, help="Name of the .out file from the MD simulation.")
# args = parser.parse_args()

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

Data = pd.DataFrame({'Steps': Steps, 'Times': Times, 'Temps': Temps, 'Etot': Etot, 'Ekin': Ekin, 'Pressures': Pressures})
Data.set_index('Times')

# st.line_chart(Data['Temps'])
st.write(px.line(Data, x='Times', y='Temps'))
st.write(px.line(Data, x='Times', y='Pressures'))
st.write(px.line(Data, x='Times', y='Etot'))

time.sleep(1)
print('rerunning')
st.ScriptRunner.RerunException(st.ScriptRequestQueue.RerunData(None))

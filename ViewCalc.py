import os
import numpy as np
import matplotlib.pyplot as plt
import re
from io import StringIO

def GetChunkFromTextFile(FileName, StartStr, StopStr, skip_header=0, skip_footer=0, LastHit=True, DataType='array'):
    # DataType means we can extract the chunk and then turn it into:
    # 1) Numpy table 'numpy'
    # 2) return the raw text 'raw'
    DataType = DataType.lower()

    # Read the file.
    try:
        with open(FileName, 'r') as myfile:
            data = myfile.read()
    except:
        print('Failed to open ' + FileName + '.  Skipping.')
        return

    # This regex looks for the data between the start and top strings.
    reout = re.compile('%s(.*?)%s' % (StartStr, StopStr), re.S)
    try:
        # Extract just the data we want.
        if LastHit == False:
            SectionStr = reout.search(data).group(1)
        else:
            SectionStr = reout.findall(data)[-1]
    except:
        # It is possible that the user asked for something that isn't in the file.  If so, just bail.
        return None

    if DataType == 'raw':
        # Now apply skip_header and skip_footer
        SectionData = SectionStr
        SectionData = ''.join(SectionData.splitlines(True)[skip_header:])
        if skip_footer > 0:
            SectionData = ''.join(SectionData.splitlines(True)[:-skip_footer])

    if DataType == 'float':
        SectionData = np.float(SectionStr)

    if DataType == 'array':
        # Convert it into a numpy array.
        SectionData = np.genfromtxt(StringIO(SectionStr), skip_header=skip_header, skip_footer=skip_footer, dtype=None)

    return SectionData


def GenerateSingleSummary(InFilebase):
    # Get the base file names.
    with open(os.path.join('CalcSummaries', InFilebase + '-BaseNames.txt'), 'r') as f:
        BaseNames = [b.strip() for b in f.readlines()]

    # Get the X-axis labels.
    with open(os.path.join('CalcSummaries', InFilebase + '-XVary.txt'), 'r') as f:
        # The first line is the header.
        XLabelType = f.readline().strip()
        XLabels = [b.strip() for b in f.readlines()]

    # Let's get the energy, forces and runtimes out of each of the files.
    Energies = np.zeros(len(BaseNames))
    Forces = np.copy(Energies)
    RunTimes = np.copy(Energies)
    for n, FileName in enumerate(BaseNames):
        try:
            Energies[n] = GetChunkFromTextFile(FileName=FileName + '.out', StartStr='!\s*total energy\s*=\s*', StopStr=' Ry', DataType='float')
            Forces[n] = GetChunkFromTextFile(FileName=FileName + '.out', StartStr='Total force =\s*', StopStr='\s*Total SCF correction', DataType='float')
        except:
            # Sometimes there will be a failed computation.  If so, we leave it out.
            Energies[n] = np.nan
            Forces[n] = np.nan

        try:
            RunTime = GetChunkFromTextFile(FileName=FileName + '.out', StartStr='PWSCF\s*:\s*', StopStr='s CPU', DataType='raw')
            RunTime = 0
        except:
            RunTimes[n] = np.nan

    # Save two column files for each.
    np.savetxt(os.path.join('CalcSummaries', InFilebase + '-Energies.txt'), np.vstack((XLabels, Energies.astype('|S32'))).T, header=XLabelType + ' Rydbergs', fmt='%s %s')
    np.savetxt(os.path.join('CalcSummaries', InFilebase + '-Forces.txt'), np.vstack((XLabels, Forces.astype('|S32'))).T, header=XLabelType + ' Rybergs/Bohr', fmt='%s %s')
    np.savetxt(os.path.join('CalcSummaries', InFilebase + '-RunTimes.txt'), np.vstack((XLabels, RunTimes.astype('|S32'))).T, header=XLabelType + ' Seconds', fmt='%s %s')

    # Return all the obtained data.
    SingleSummary = dict()
    SingleSummary['InFile'] = InFilebase
    SingleSummary['BaseNames'] = BaseNames
    SingleSummary['XLabelType'] = XLabelType
    SingleSummary['XLabels'] = XLabels
    SingleSummary['Energies'] = Energies
    SingleSummary['Forces'] = Forces
    SingleSummary['RunTimes'] = RunTimes

    return SingleSummary


def PlotSummary(Summary, prefix=''):
    XTicks = Summary['XLabels']
    X = range(len(Summary['Energies']))

    # Plot the energy convergence.
    plt.figure()
    E = Summary['Energies']
    plt.plot(X, E)
    plt.xlabel(Summary['XLabelType'])
    plt.ylabel('Rydbergs')
    plt.xticks(X, XTicks)
    plt.title(prefix + 'Energies')

    # Plot force
    plt.figure()
    F = Summary['Forces']
    plt.plot(X, F)
    plt.xlabel(Summary['XLabelType'])
    plt.ylabel('Rydbergs per Bohr')
    plt.xticks(X, XTicks)
    plt.title(prefix + 'Forces')

    # Plot Time
    plt.figure()
    T = Summary['RunTimes']
    plt.plot(X, T)
    plt.xlabel(Summary['XLabelType'])
    plt.ylabel('seconds')
    plt.xticks(X, XTicks)
    plt.title(prefix + 'Run Time')


def CalcSummary():
    # Get the base file names.  If there is only one, then we will plot it.  If there are two, then we are doing differential convergence.
    with open(os.path.join('CalcSummaries', 'BaseNames.txt'), 'r') as f:
        InFile1 = f.readline().strip()
        try:
            InFile2 = f.readline().strip()
        except:
            InFile2 = None
        if InFile2 == '':
            # For some reason, even though the file has only one line, it returns a second blank line...
            InFile2 = None

    # Now Generate summaries from each
    Summary1 = GenerateSingleSummary(InFile1)
    if InFile2 is None:
        # If there is only one summary, then we plot it.
        PlotSummary(Summary1, prefix=InFile1 + ' ')
    else:
        # Otherwise, with two summaries, we have to plot the differential.
        Summary2 = GenerateSingleSummary(InFile2)

        # If there is a second summary, then this is a differential comparison.  Produce plots of the first minus the second.
        Energies = Summary1['Energies'] - Summary2['Energies']
        Forces = Summary1['Forces'] - Summary2['Forces']
        RunTimes = Summary1['RunTimes'] - Summary2['RunTimes']
        XLabels = [x1 + '-' + x2 for x1, x2 in zip(Summary1['XLabels'], Summary2['XLabels'])]
        BaseName = Summary1['InFile'] + '-minus-' + Summary2['InFile']
        XLabelType = Summary1['XLabelType']

        # Save two column files for each.
        np.savetxt(os.path.join('CalcSummaries', BaseName + '-Energies.txt'), np.vstack((XLabels, Energies.astype('|S32'))).T, header=XLabelType + ' Rydbergs', fmt='%s %s')
        np.savetxt(os.path.join('CalcSummaries', BaseName + '-Forces.txt'), np.vstack((XLabels, Forces.astype('|S32'))).T, header=XLabelType + ' Rybergs/Bohr', fmt='%s %s')
        np.savetxt(os.path.join('CalcSummaries', BaseName + '-RunTimes.txt'), np.vstack((XLabels, RunTimes.astype('|S32'))).T, header=XLabelType + ' Seconds', fmt='%s %s')

        DiffSummary = dict()
        DiffSummary['InFile'] = BaseName
        DiffSummary['XLabelType'] = XLabelType
        DiffSummary['XLabels'] = XLabels
        DiffSummary['Energies'] = Energies
        DiffSummary['Forces'] = Forces
        DiffSummary['RunTimes'] = RunTimes

        PlotSummary(Summary1, prefix=InFile1 + ' ')
        PlotSummary(Summary2, prefix=InFile2 + ' ')
        PlotSummary(DiffSummary, prefix='Differential ')

    plt.show()

    return


if __name__ == '__main__':
    CalcSummary()

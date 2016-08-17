import os


def Convergekgrid(InFile1=None, kGrid1=[1, 1, 1], InFile2=None, kGrid2=None, kGridMultipliers=range(1, 3)):
    """ InFile1 and 2 should have a format like 'spinel.1.in.  1 and 2 indicate the we are looking for differential convergence.
        if InFile2 is empty, then we only converge on InFile1.
        kGrid is the starting kgrid.  kGridMultipliers will give several more kgrids to check convergence.
        """

    # Each step in the convergence has a file which describes the source in file and what k-grid we are on.
    basenamestr = '%s-convergek-%d,%d,%d'

    # This is the substitution we do to edit the kgrid for each file.
    sedstr = "sed -e 's/x x x 0 0 0/%d %d %d 0 0 0/' -e 's/calcdir/%s/' %s > %s.in"

    # This is the str to run pw.x.
    pwstr = 'pw.x < %s.in > %s.out\n'

    # This is the string which will contain all the pw.x commands to run.
    RunStr = list()

    # XVary contains x-axis values for plotting results.  The varied parameter.  We need one for each infile.
    XVaryStr1 = list()
    XVaryStr2 = list()

    # And in case the plotter wants to crawl results, then the root file name lists, for 1 and 2.
    BaseNamesStr1 = list()
    BaseNamesStr2 = list()

    # The in filenames without the .in extension.
    InFile1noext, _ = os.path.splitext(InFile1)
    InFile2noext, _ = os.path.splitext(InFile2)

    for n in range(len(kGridMultipliers)):
        k = [kGrid1[0] * kGridMultipliers[n], kGrid1[1] * kGridMultipliers[n], kGrid1[2] * kGridMultipliers[n]]

        # Make the unique name which is used for the .in, .out and for the data directory for this calculation.
        BaseName1 = basenamestr % (InFile1noext, k[0], k[1], k[2])
        BaseNamesStr1.append(BaseName1)

        # Add the x-axis labels for later plots.
        XVaryStr1.append('%d,%d,%d' % (k[0], k[1], k[2]))

        # sed on first file.
        os.system(sedstr % (k[0], k[1], k[2], BaseName1, InFile1, BaseName1))
        RunStr.append(pwstr % (BaseName1, BaseName1))

        if InFile2 is not None:
            k = [kGrid2[0] * kGridMultipliers[n], kGrid2[1] * kGridMultipliers[n], kGrid2[2] * kGridMultipliers[n]]
            BaseName2 = basenamestr % (InFile2noext, k[0], k[1], k[2])
            BaseNamesStr2.append(BaseName2)
            XVaryStr2.append('%d,%d,%d' % (k[0], k[1], k[2]))
            os.system(sedstr % (k[0], k[1], k[2], BaseName2, InFile2, BaseName2))
            RunStr.append(pwstr % (BaseName2, BaseName2))

    # Make a bash script that the user can use to run this.
    with open('runpw', 'w') as f:
        f.write('#!/bin/bash\n')
        f.write(''.join(RunStr))
    os.system('chmod +x runpw')

    # Write files which allow easier plotting and viewing later.
    try:
        os.mkdir('CalcSummaries')
    except:
        pass
    with open(os.path.join('CalcSummaries', InFile1noext + '-XVary.txt'), 'w') as f:
        f.write('k-grid\n')
        f.write('\n'.join(XVaryStr1))
    with open(os.path.join('CalcSummaries', InFile1noext + '-BaseNames.txt'), 'w') as f:
        f.write('\n'.join(BaseNamesStr1))

    if InFile2 is not None:
        with open(os.path.join('CalcSummaries', InFile2noext + '-XVary.txt'), 'w') as f:
            f.write('k-grid\n')
            f.write('\n'.join(XVaryStr2))
        with open(os.path.join('CalcSummaries', InFile2noext + '-BaseNames.txt'), 'w') as f:
            f.write('\n'.join(BaseNamesStr2))

    # Finally, write infile 1 and 2 to a basenames file so this can always be read automatically.
    with open(os.path.join('CalcSummaries', 'BaseNames.txt'), 'w') as f:
        f.write(InFile1noext)
        if InFile2 is not None:
            f.write('\n')
            f.write(InFile2noext)

    # Print results for the user.
    print "kpoint convergence set written.  Run 'runpw' to run all simulations.  Run python ViewCalc.py to view results after.\n"


def ConvergeParameter(InFile1=None, ReplaceStr='', ReplaceFormatStr=None, ReplaceLabel='', ConvergenceName='', ReplaceVals1=None, InFile2=None, ReplaceVals2=None):
    """ InFile1 and 2 should have a format like 'spinel.1.in.  1 and 2 indicate the we are looking for differential convergence.
        if InFile2 is empty, then we only converge on InFile1.
        ReplaceStr is the string that sed will use to replace values.
        ReplaceLabel is a description which goes onto the xlabel of the plots later.
        ReplaceFormatStr is just the formatting string so we can place it in filenames and such.
        ConvergenceName is like title for this calculation, which also goes in filenames, etc.
        ReplaceVals is a list of values or a list of list of values for each replacement
        """

    # This is the substitution we do to edit the kgrid for each file.
    sedstr = "sed -e '" + ReplaceStr + "' -e 's/calcdir/%s/' %s > %s.in"

    # This is the str to run pw.x.
    pwstr = 'echo %s\npw.x < %s.in > %s.out\n'

    # This is the string which will contain all the pw.x commands to run.
    RunStr = list()

    # XVary contains x-axis values for plotting results.  The varied parameter.  We need one for each infile.
    XVaryStr1 = list()
    XVaryStr2 = list()

    # And in case the plotter wants to crawl results, then the root file name lists, for 1 and 2.
    BaseNamesStr1 = list()
    BaseNamesStr2 = list()

    # The in filenames without the .in extension.
    InFile1noext, _ = os.path.splitext(InFile1)
    if InFile2 is not None:
        InFile2noext, _ = os.path.splitext(InFile2)

    for n in range(len(ReplaceVals1)):
        Vals = ReplaceVals1[n]

        # Make the unique name which is used for the .in, .out and for the data directory for this calculation.
        BaseName1 = '%s-' + ConvergenceName + '-' + ReplaceFormatStr
        BaseName1Vals = (InFile1noext,) + (Vals,)
        BaseName1 = BaseName1 % BaseName1Vals
        BaseNamesStr1.append(BaseName1)

        # Add the x-axis labels for later plots.
        XVaryStr1.append(ReplaceFormatStr % Vals)

        # sed on first file.
        os.system(sedstr % ((Vals,) + (BaseName1, InFile1, BaseName1)))
        RunStr.append(pwstr % (BaseName1, BaseName1, BaseName1))

        if InFile2 is not None:
            Vals = ReplaceVals2[n]
            BaseName2 = '%s-' + ConvergenceName + '-' + ReplaceFormatStr
            BaseName2Vals = (InFile2noext,) + (Vals,)
            BaseName2 = BaseName1 % BaseName2Vals
            BaseNamesStr2.append(BaseName2)
            XVaryStr1.append(ReplaceFormatStr % Vals)
            os.system((sedstr % (Vals,) + (BaseName2, InFile2, BaseName2)))
            RunStr.append(pwstr % (BaseName2, BaseName2, BaseName2))

    # Make a bash script that the user can use to run this.
    with open('runpw', 'w') as f:
        f.write('#!/bin/bash\n')
        f.write(''.join(RunStr))
    os.system('chmod +x runpw')

    # Write files which allow easier plotting and viewing later.
    try:
        os.mkdir('CalcSummaries')
    except:
        pass
    with open(os.path.join('CalcSummaries', InFile1noext + '-XVary.txt'), 'w') as f:
        f.write(ReplaceLabel + '\n')
        f.write('\n'.join(XVaryStr1))
    with open(os.path.join('CalcSummaries', InFile1noext + '-BaseNames.txt'), 'w') as f:
        f.write('\n'.join(BaseNamesStr1))

    if InFile2 is not None:
        with open(os.path.join('CalcSummaries', InFile2noext + '-XVary.txt'), 'w') as f:
            f.write(ReplaceLabel + '\n')
            f.write('\n'.join(XVaryStr2))
        with open(os.path.join('CalcSummaries', InFile2noext + '-BaseNames.txt'), 'w') as f:
            f.write('\n'.join(BaseNamesStr2))

    # Finally, write infile 1 and 2 to a basenames file so this can always be read automatically.
    with open(os.path.join('CalcSummaries', 'BaseNames.txt'), 'w') as f:
        f.write(InFile1noext)
        if InFile2 is not None:
            f.write('\n')
            f.write(InFile2noext)

    # Print results for the user.
    print "Convergence set written.  Run 'runpw' to run all simulations.  Run python ViewCalc.py to view results after.\n"


def frange(start, stop, step):
    while start < stop:
        yield start
        start += step


if __name__ == '__main__':
    # Example to converge a kpoint grid from 1,1,1, 2,2,2, 3,3,3, 4,4,4.
    # Convergekgrid('C.scf.1.in', kGridMultipliers=range(1,5))

    # Example to differentially converge a kpoint grid starting from 2,2,2 to 4,4,4, 6,6,6 and 8,8,8.
    # Convergekgrid(InFile1='Co.HCP.scf.in', kGrid1=[2, 2, 1], InFile2='Co.FCC.scf.in', kGrid2=[2, 2, 2], kGridMultipliers=range(1, 10))


    ConvergeParameter(InFile1='Co.FCC.scf.in', ReplaceStr='s/celldm(1) = 6.48/celldm(1) = %0.2f/', ReplaceLabel='celldm(1)', ReplaceFormatStr='%0.2f', ConvergenceName='ConvergeLatticeParam',
                      ReplaceVals1=list(frange(6.44, 6.52, 0.01)))

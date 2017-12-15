import os

def ConvergeParameter(InFile1=None, ReplaceStr='', ReplaceFormatStr=None, ReplaceLabel='', ConvergenceName='', ReplaceVals1=None, InFile2=None, ReplaceVals2=None, ParallelOpts='-nk 2 -nb 2', MPIOpts='mpirun -np 8'):
    """ InFile1 and 2 should have a format like 'spinel.1.in.  1 and 2 indicate the we are looking for differential convergence.
        if InFile2 is empty, then we only converge on InFile1.
        ReplaceStr is the string that sed will use to replace values.
        ReplaceLabel is a description which goes onto the xlabel of the plots later.
        ReplaceFormatStr is just the formatting string so we can place it in filenames and such.
        ConvergenceName is like title for this calculation, which also goes in filenames, etc.
        ReplaceVals is a list of values or a list of list of values for each replacement
        """

    if ConvergenceName == '' and ReplaceLabel != '':
        ConvergenceName = ReplaceLabel

    # This is the substitution we do to edit the kgrid for each file.
    sedstr = "sed -e '" + ReplaceStr + "' -e 's/calcdir/%s/' %s > %s.in"

    # This is the str to run pw.x.
    pwstr = 'echo %s\npw.x %s < %s.in > %s.out\n'
    pwstrMPI = 'echo %s\nprintf "%s, " >> mpijoblist.txt\nsbatch myjobn.sh %s >> mpijoblist.txt\nsleep 30\n\n'

    # This is the string which will contain all the pw.x commands to run.
    RunStr = list()
    RunStrMPI = list() # And for the cluster too.

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
        if type(Vals) != tuple:
            Vals = (Vals,)

        # Make the unique name which is used for the .in, .out and for the data directory for this calculation.
        BaseName1 = '%s-' + ConvergenceName + '-' + ReplaceFormatStr
        BaseName1Vals = (InFile1noext,) + Vals
        BaseName1 = BaseName1 % BaseName1Vals
        BaseNamesStr1.append(BaseName1)

        # Add the x-axis labels for later plots.
        XVaryStr1.append(ReplaceFormatStr % Vals)

        # sed on first file.
        os.system(sedstr % (Vals + (BaseName1, InFile1, BaseName1)))
        RunStr.append(pwstr % (BaseName1, ParallelOpts, BaseName1, BaseName1))
        RunStrMPI.append(pwstrMPI % (BaseName1, BaseName1, BaseName1))

        if InFile2 is not None:
            Vals = ReplaceVals2[n]
            if type(Vals) != tuple:
                Vals = (Vals,)
            BaseName2 = '%s-' + ConvergenceName + '-' + ReplaceFormatStr
            BaseName2Vals = (InFile2noext,) + Vals
            BaseName2 = BaseName2 % BaseName2Vals
            BaseNamesStr2.append(BaseName2)
            XVaryStr2.append(ReplaceFormatStr % Vals)
            os.system(sedstr % (Vals + (BaseName2, InFile2, BaseName2)))
            RunStr.append(pwstr % (BaseName2, ParallelOpts, BaseName2, BaseName2))
            RunStrMPI.append(pwstrMPI % (BaseName2, BaseName2, BaseName2))

    # Make a bash script that the user can use to run this.
    with open('runpw', 'w') as f:
        f.write('#!/bin/bash\n')
        f.write(''.join(RunStr))
    os.system('chmod +x runpw')
    with open('runpwmpi', 'w') as f:
        f.write('#!/bin/bash\n')
        f.write(''.join(RunStrMPI))
    os.system('chmod +x runpwmpi')

    # Tweak the myjobn.sh to have this job name
    os.system("sed -e 's/jobname/%s/' myjobn.sh > myjobntemp.sh" % ConvergenceName)
    os.system('rm myjobn.sh')
    os.system('mv myjobntemp.sh myjobn.sh')

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
    print("Convergence set written.  Run 'runpw' to run all simulations.  Run python ViewCalc.py to view results after.\n")


def frange(start, stop, step):
    while start < stop:
        yield start
        start += step


if __name__ == '__main__':
    # ConvergeParameter(InFile1='Co.FCC.scf.in', ReplaceStr='s/celldm(1) = 6.48/celldm(1) = %0.2f/', ReplaceLabel='celldm(1)', ReplaceFormatStr='%0.2f', ConvergenceName='ConvergeLatticeParam',
    #                  ReplaceVals1=list(frange(6.44, 6.52, 0.01)))

    # # Example with changing k grid.
    # ReplaceVals = [(x, x, x) for x in range(2,10,1)]
    # ConvergeParameter(InFile1='Periclase.scf', #InFile2='scf.Fe.template',
    #     ReplaceStr='s/3 3 3   0 0 0/%d %d %d 0 0 0/',
    #     ReplaceLabel='kgrid',
    #     ReplaceFormatStr='%d,%d,%d',
    #     ReplaceVals1=ReplaceVals,
    #     #ReplaceVals2=ReplaceVals,
    #     )

    # # Finding Hubbard U in DFT+U.
    # ConvergeParameter(InFile1='Magnetite.relax', ReplaceStr='s/Hubbard_alpha(1) = 1D-40/Hubbard_alpha(1) = %0.3f/',
    #                   ReplaceLabel='HubbardAlpha',
    #                   ReplaceFormatStr='%0.3f',
    #                   ReplaceVals1=list(frange(-0.01, 0.011, 0.001)))

    # ecutwfc
    ReplaceVals = list(frange(50.0, 80.0, 5))
    ConvergeParameter(  InFile1='Tr4CFe.scf',
                        InFile2='Tr4CNi.scf',
                        ReplaceStr='s/ecutwfc=64/ecutwfc=%0.3f/',
                        ReplaceLabel='ecutwfc',
                        ReplaceFormatStr='%0.3f',
                        ReplaceVals1=ReplaceVals,
                        ReplaceVals2=ReplaceVals)

    # # # ecutrho
    # ConvergeParameter(InFile1='Tr4C.scf', ReplaceStr='s/ecutrho = 800/ecutrho = %0.3f/',
    #               ReplaceLabel='ecutrho',
    #               ReplaceFormatStr='%0.3f',
    #               ReplaceVals1=list(frange(500, 1000, 50)))

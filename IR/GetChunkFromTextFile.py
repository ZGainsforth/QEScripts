import numpy as np
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
        SectionData = np.genfromtxt(StringIO(SectionStr), skip_header=skip_header, skip_footer=skip_footer)

    return SectionData

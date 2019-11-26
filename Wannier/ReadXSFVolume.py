import os
import numpy as np
import matplotlib.pyplot as plt
import re
from io import StringIO
from skimage.external.tifffile import imsave 
from scipy.interpolate import griddata
from scipy.signal import medfilt

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

def ReadXSFVolume(FileName, verbose=True, WFOffset=(0,0,0), Cutoff=0.0):
    print(FileName)
    Datagrid = GetChunkFromTextFile(FileName,'BEGIN_DATAGRID_3D_UNKNOWN','END_DATAGRID_3D', DataType='raw')
    lines = Datagrid.splitlines()
    
    # Line 0 is the 'BEGIN_DATAGRID_3D_UNKNOWN' header.
    
    # Line 1 is the x, y, z dimensions of the cube in pixels.
    xPixels, yPixels, zPixels = map(int, lines[1].split())
    if verbose==True:
        print(f'Dimension of data cube is ({xPixels}, {yPixels}, {zPixels}) pixels.')
    
    # Line 2 is the origin. 
    xOrigin, yOrigin, zOrigin = map(float, lines[2].split())
    if verbose==True:
        print(f'Origin of data cube is ({xOrigin}, {yOrigin}, {zOrigin}) angstroms.')
   
    # Lines 3-5 are the metric (or identify matrix if this is a cube with sides of length 1). 
    Mstr = ' '.join(lines[3:6])
    M = np.array(list(map(float, Mstr.split()))).reshape(3,3).T
    if verbose==True:
        print('Metric is:')
        print(M)

    # All the rest of the lines are the volume values.
    vstr = ' '.join(lines[6:])
    v = np.array(list(map(float, vstr.split()))).reshape(xPixels, yPixels, zPixels)

    # Next we need a datacube which encompases the entire volume.
    # Make a cartesian grid of width 1 but same number of pixels as the xsf datacube.
    yp,xp,zp = np.meshgrid(np.linspace(0,1,xPixels), np.linspace(0,1,yPixels), np.linspace(0,1,zPixels))
    
    # Transform those coordinates to the same coordinate system as the xsf datacube.
    C = np.stack([xp,yp,zp], axis=0)
    x,y,z = np.einsum('ij,jklm->iklm', M,C)
    # Shift the origin to zero.
    x += xOrigin + WFOffset[0]
    y += yOrigin + WFOffset[1]
    z += zOrigin + WFOffset[2]

    # The cube x,y,z now represents the coordinates of the actual space that the orbital exists in.
    # we want to resample now using a new larger cube that includes the Wannier function.
    # Find the bounds of the cube.
    xmin = np.min(x); xmax = np.max(x);
    ymin = np.min(y); ymax = np.max(y);
    zmin = np.min(z); zmax = np.max(z);
    # Calculate the pixel sizes from the previous coordinate system.
    dx = np.linalg.norm(M.T[:,0])/xPixels
    dy = np.linalg.norm(M.T[:,1])/yPixels
    dz = np.linalg.norm(M.T[:,2])/zPixels
    # We want our new pixels to be square, so choose the smallest dx,dy,dz.
    dx = dy = dz = np.min([dx,dy,dz])
    # Calculate how many pixels that now is in our new cube.
    nx = np.ceil((xmax-xmin)/dx).astype(int)
    ny = np.ceil((ymax-ymin)/dy).astype(int)
    nz = np.ceil((zmax-zmin)/dz).astype(int)
    Y,X,Z = np.meshgrid(np.linspace(xmin,xmax,nx), np.linspace(ymin,ymax,ny), np.linspace(zmin,zmax,nz)) 

    # We are going to interpolate using griddata.  
    # It expects an (n,D) array of points, whereas we have (x,y,z,D)
    # So collapse the first three dimensions (kind of, ravel all but the last dimension).
    xyz = np.stack([x,y,z],axis=3).reshape(-1,3)
    xyz.shape
    XYZ = np.stack([X,Y,Z],axis=3).reshape(-1,3)
    XYZ.shape
    # And interpolate/extrapolate v->V from xyz->XYZ.
    V = griddata(xyz, v.ravel(), XYZ, method='nearest')
    # Now that we are interpolated, reshape back to (x,y,z,D).
    V = V.reshape(X.shape)
    # Since we use nearest interpolation it comes out a bit noisy.  Fix it.
    V = medfilt(V)

    # # Now eliminate values close to zero.
    # # Vnew = np.zeros(V.shape)
    # # Vnew[V>Cutoff] = V
    # print(Cutoff)
    # Vind1 = V<Cutoff    
    # Vind2 = V>(-Cutoff)
    # Vind = Vind1&Vind2
    # print(Vind)
    # V[Vind] = 1e-25

    # Our pixel sizes are different, and medfilt can also change the amplitudes a little.
    # Renormalize so that the total intensity in our new cube is the same as outside the cube.
    V /= np.sum(V)
    # V *= np.sum(v)
    # Note this will fail if the edge of the cube doesn't have zeros or close because the extrapolation
    # will extend that edge value out...

    # Now eliminate values close to zero.
    # Vnew = np.zeros(V.shape)
    # Vnew[V>Cutoff] = V
    print(Cutoff)
    Vind1 = V<Cutoff    
    Vind2 = V>(-Cutoff)
    Vind = Vind1&Vind2
    V[Vind] = 1e-9

    return(X, Y, Z, V.astype('float32'))

    
if __name__ == '__main__':

    X,Y,Z,V = ReadXSFVolume('NiO_00001.xsf', verbose=False) #, Cutoff=0.001) #, WFOffset=(0,0,3.5945353))

    imsave('NiO_00001.tif', V)

    print('Done.')

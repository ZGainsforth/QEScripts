--------------------------------------------------------------------------------
-- Quanty input file generated using Crispy. If you use this file please cite
-- the following reference: http://dx.doi.org/10.5281/zenodo.1008184.
--
-- elements: 3d
-- symmetry: D4h
-- experiment: XAS
-- edge: L2,3 (2p)
--------------------------------------------------------------------------------
Verbosity(0x0000)

--------------------------------------------------------------------------------
-- Initialize the Hamiltonians.
--------------------------------------------------------------------------------
H_i = 0
H_f = 0

--------------------------------------------------------------------------------
-- Toggle the Hamiltonian terms.
--------------------------------------------------------------------------------
H_atomic = 1
H_crystal_field = 1
H_3d_ligands_hybridization_lmct = 0
H_3d_ligands_hybridization_mlct = 0
H_magnetic_field = 1
H_exchange_field = 0

--------------------------------------------------------------------------------
-- Define the number of electrons, shells, etc.
--------------------------------------------------------------------------------
NBosons = 0
NFermions = 16

NElectrons_2p = 6
NElectrons_3d = 3

IndexDn_2p = {0, 2, 4}
IndexUp_2p = {1, 3, 5}
IndexDn_3d = {6, 8, 10, 12, 14}
IndexUp_3d = {7, 9, 11, 13, 15}

if H_3d_ligands_hybridization_lmct == 1 then
    NFermions = 26

    NElectrons_L1 = 10

    IndexDn_L1 = {16, 18, 20, 22, 24}
    IndexUp_L1 = {17, 19, 21, 23, 25}
end

if H_3d_ligands_hybridization_mlct == 1 then
    NFermions = 26

    NElectrons_L2 = 0

    IndexDn_L2 = {16, 18, 20, 22, 24}
    IndexUp_L2 = {17, 19, 21, 23, 25}
end

if H_3d_ligands_hybridization_lmct == 1 and H_3d_ligands_hybridization_mlct == 1 then
    return
end

--------------------------------------------------------------------------------
-- Define the atomic term.
--------------------------------------------------------------------------------
N_2p = NewOperator('Number', NFermions, IndexUp_2p, IndexUp_2p, {1, 1, 1})
     + NewOperator('Number', NFermions, IndexDn_2p, IndexDn_2p, {1, 1, 1})

N_3d = NewOperator('Number', NFermions, IndexUp_3d, IndexUp_3d, {1, 1, 1, 1, 1})
     + NewOperator('Number', NFermions, IndexDn_3d, IndexDn_3d, {1, 1, 1, 1, 1})

if H_atomic == 1 then
    F0_3d_3d = NewOperator('U', NFermions, IndexUp_3d, IndexDn_3d, {1, 0, 0})
    F2_3d_3d = NewOperator('U', NFermions, IndexUp_3d, IndexDn_3d, {0, 1, 0})
    F4_3d_3d = NewOperator('U', NFermions, IndexUp_3d, IndexDn_3d, {0, 0, 1})

    F0_2p_3d = NewOperator('U', NFermions, IndexUp_2p, IndexDn_2p, IndexUp_3d, IndexDn_3d, {1, 0}, {0, 0})
    F2_2p_3d = NewOperator('U', NFermions, IndexUp_2p, IndexDn_2p, IndexUp_3d, IndexDn_3d, {0, 1}, {0, 0})
    G1_2p_3d = NewOperator('U', NFermions, IndexUp_2p, IndexDn_2p, IndexUp_3d, IndexDn_3d, {0, 0}, {1, 0})
    G3_2p_3d = NewOperator('U', NFermions, IndexUp_2p, IndexDn_2p, IndexUp_3d, IndexDn_3d, {0, 0}, {0, 1})

    U_3d_3d_i = 0.0
    F2_3d_3d_i = 8.9617 * 0.8
    F4_3d_3d_i = 5.5766 * 0.8
    F0_3d_3d_i = U_3d_3d_i + 2 / 63 * F2_3d_3d_i + 2 / 63 * F4_3d_3d_i

    U_3d_3d_f = 0.0
    F2_3d_3d_f = 9.8762 * 0.8
    F4_3d_3d_f = 6.1531 * 0.8
    F0_3d_3d_f = U_3d_3d_f + 2 / 63 * F2_3d_3d_f + 2 / 63 * F4_3d_3d_f
    U_2p_3d_f = 0.0
    F2_2p_3d_f = 5.3511 * 0.8
    G1_2p_3d_f = 3.7928 * 0.8
    G3_2p_3d_f = 2.1542 * 0.8
    F0_2p_3d_f = U_2p_3d_f + 1 / 15 * G1_2p_3d_f + 3 / 70 * G3_2p_3d_f

    H_i = H_i + Chop(
          F0_3d_3d_i * F0_3d_3d
        + F2_3d_3d_i * F2_3d_3d
        + F4_3d_3d_i * F4_3d_3d)

    H_f = H_f + Chop(
          F0_3d_3d_f * F0_3d_3d
        + F2_3d_3d_f * F2_3d_3d
        + F4_3d_3d_f * F4_3d_3d
        + F0_2p_3d_f * F0_2p_3d
        + F2_2p_3d_f * F2_2p_3d
        + G1_2p_3d_f * G1_2p_3d
        + G3_2p_3d_f * G3_2p_3d)

    ldots_3d = NewOperator('ldots', NFermions, IndexUp_3d, IndexDn_3d)

    ldots_2p = NewOperator('ldots', NFermions, IndexUp_2p, IndexDn_2p)

    zeta_3d_i = 0.0222 * 1.0

    zeta_3d_f = 0.0312 * 1.0
    zeta_2p_f = 4.6504 * 1.0

    H_i = H_i + Chop(
          zeta_3d_i * ldots_3d)

    H_f = H_f + Chop(
          zeta_3d_f * ldots_3d
        + zeta_2p_f * ldots_2p)
end

--------------------------------------------------------------------------------
-- Define the crystal field term.
--------------------------------------------------------------------------------
if H_crystal_field == 1 then
    -- PotentialExpandedOnClm('D4h', 2, {Ea1g, Eb1g, Eb2g, Eeg})
    -- Dq_3d = NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, PotentialExpandedOnClm('D4h', 2, { 6,  6, -4, -4}))
    -- Ds_3d = NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, PotentialExpandedOnClm('D4h', 2, {-2,  2,  2, -1}))
    -- Dt_3d = NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, PotentialExpandedOnClm('D4h', 2, {-6, -1, -1,  4}))

    Akm = {{4, 0, 21}, {4, -4, 1.5 * sqrt(70)}, {4, 4, 1.5 * sqrt(70)}}
    Dq_3d = NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, Akm)

    Akm = {{2, 0, -7}}
    Ds_3d = NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, Akm)

    Akm = {{4, 0, -21}}
    Dt_3d = NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, Akm)

    Dq_3d_i = 0.0543
    Ds_3d_i = 0.05
    Dt_3d_i = 0.01

    io.write('Energies of the 3d orbitals in the initial Hamiltonian (crystal field term only):\n')
    io.write('================\n')
    io.write('Irrep.         E\n')
    io.write('================\n')
    io.write(string.format('a1g     %8.3f\n', 6 * Dq_3d_i - 2 * Ds_3d_i - 6 * Dt_3d_i ))
    io.write(string.format('b1g     %8.3f\n', 6 * Dq_3d_i + 2 * Ds_3d_i - Dt_3d_i ))
    io.write(string.format('b2g     %8.3f\n', -4 * Dq_3d_i + 2 * Ds_3d_i - Dt_3d_i ))
    io.write(string.format('eg      %8.3f\n', -4 * Dq_3d_i - Ds_3d_i + 4 * Dt_3d_i))
    io.write('================\n')
    io.write('\n')

    Dq_3d_f = 0.0543
    Ds_3d_f = 0.05
    Dt_3d_f = 0.01

    H_i = H_i + Chop(
          Dq_3d_i * Dq_3d
        + Ds_3d_i * Ds_3d
        + Dt_3d_i * Dt_3d)

    H_f = H_f + Chop(
          Dq_3d_f * Dq_3d
        + Ds_3d_f * Ds_3d
        + Dt_3d_f * Dt_3d)
end

--------------------------------------------------------------------------------
-- Define the 3d-ligands hybridization term (LMCT).
--------------------------------------------------------------------------------
if H_3d_ligands_hybridization_lmct == 1 then
    N_L1 = NewOperator('Number', NFermions, IndexUp_L1, IndexUp_L1, {1, 1, 1, 1, 1})
         + NewOperator('Number', NFermions, IndexDn_L1, IndexDn_L1, {1, 1, 1, 1, 1})

    Delta_3d_L1_i = 0.0
    e_3d_i = (10 * Delta_3d_L1_i - NElectrons_3d * (19 + NElectrons_3d) * U_3d_3d_i / 2) / (10 + NElectrons_3d)
    e_L1_i = NElectrons_3d * ((1 + NElectrons_3d) * U_3d_3d_i / 2 - Delta_3d_L1_i) / (10 + NElectrons_3d)

    Delta_3d_L1_f = 0.0
    e_3d_f = (10 * Delta_3d_L1_f - NElectrons_3d * (31 + NElectrons_3d) * U_3d_3d_f / 2 - 90 * U_2p_3d_f) / (16 + NElectrons_3d)
    e_2p_f = (10 * Delta_3d_L1_f + (1 + NElectrons_3d) * (NElectrons_3d * U_3d_3d_f / 2 - (10 + NElectrons_3d) * U_2p_3d_f)) / (16 + NElectrons_3d)
    e_L1_f = ((1 + NElectrons_3d) * (NElectrons_3d * U_3d_3d_f / 2 + 6 * U_2p_3d_f) - (6 + NElectrons_3d) * Delta_3d_L1_f) / (16 + NElectrons_3d)

    H_i = H_i + Chop(
          e_3d_i * N_3d
        + e_L1_i * N_L1)

    H_f = H_f + Chop(
          e_3d_f * N_3d
        + e_2p_f * N_2p
        + e_L1_f * N_L1)

    Dq_L1 = NewOperator('CF', NFermions, IndexUp_L1, IndexDn_L1, PotentialExpandedOnClm('D4h', 2, { 6,  6, -4, -4}))
    Ds_L1 = NewOperator('CF', NFermions, IndexUp_L1, IndexDn_L1, PotentialExpandedOnClm('D4h', 2, {-2,  2,  2, -1}))
    Dt_L1 = NewOperator('CF', NFermions, IndexUp_L1, IndexDn_L1, PotentialExpandedOnClm('D4h', 2, {-6, -1, -1,  4}))

    Va1g_3d_L1 = NewOperator('CF', NFermions, IndexUp_L1, IndexDn_L1, IndexUp_3d, IndexDn_3d, PotentialExpandedOnClm('D4h', 2, {1, 0, 0, 0}))
               + NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, IndexUp_L1, IndexDn_L1, PotentialExpandedOnClm('D4h', 2, {1, 0, 0, 0}))

    Vb1g_3d_L1 = NewOperator('CF', NFermions, IndexUp_L1, IndexDn_L1, IndexUp_3d, IndexDn_3d, PotentialExpandedOnClm('D4h', 2, {0, 1, 0, 0}))
               + NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, IndexUp_L1, IndexDn_L1, PotentialExpandedOnClm('D4h', 2, {0, 1, 0, 0}))

    Vb2g_3d_L1 = NewOperator('CF', NFermions, IndexUp_L1, IndexDn_L1, IndexUp_3d, IndexDn_3d, PotentialExpandedOnClm('D4h', 2, {0, 0, 1, 0}))
               + NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, IndexUp_L1, IndexDn_L1, PotentialExpandedOnClm('D4h', 2, {0, 0, 1, 0}))

    Veg_3d_L1 = NewOperator('CF', NFermions, IndexUp_L1, IndexDn_L1, IndexUp_3d, IndexDn_3d, PotentialExpandedOnClm('D4h', 2, {0, 0, 0, 1}))
              + NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, IndexUp_L1, IndexDn_L1, PotentialExpandedOnClm('D4h', 2, {0, 0, 0, 1}))

    Dq_L1_i = 0.0
    Ds_L1_i = 0.0
    Dt_L1_i = 0.0
    Va1g_3d_L1_i = 0.0
    Vb1g_3d_L1_i = 0.0
    Vb2g_3d_L1_i = 0.0
    Veg_3d_L1_i = 0.0

    Dq_L1_f = 0.0
    Ds_L1_f = 0.0
    Dt_L1_f = 0.0
    Va1g_3d_L1_f = 0.0
    Vb1g_3d_L1_f = 0.0
    Vb2g_3d_L1_f = 0.0
    Veg_3d_L1_f = 0.0

    H_i = H_i + Chop(
          Dq_L1_i * Dq_L1
        + Ds_L1_i * Ds_L1
        + Dt_L1_i * Dt_L1
        + Va1g_3d_L1_i * Va1g_3d_L1
        + Vb1g_3d_L1_i * Vb1g_3d_L1
        + Vb2g_3d_L1_i * Vb2g_3d_L1
        + Veg_3d_L1_i  * Veg_3d_L1)

    H_f = H_f + Chop(
          Dq_L1_f * Dq_L1
        + Ds_L1_f * Ds_L1
        + Dt_L1_f * Dt_L1
        + Va1g_3d_L1_f * Va1g_3d_L1
        + Vb1g_3d_L1_f * Vb1g_3d_L1
        + Vb2g_3d_L1_f * Vb2g_3d_L1
        + Veg_3d_L1_f  * Veg_3d_L1)
end

--------------------------------------------------------------------------------
-- Define the 3d-ligands hybridization term (MLCT).
--------------------------------------------------------------------------------
if H_3d_ligands_hybridization_mlct == 1 then
    N_L2 = NewOperator('Number', NFermions, IndexUp_L2, IndexUp_L2, {1, 1, 1, 1, 1})
         + NewOperator('Number', NFermions, IndexDn_L2, IndexDn_L2, {1, 1, 1, 1, 1})

    Delta_3d_L2_i = 0.0
    e_3d_i = U_3d_3d_i * (-NElectrons_3d + 1) / 2
    e_L2_i = Delta_3d_L2_i - U_3d_3d_i * NElectrons_3d / 2 - U_3d_3d_i / 2

    Delta_3d_L2_f = 0.0
    e_3d_f = -(U_3d_3d_f * NElectrons_3d^2 + 11 * U_3d_3d_f * NElectrons_3d + 60 * U_2p_3d_f) / (2 * NElectrons_3d + 12)
    e_2p_f = NElectrons_3d * (U_3d_3d_f * NElectrons_3d + U_3d_3d_f - 2 * U_2p_3d_f * NElectrons_3d - 2 * U_2p_3d_f) / (2 * (NElectrons_3d + 6))
    e_L2_f = (2 * Delta_3d_L2_f * NElectrons_3d + 12 * Delta_3d_L2_f - U_3d_3d_f * NElectrons_3d^2 - U_3d_3d_f * NElectrons_3d - 12 * U_2p_3d_f * NElectrons_3d - 12 * U_2p_3d_f) / (2 * (NElectrons_3d + 6))

    H_i = H_i + Chop(
          e_3d_i * N_3d
        + e_L2_i * N_L2)

    H_f = H_f + Chop(
          e_3d_f * N_3d
        + e_2p_f * N_2p
        + e_L2_f * N_L2)

    Dq_L2 = NewOperator('CF', NFermions, IndexUp_L2, IndexDn_L2, PotentialExpandedOnClm('D4h', 2, { 6,  6, -4, -4}))
    Ds_L2 = NewOperator('CF', NFermions, IndexUp_L2, IndexDn_L2, PotentialExpandedOnClm('D4h', 2, {-2,  2,  2, -1}))
    Dt_L2 = NewOperator('CF', NFermions, IndexUp_L2, IndexDn_L2, PotentialExpandedOnClm('D4h', 2, {-6, -1, -1,  4}))

    Va1g_3d_L2 = NewOperator('CF', NFermions, IndexUp_L2, IndexDn_L2, IndexUp_3d, IndexDn_3d, PotentialExpandedOnClm('D4h', 2, {1, 0, 0, 0}))
               + NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, IndexUp_L2, IndexDn_L2, PotentialExpandedOnClm('D4h', 2, {1, 0, 0, 0}))

    Vb1g_3d_L2 = NewOperator('CF', NFermions, IndexUp_L2, IndexDn_L2, IndexUp_3d, IndexDn_3d, PotentialExpandedOnClm('D4h', 2, {0, 1, 0, 0}))
               + NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, IndexUp_L2, IndexDn_L2, PotentialExpandedOnClm('D4h', 2, {0, 1, 0, 0}))

    Vb2g_3d_L2 = NewOperator('CF', NFermions, IndexUp_L2, IndexDn_L2, IndexUp_3d, IndexDn_3d, PotentialExpandedOnClm('D4h', 2, {0, 0, 1, 0}))
               + NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, IndexUp_L2, IndexDn_L2, PotentialExpandedOnClm('D4h', 2, {0, 0, 1, 0}))

    Veg_3d_L2 = NewOperator('CF', NFermions, IndexUp_L2, IndexDn_L2, IndexUp_3d, IndexDn_3d, PotentialExpandedOnClm('D4h', 2, {0, 0, 0, 1}))
              + NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, IndexUp_L2, IndexDn_L2, PotentialExpandedOnClm('D4h', 2, {0, 0, 0, 1}))

    Dq_L2_i = 0.0
    Ds_L2_i = 0.0
    Dt_L2_i = 0.0
    Va1g_3d_L2_i = 0.0
    Vb1g_3d_L2_i = 0.0
    Vb2g_3d_L2_i = 0.0
    Veg_3d_L2_i = 0.0

    Dq_L2_f = 0.0
    Ds_L2_f = 0.0
    Dt_L2_f = 0.0
    Va1g_3d_L2_f = 0.0
    Vb1g_3d_L2_f = 0.0
    Vb2g_3d_L2_f = 0.0
    Veg_3d_L2_f = 0.0

    H_i = H_i + Chop(
          Dq_L2_i * Dq_L2
        + Ds_L2_i * Ds_L2
        + Dt_L2_i * Dt_L2
        + Va1g_3d_L2_i * Va1g_3d_L2
        + Vb1g_3d_L2_i * Vb1g_3d_L2
        + Vb2g_3d_L2_i * Vb2g_3d_L2
        + Veg_3d_L2_i  * Veg_3d_L2)

    H_f = H_f + Chop(
          Dq_L2_f * Dq_L2
        + Ds_L2_f * Ds_L2
        + Dt_L2_f * Dt_L2
        + Va1g_3d_L2_f * Va1g_3d_L2
        + Vb1g_3d_L2_f * Vb1g_3d_L2
        + Vb2g_3d_L2_f * Vb2g_3d_L2
        + Veg_3d_L2_f  * Veg_3d_L2)
end

--------------------------------------------------------------------------------
-- Define the magnetic field and exchange field terms.
--------------------------------------------------------------------------------
Sx_3d = NewOperator('Sx', NFermions, IndexUp_3d, IndexDn_3d)
Sy_3d = NewOperator('Sy', NFermions, IndexUp_3d, IndexDn_3d)
Sz_3d = NewOperator('Sz', NFermions, IndexUp_3d, IndexDn_3d)
Ssqr_3d = NewOperator('Ssqr', NFermions, IndexUp_3d, IndexDn_3d)
Splus_3d = NewOperator('Splus', NFermions, IndexUp_3d, IndexDn_3d)
Smin_3d = NewOperator('Smin', NFermions, IndexUp_3d, IndexDn_3d)

Lx_3d = NewOperator('Lx', NFermions, IndexUp_3d, IndexDn_3d)
Ly_3d = NewOperator('Ly', NFermions, IndexUp_3d, IndexDn_3d)
Lz_3d = NewOperator('Lz', NFermions, IndexUp_3d, IndexDn_3d)
Lsqr_3d = NewOperator('Lsqr', NFermions, IndexUp_3d, IndexDn_3d)
Lplus_3d = NewOperator('Lplus', NFermions, IndexUp_3d, IndexDn_3d)
Lmin_3d = NewOperator('Lmin', NFermions, IndexUp_3d, IndexDn_3d)

Jx_3d = NewOperator('Jx', NFermions, IndexUp_3d, IndexDn_3d)
Jy_3d = NewOperator('Jy', NFermions, IndexUp_3d, IndexDn_3d)
Jz_3d = NewOperator('Jz', NFermions, IndexUp_3d, IndexDn_3d)
Jsqr_3d = NewOperator('Jsqr', NFermions, IndexUp_3d, IndexDn_3d)
Jplus_3d = NewOperator('Jplus', NFermions, IndexUp_3d, IndexDn_3d)
Jmin_3d = NewOperator('Jmin', NFermions, IndexUp_3d, IndexDn_3d)

Tx_3d = NewOperator('Tx', NFermions, IndexUp_3d, IndexDn_3d)
Ty_3d = NewOperator('Ty', NFermions, IndexUp_3d, IndexDn_3d)
Tz_3d = NewOperator('Tz', NFermions, IndexUp_3d, IndexDn_3d)

Sx = Sx_3d
Sy = Sy_3d
Sz = Sz_3d

Lx = Lx_3d
Ly = Ly_3d
Lz = Lz_3d

Jx = Jx_3d
Jy = Jy_3d
Jz = Jz_3d

Tx = Tx_3d
Ty = Ty_3d
Tz = Tz_3d

Ssqr = Sx * Sx + Sy * Sy + Sz * Sz
Lsqr = Lx * Lx + Ly * Ly + Lz * Lz
Jsqr = Jx * Jx + Jy * Jy + Jz * Jz

if H_magnetic_field == 1 then
    Bx_i = 0.0
    By_i = 0.0
    Bz_i = 1.1920928955078125e-07

    Bx_f = 0.0
    By_f = 0.0
    Bz_f = 1.1920928955078125e-07

    H_i = H_i + Chop(
          Bx_i * (2 * Sx + Lx)
        + By_i * (2 * Sy + Ly)
        + Bz_i * (2 * Sz + Lz))

    H_f = H_f + Chop(
          Bx_f * (2 * Sx + Lx)
        + By_f * (2 * Sy + Ly)
        + Bz_f * (2 * Sz + Lz))
end

if H_exchange_field == 1 then
    Hx_i = 0.0
    Hy_i = 0.0
    Hz_i = 0.0

    Hx_f = 0.0
    Hy_f = 0.0
    Hz_f = 0.0

    H_i = H_i + Chop(
          Hx_i * Sx
        + Hy_i * Sy
        + Hz_i * Sz)

    H_f = H_f + Chop(
          Hx_f * Sx
        + Hy_f * Sy
        + Hz_f * Sz)
end

NConfigurations = 1

--------------------------------------------------------------------------------
-- Define the restrictions and set the number of initial states.
--------------------------------------------------------------------------------
InitialRestrictions = {NFermions, NBosons, {'111111 0000000000', NElectrons_2p, NElectrons_2p},
                                           {'000000 1111111111', NElectrons_3d, NElectrons_3d}}

FinalRestrictions = {NFermions, NBosons, {'111111 0000000000', NElectrons_2p - 1, NElectrons_2p - 1},
                                         {'000000 1111111111', NElectrons_3d + 1, NElectrons_3d + 1}}

if H_3d_ligands_hybridization_lmct == 1 then
    InitialRestrictions = {NFermions, NBosons, {'111111 0000000000 0000000000', NElectrons_2p, NElectrons_2p},
                                               {'000000 1111111111 0000000000', NElectrons_3d, NElectrons_3d},
                                               {'000000 0000000000 1111111111', NElectrons_L1, NElectrons_L1}}

    FinalRestrictions = {NFermions, NBosons, {'111111 0000000000 0000000000', NElectrons_2p - 1, NElectrons_2p - 1},
                                             {'000000 1111111111 0000000000', NElectrons_3d + 1, NElectrons_3d + 1},
                                             {'000000 0000000000 1111111111', NElectrons_L1, NElectrons_L1}}

    CalculationRestrictions = {NFermions, NBosons, {'000000 0000000000 1111111111', NElectrons_L1 - (NConfigurations - 1), NElectrons_L1}}
end

if H_3d_ligands_hybridization_mlct == 1 then
    InitialRestrictions = {NFermions, NBosons, {'111111 0000000000 0000000000', NElectrons_2p, NElectrons_2p},
                                               {'000000 1111111111 0000000000', NElectrons_3d, NElectrons_3d},
                                               {'000000 0000000000 1111111111', NElectrons_L2, NElectrons_L2}}

    FinalRestrictions = {NFermions, NBosons, {'111111 0000000000 0000000000', NElectrons_2p - 1, NElectrons_2p - 1},
                                             {'000000 1111111111 0000000000', NElectrons_3d + 1, NElectrons_3d + 1},
                                             {'000000 0000000000 1111111111', NElectrons_L2, NElectrons_L2}}

    CalculationRestrictions = {NFermions, NBosons, {'000000 0000000000 1111111111', NElectrons_L2, NElectrons_L2 + (NConfigurations - 1)}}
end

T = 10.0 * EnergyUnits.Kelvin.value

-- Approximate machine epsilon for single precision arithmetics.
epsilon = 1.19e-07

NPsis = 120
NPsisAuto = 1

dZ = {}

if NPsisAuto == 1 and NPsis ~= 1 then
    NPsis = 4
    NPsisIncrement = 8
    NPsisIsConverged = false

    while not NPsisIsConverged do
        if CalculationRestrictions == nil then
            Psis_i = Eigensystem(H_i, InitialRestrictions, NPsis)
        else
            Psis_i = Eigensystem(H_i, InitialRestrictions, NPsis, {{'restrictions', CalculationRestrictions}})
        end

        if not (type(Psis_i) == 'table') then
            Psis_i = {Psis_i}
        end

        E_gs_i = Psis_i[1] * H_i * Psis_i[1]

        Z = 0

        for i, Psi in ipairs(Psis_i) do
            E = Psi * H_i * Psi

            if math.abs(E - E_gs_i) < epsilon then
                dZ[i] = 1
            else
                dZ[i] = math.exp(-(E - E_gs_i) / T)
            end

            Z = Z + dZ[i]

            if (dZ[i] / Z) < math.sqrt(epsilon) then
                i = i - 1
                NPsisIsConverged = true
                NPsis = i
                Psis_i = {unpack(Psis_i, 1, i)}
                dZ = {unpack(dZ, 1, i)}
                break
            end
        end

        if NPsisIsConverged then
            break
        else
            NPsis = NPsis + NPsisIncrement
        end
    end
else
    if CalculationRestrictions == nil then
        Psis_i = Eigensystem(H_i, InitialRestrictions, NPsis)
    else
        Psis_i = Eigensystem(H_i, InitialRestrictions, NPsis, {{'restrictions', CalculationRestrictions}})
    end

    if not (type(Psis_i) == 'table') then
        Psis_i = {Psis_i}
    end
        E_gs_i = Psis_i[1] * H_i * Psis_i[1]

    Z = 0

    for i, Psi in ipairs(Psis_i) do
        E = Psi * H_i * Psi

        if math.abs(E - E_gs_i) < epsilon then
            dZ[i] = 1
        else
            dZ[i] = math.exp(-(E - E_gs_i) / T)
        end

        Z = Z + dZ[i]
    end
end

-- Normalize dZ to unity.
for i in ipairs(dZ) do
    dZ[i] = dZ[i] / Z
end

--------------------------------------------------------------------------------
-- Define some helper function for the spectra calculation.
--------------------------------------------------------------------------------
function ValueInTable(value, table)
    -- Check if a value is in a table.
    for k, v in ipairs(table) do
        if value == v then
            return true
        end
    end
    return false
end

function GetSpectrum(G, T, Psis, indices, dZSpectra)
    -- Extract the spectra corresponding to the operators identified
    -- using the indices argument. The returned spectrum is a weighted
    -- sum, where the weights are the Boltzmann probabilities.
    if not (type(indices) == 'table') then
        indices = {indices}
    end

    c = 1
    dZSpectrum = {}

    for i in ipairs(T) do
        for k in ipairs(Psis) do
            if ValueInTable(i, indices) then
                table.insert(dZSpectrum, dZSpectra[c])
            else
                table.insert(dZSpectrum, 0)
            end
            c = c + 1
        end
    end

    return Spectra.Sum(G, dZSpectrum)
end

function SaveSpectrum(G, suffix)
    -- Scale, broaden, and save the spectrum to disk.
    G = -1 / math.pi * G

    Gmin1 = 0.24 - Gamma
    Gmax1 = 0.26 - Gamma
    Egamma1 = (522.1 - Eedge1) + DeltaE
    G.Broaden(0, {{Emin, Gmin1}, {Egamma1, Gmin1}, {Egamma1, Gmax1}, {Emax, Gmax1}})

    G.Print({{'file', 'V2+_D4h_2p_XAS_' .. suffix .. '.spec'}})
end

--------------------------------------------------------------------------------
-- Define the transition operators.
--------------------------------------------------------------------------------
t = math.sqrt(1/2)

Tx_2p_3d = NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, IndexUp_2p, IndexDn_2p, {{1, -1, t    }, {1, 1, -t    }})
Ty_2p_3d = NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, IndexUp_2p, IndexDn_2p, {{1, -1, t * I}, {1, 1,  t * I}})
Tz_2p_3d = NewOperator('CF', NFermions, IndexUp_3d, IndexDn_3d, IndexUp_2p, IndexDn_2p, {{1,  0, 1    }                })

k = {0, 0, 1}
ev = {0, 1, 0}
eh = {1, 0, 0}

-- Calculate the right and left polarization vectors.
er = {t * (eh[1] - I * ev[1]),
      t * (eh[2] - I * ev[2]),
      t * (eh[3] - I * ev[3])}

el = {-t * (eh[1] + I * ev[1]),
      -t * (eh[2] + I * ev[2]),
      -t * (eh[3] + I * ev[3])}

function CalculateT(e)
    -- Calculate the transition operator for arbitrary polarization.
    T = e[1] * Tx_2p_3d + e[2] * Ty_2p_3d + e[3] * Tz_2p_3d
    return Chop(T)
end

Tv_2p_3d = CalculateT(ev)
Th_2p_3d = CalculateT(eh)
Tr_2p_3d = CalculateT(er)
Tl_2p_3d = CalculateT(el)
Tk_2p_3d = CalculateT(k)

-- List with the user selected spectra.
spectra = {'Isotropic'}

-- Create two lists, one with the operators and the second with
-- the indices of the operators required to calculate a given
-- spectrum.
T_2p_3d = {}
indices_2p_3d = {}
c = 1

spectrum = 'Isotropic'
if ValueInTable(spectrum, spectra) then
    indices_2p_3d[spectrum] = {}
    for j, operator in ipairs({Tr_2p_3d, Tl_2p_3d, Tk_2p_3d}) do
        table.insert(T_2p_3d, operator)
        table.insert(indices_2p_3d[spectrum], c)
        c = c + 1
    end
end

spectrum = 'Circular Dichroism'
if ValueInTable(spectrum, spectra) then
    indices_2p_3d[spectrum] = {}
    if ValueInTable('Isotropic', spectra) then
        table.insert(indices_2p_3d[spectrum], 1)
        table.insert(indices_2p_3d[spectrum], 2)
    else
        for j, operator in ipairs({Tr_2p_3d, Tl_2p_3d}) do
            table.insert(T_2p_3d, operator)
            table.insert(indices_2p_3d[spectrum], c)
            c = c + 1
        end
    end
end

spectrum = 'Linear Dichroism'
if ValueInTable(spectrum, spectra) then
    indices_2p_3d[spectrum] = {}
    for j, operator in ipairs({Tv_2p_3d, Th_2p_3d}) do
        table.insert(T_2p_3d, operator)
        table.insert(indices_2p_3d[spectrum], c)
        c = c + 1
    end
end

--------------------------------------------------------------------------------
-- Calculate and save the spectra.
--------------------------------------------------------------------------------
Sk = Chop(k[1] * Sx + k[2] * Sy + k[3] * Sz)
Lk = Chop(k[1] * Lx + k[2] * Ly + k[3] * Lz)
Jk = Chop(k[1] * Jx + k[2] * Jy + k[3] * Jz)
Tk = Chop(k[1] * Tx + k[2] * Ty + k[3] * Tz)

Operators = {H_i, Ssqr, Lsqr, Jsqr, Sk, Lk, Jk, Tk, ldots_3d, N_2p, N_3d, 'dZ'}
header = 'Analysis of the initial Hamiltonian:\n'
header = header .. '=================================================================================================================================\n'
header = header .. 'State         <E>     <S^2>     <L^2>     <J^2>      <Sk>      <Lk>      <Jk>      <Tk>     <l.s>    <N_2p>    <N_3d>          dZ\n'
header = header .. '=================================================================================================================================\n'
footer = '=================================================================================================================================\n'

if H_3d_ligands_hybridization_lmct == 1 then
    Operators = {H_i, Ssqr, Lsqr, Jsqr, Sk, Lk, Jk, Tk, ldots_3d, N_2p, N_3d, N_L1, 'dZ'}
    header = 'Analysis of the initial Hamiltonian:\n'
    header = header .. '===========================================================================================================================================\n'
    header = header .. 'State         <E>     <S^2>     <L^2>     <J^2>      <Sk>      <Lk>      <Jk>      <Tk>     <l.s>    <N_2p>    <N_3d>    <N_L1>          dZ\n'
    header = header .. '===========================================================================================================================================\n'
    footer = '===========================================================================================================================================\n'
end

if H_3d_ligands_hybridization_mlct == 1 then
    Operators = {H_i, Ssqr, Lsqr, Jsqr, Sk, Lk, Jk, Tk, ldots_3d, N_2p, N_3d, N_L2, 'dZ'}
    header = 'Analysis of the initial Hamiltonian:\n'
    header = header .. '===========================================================================================================================================\n'
    header = header .. 'State         <E>     <S^2>     <L^2>     <J^2>      <Sk>      <Lk>      <Jk>      <Tk>     <l.s>    <N_2p>    <N_3d>    <N_L2>          dZ\n'
    header = header .. '===========================================================================================================================================\n'
    footer = '===========================================================================================================================================\n'
end

io.write(header)
for i, Psi in ipairs(Psis_i) do
    io.write(string.format('%5d', i))
    for j, Operator in ipairs(Operators) do
        if j == 1 then
            io.write(string.format('%12.6f', Complex.Re(Psi * Operator * Psi)))
        elseif Operator == 'dZ' then
            io.write(string.format('%12.2E', dZ[i]))
        else
            io.write(string.format('%10.4f', Complex.Re(Psi * Operator * Psi)))
        end
    end
    io.write('\n')
end
io.write(footer)


if next(spectra) == nil then
    return
end

E_gs_i = Psis_i[1] * H_i * Psis_i[1]

if CalculationRestrictions == nil then
    Psis_f = Eigensystem(H_f, FinalRestrictions, 1)
else
    Psis_f = Eigensystem(H_f, FinalRestrictions, 1, {{'restrictions', CalculationRestrictions}})
end

Psis_f = {Psis_f}
E_gs_f = Psis_f[1] * H_f * Psis_f[1]

Eedge1 = 512.1
DeltaE = E_gs_f - E_gs_i

Emin = (502.1 - Eedge1) + DeltaE
Emax = (542.1 - Eedge1) + DeltaE
NE = 1000
Gamma = 0.1
DenseBorder = 2000

if CalculationRestrictions == nil then
    G_2p_3d = CreateSpectra(H_f, T_2p_3d, Psis_i, {{'Emin', Emin}, {'Emax', Emax}, {'NE', NE}, {'Gamma', Gamma}, {'DenseBorder', DenseBorder}})
else
    G_2p_3d = CreateSpectra(H_f, T_2p_3d, Psis_i, {{'Emin', Emin}, {'Emax', Emax}, {'NE', NE}, {'Gamma', Gamma}, {'restrictions', CalculationRestrictions}, {'DenseBorder', DenseBorder}})
end

-- Create a list with the Boltzmann probabilities for a given operator
-- and state.
dZ_2p_3d = {}
for i in ipairs(T_2p_3d) do
    for j in ipairs(Psis_i) do
        table.insert(dZ_2p_3d, dZ[j])
    end
end

Pcl_2p_3d = 2

spectrum = 'Isotropic'
if ValueInTable(spectrum, spectra) then
    Giso = GetSpectrum(G_2p_3d, T_2p_3d, Psis_i, indices_2p_3d[spectrum], dZ_2p_3d)
    Giso = Giso / 3 / Pcl_2p_3d
    SaveSpectrum(Giso, 'iso')
end

spectrum = 'Circular Dichroism'
if ValueInTable(spectrum, spectra) then
    Gr = GetSpectrum(G_2p_3d, T_2p_3d, Psis_i, indices_2p_3d[spectrum][1], dZ_2p_3d)
    Gl = GetSpectrum(G_2p_3d, T_2p_3d, Psis_i, indices_2p_3d[spectrum][2], dZ_2p_3d)
    Gr = Gr / Pcl_2p_3d
    Gl = Gl / Pcl_2p_3d
    SaveSpectrum(Gr, 'r')
    SaveSpectrum(Gl, 'l')
    SaveSpectrum(Gr - Gl, 'cd')
end

spectrum = 'Linear Dichroism'
if ValueInTable(spectrum, spectra) then
    Gv = GetSpectrum(G_2p_3d, T_2p_3d, Psis_i, indices_2p_3d[spectrum][1], dZ_2p_3d)
    Gh = GetSpectrum(G_2p_3d, T_2p_3d, Psis_i, indices_2p_3d[spectrum][2], dZ_2p_3d)
    Gv = Gv / Pcl_2p_3d
    Gh = Gh / Pcl_2p_3d
    SaveSpectrum(Gv, 'v')
    SaveSpectrum(Gh, 'h')
    SaveSpectrum(Gv - Gh, 'ld')
end


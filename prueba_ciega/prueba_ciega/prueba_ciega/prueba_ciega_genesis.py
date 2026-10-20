import math
import numpy as np

# Función para leer coordenadas Cα de un archivo PDB
def leer_pdb(path):
    coords = []
    with open(path, 'r') as f:
        for line in f:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                coords.append([x, y, z])
    return np.array(coords)

def kabsch_rmsd(P, Q):
    cP = np.mean(P, axis=0)
    cQ = np.mean(Q, axis=0)
    Pc = P - cP
    Qc = Q - cQ
    H = Pc.T @ Qc
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1.0, 1.0, d])
    R = Vt.T @ D @ U.T
    P_rot = (R @ Pc.T).T
    diff = P_rot - Qc
    return math.sqrt(np.sum(diff**2) / P.shape[0])

# Leer archivos locales
P_out = leer_pdb("salida_restaurada.pdb")
Q_ref = leer_pdb("referencia_secreta.pdb")

rmsd = kabsch_rmsd(P_out, Q_ref)
D_max = 5.0
score = max(0.0, min(1.0, 1.0 - (rmsd / D_max)))

print(f"RMSD_Ca = {rmsd:.4f} A")
print(f"Score S = {score:.4f}")
print(f"Hash de sello: 61243bb8e353fbd07545ea0864c851980c549409667d9b40ea8caebb9c471281")

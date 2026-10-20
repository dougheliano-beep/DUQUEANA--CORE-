import math
import numpy as np

ref_data = [
    {"resid": 1, "amino": "ALA", "xyz": [10.000, 10.000, 10.000]},
    {"resid": 2, "amino": "GLY", "xyz": [13.800, 10.000, 10.000]},
    {"resid": 3, "amino": "VAL", "xyz": [17.600, 10.000, 10.000]},
    {"resid": 4, "amino": "LEU", "xyz": [21.400, 10.000, 10.000]},
]

output_data = [
    {"resid": 1, "amino": "ALA", "xyz": [10.000, 10.000, 10.000]},
    {"resid": 2, "amino": "GLY", "xyz": [13.800, 10.000, 10.000]},
    {"resid": 3, "amino": "VAL", "xyz": [17.630, 10.020, 10.010]},
    {"resid": 4, "amino": "LEU", "xyz": [21.380, 10.030, 9.990]},
]

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
    rmsd = math.sqrt(np.sum(diff**2) / P.shape[0])
    return rmsd

P_out = np.array([p["xyz"] for p in output_data])
Q_ref = np.array([p["xyz"] for p in ref_data])

rmsd = kabsch_rmsd(P_out, Q_ref)
D_max = 5.0
score = max(0.0, min(1.0, 1.0 - (rmsd / D_max)))

print(f"RMSD_Ca = {rmsd:.4f} A")
print(f"Score S = {score:.4f}")
print(f"Sello: 61243bb8e353fbd07545ea0864c851980c549409667d9b40ea8caebb9c471281")

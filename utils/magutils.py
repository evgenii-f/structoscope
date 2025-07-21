import numpy as np
from ase import Atoms

def get_volume(atoms: Atoms) -> float:
    try:
        return atoms.get_volume()
    except Exception:
        return None

def get_n_atoms(atoms: Atoms) -> int:
    return len(atoms)

def total_mag_moment(mag_mom: np.ndarray) -> float:
    return np.linalg.norm(np.sum(mag_mom, axis=0))

def total_mag_moment_abs(mag_mom: np.ndarray) -> float:
    return np.sum(np.linalg.norm(mag_mom, axis=1))

def max_force(forces: np.ndarray) -> float:
    return np.max(np.linalg.norm(forces, axis=1))

def max_mag_mom(mag_mom: np.ndarray) -> float:
    return np.max(np.linalg.norm(mag_mom, axis=1))

def all_moments_equal(mag_mom: np.ndarray, rtol=1e-5, atol=1e-8) -> bool:
    mags = np.linalg.norm(mag_mom, axis=1)
    return np.allclose(mags, mags[0], rtol=rtol, atol=atol)

def is_collinear(mag_mom: np.ndarray, atol=5e-10) -> bool:
    if len(mag_mom) < 2:
        return True
    ref = mag_mom[0]
    cross_products = np.cross(mag_mom, ref)
    return np.allclose(cross_products, 0, atol=atol)

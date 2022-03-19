import os
import emcee
import lymph
import corner
from cycler import cycler
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import font_manager
import matplotlib.gridspec as gs
import matplotlib.pyplot as plt
from multiprocessing import Pool

import numpy as np
import scipy as sp
import pandas as pd

dirname = os.path.dirname(__file__)
hdf5_path = os.path.join(dirname, '../data/extended_system.hdf5')


extended_systm = lymph.utils.system_from_hdf(
    filename=hdf5_path,
    name="extended/model")


def llh(theta):
    early_p = 0.3
    max_t = 10
    spread_probs, late_p = theta[:-1], theta[-1]

    if late_p > 1. or late_p < 0.:
        return -np.inf

    t = np.arange(max_t + 1)
    time_dists = {
        "early": sp.stats.binom.pmf(np.arange(max_t+1), max_t, early_p),
        "late": sp.stats.binom.pmf(np.arange(max_t+1), max_t, late_p),
    }

    return extended_systm.marginal_log_likelihood(spread_probs, t_stages=["early", "late"], time_dists=time_dists)


# Settings for the sampler
ndim = len(extended_systm.spread_probs) + 1
nwalkers = 20 * ndim
nstep = 10000
burnin = 5000
moves = [(emcee.moves.DEMove(), 0.8), (emcee.moves.DESnookerMove(), 0.2)]


# prepare the backend
new_backend = emcee.backends.HDFBackend(
    filename=hdf5_path,
    name="extended/samples"
)
#backend.reset(nwalkers, ndim)
print("Initial size: {0}".format(new_backend.iteration))

# starting point
initial_spread_probs = np.random.uniform(
    low=0., high=1., size=(nwalkers, ndim))


if __name__ == "__main__":
    sampler = emcee.EnsembleSampler(
        nwalkers, ndim,
        llh,
        moves=moves,
        backend=new_backend
    )
    sampler.run_mcmc(initial_spread_probs, nstep -
                     new_backend.iteration, progress=True)
    samples_HMM = sampler.get_chain(flat=True, discard=burnin)
    print(samples_HMM)

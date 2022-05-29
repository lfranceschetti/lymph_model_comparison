from graphs import all_graphs
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
from sklearn.model_selection import KFold

import numpy as np
import scipy as sp
import pandas as pd

np.random.seed(42)
full_data = pd.read_csv("../data/ipsi_data.csv", header=[0,1])


spsn = {"PET": [0.86, 0.79],
            "MRI": [0.63, 0.81],
            "diagnostic_consensus": [0.63, 0.81],
            "pathology": [1., 1.]}

kf = KFold(n_splits=5, random_state = 42, shuffle = True)



def sample(systm):

        # Settings for the sampler
        ndim = len(systm.spread_probs) + 1
        nwalkers =  3* ndim #20 *
        nstep = 10 # 10000
        burnin = 5  # 7000
        moves = [(emcee.moves.DEMove(), 0.8), (emcee.moves.DESnookerMove(), 0.2)]


        initial_spread_probs = np.random.uniform(
            low=0., high=1., size=(nwalkers, ndim))


        if __name__ == "__main__":

            sampler = emcee.EnsembleSampler(
                nwalkers, ndim,
                llh,
                moves=moves,
            )
            sampler.run_mcmc(initial_spread_probs, nstep, progress=True)
            samples_HMM = sampler.get_chain(flat=True, discard=burnin)
            return samples_HMM




for graph in all_graphs:
    system = lymph.Unilateral(graph=graph)
    system.modalities = spsn

    p_D_M = 0
    for train_idx, val_idx in kf.split(full_data):
        data_sample, data_val = full_data.iloc[train_idx], full_data.iloc[val_idx]
        system.patient_data = data_sample

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
            return system.marginal_log_likelihood(spread_probs, t_stages=["early", "late"], time_dists=time_dists)

        

        samples = sample(system)
        sum_llh = 0
        system.patient_data = data_val
        for param in samples:
            sum_llh += llh(param, system)
        p_D_M += sum_llh / len(samples)
        #Hi
        #push changes
        var = 0

    print(p_D_M)





    


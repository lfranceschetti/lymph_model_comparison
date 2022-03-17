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


NEW_MODEL = False

filename = "latest_extended.hdf5"

if not NEW_MODEL:
    extended_systm = lymph.utils.system_from_hdf(
        filename=filename,
        name="extended/model")
else:
    graph = {
        ('tumor', 'primary'): ['II', 'III', 'IV', 'VII'],
        ('lnl', 'I'): [],
        ('lnl', 'II'): ['I', 'III', 'V', 'VII'],
        ('lnl', 'III'): ['IV'],
        ('lnl', 'IV'): [],
        ('lnl', 'V'): [],
        ('lnl', 'VII'): [],
    }
    extended_systm = lymph.Unilateral(graph=graph)


if NEW_MODEL:
    spsn = {"PET": [0.86, 0.79],
            "MRI": [0.63, 0.81],
            "diagnostic_consensus": [0.63, 0.81],
            "pathology": [1., 1.]}
#                    ^   ^
#           specificty     sensitivity
    extended_systm.modalities = spsn

if NEW_MODEL:
    data = pd.read_csv(r"notebook\latest.csv", header=[0, 1, 2])
    t_stage = data.iloc[:, 18]
    data = data.iloc[:, 21:168]
    ipsi_data = data.xs("ipsi", level=1, axis=1)
    t_stage.loc[t_stage <= 2, ] = "early"
    t_stage.loc[t_stage != "early", ] = "late"

    ipsi_data["info", "t_stage"] = t_stage
    ipsi_data = ipsi_data.drop(['Ia', 'Ib', "IIa", "IIb"], level=1, axis=1)
    ipsi_data = ipsi_data.drop(['CT', 'FNA', "pCT"], level=0, axis=1)

    extended_systm.patient_data = ipsi_data


if NEW_MODEL:
    extended_systm.to_hdf(
        filename=filename,
        name="extended/model"
    )


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


ndim = len(extended_systm.spread_probs) + 1
nwalkers = 2 * ndim
nstep = 10
burnin = 5
moves = [(emcee.moves.DEMove(), 0.8), (emcee.moves.DESnookerMove(), 0.2)]

if True:

    initial_spread_probs = np.random.uniform(
        low=0., high=1., size=(nwalkers, ndim))

    backend = emcee.backends.HDFBackend(
        filename=filename,
        name="extended/samples"
    )
    backend.reset(nwalkers, ndim)

    if __name__ == "__main__":
        with Pool() as pool:
            sampler = emcee.EnsembleSampler(
                nwalkers, ndim,
                llh,
                moves=moves, pool=pool,
                backend=backend
            )
            sampler.run_mcmc(initial_spread_probs, nstep)
        samples_HMM = sampler.get_chain(flat=True, discard=burnin)
        print(samples_HMM)
else:
    recover_backend = emcee.backends.HDFBackend(
        filename=filename, name="extended/samples")
    samples_HMM = recover_backend.get_chain(flat=True, discard=burnin)

spread_probs = []
late_p = []
for sample in samples_HMM:
    spread_probs.append(sample[:-1])
    late_p.append(sample[-1])


plt.style.use(r"notebook\lymph.mplstyle")


def set_size(width="single", unit="cm", ratio="golden"):
    if width == "single":
        width = 10
    elif width == "full":
        width = 16
    else:
        try:
            width = width
        except:
            width = 10

    if unit == "cm":
        width = width / 2.54

    if ratio == "golden":
        ratio = 1.618
    else:
        ratio = ratio

    try:
        height = width / ratio
    except:
        height = width / 1.618

    return (width, height)


labels = [r"$\tilde{b}_2$", r"$\tilde{b}_3$",
          r"$\tilde{b}_4$", r"$\tilde{b}_7$",
          r"$\tilde{t}_{21}$", r"$\tilde{t}_{23}$", r"$\tilde{t}_{25}$", r"$\tilde{t}_{27}$", r"$\tilde{t}_{37}$"]

fig = plt.figure(figsize=set_size(width="full", ratio=1))


# USZ colors
usz_blue = '#005ea8'
usz_green = '#00afa5'
usz_red = '#ae0060'
usz_orange = '#f17900'
usz_gray = '#c5d5db'

# colormaps
white_to_blue = LinearSegmentedColormap.from_list("white_to_blue",
                                                  ["#ffffff", usz_blue],
                                                  N=256)
white_to_green = LinearSegmentedColormap.from_list("white_to_green",
                                                   ["#ffffff", usz_green],
                                                   N=256)
green_to_red = LinearSegmentedColormap.from_list("green_to_red",
                                                 [usz_green, usz_red],
                                                 N=256)

h = usz_gray.lstrip('#')
gray_rgba = tuple(int(h[i:i+2], 16) / 255. for i in (0, 2, 4)) + (1.0,)
tmp = LinearSegmentedColormap.from_list("tmp", [usz_green, usz_red], N=128)
tmp = tmp(np.linspace(0., 1., 128))
tmp = np.vstack([np.array([gray_rgba]*128), tmp])
halfGray_halfGreenToRed = ListedColormap(tmp)


corner.corner(np.array(spread_probs), labels=labels, smooth=True, fig=fig,
              hist_kwargs={'histtype': 'stepfilled', 'color': usz_blue},
              **{'plot_datapoints': False, 'no_fill_contours': True,
                 "density_cmap": white_to_blue.reversed(),
                 "contour_kwargs": {"colors": "k"},
                 "levels": np.array([0.2, 0.5, 0.8])},
              show_titles=True, title_kwargs={"fontsize": "medium"})

axes = fig.get_axes()
for ax in axes:
    ax.grid(False)


plt.savefig(r"notebook\extended_corner_HMM.png", dpi=300, bbox_inches="tight")
plt.savefig(r"notebook\extended_corner_HMM.svg", bbox_inches="tight")


extended_systm.spread_probs = np.mean(np.array(spread_probs), axis=0)

# modify the transition matrix for nicer coloring
mod_A = -1 * np.ones_like(extended_systm.A)
for key, nums in extended_systm._idx_dict.items():
    for i in nums:
        mod_A[key, i] = extended_systm.A[key, i]

# plot the transition matrix
fig, ax = plt.subplots(figsize=set_size(ratio=1.),
                       constrained_layout=True)

h = ax.imshow(mod_A, cmap=halfGray_halfGreenToRed, vmin=-1., vmax=1.)
ax.set_xticks(range(len(extended_systm.state_list)))
ax.set_xticklabels(extended_systm.state_list, rotation=-90, fontsize="small")
ax.set_yticks(range(len(extended_systm.state_list)))
ax.set_yticklabels(extended_systm.state_list, fontsize="small")
ax.tick_params(direction="out")
ax.grid(False)

# label the non-zero entries with their probability in %
for i in range(len(extended_systm.state_list)):
    for j in range(len(extended_systm.state_list)):
        if mod_A[i, j] > 0.:
            ax.text(j, i, f"{mod_A[i,j]*100:.1f}", ha="center", va="center",
                    color="white", fontsize="x-small")

plt.savefig(r"notebook\transition_matrix.png", dpi=300, bbox_inches="tight")
plt.savefig(r"notebook\transition_matrix.svg", bbox_inches="tight")

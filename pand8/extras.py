import numpy as np

MASS_ELECTRON_GEV = 0.511e-3

def _calculate_twiss_gamma(alpha, beta):
    gamma = (1 + alpha**2) / beta
    return gamma

def append_twiss_gamma(twiss_df):
    gamma_x = _calculate_twiss_gamma(twiss_df.ALFX, twiss_df.BETX)
    gamma_y = _calculate_twiss_gamma(twiss_df.ALFY, twiss_df.BETY)
    return twiss_df.assign(GAMX=gamma_x, GAMY=gamma_y)

def append_beam_size_columns(twiss_df,
                             emitnx: float, emitny: float,
                             espread_norm: float):
    fix_initial_row_energy(twiss_df)

    relgamma = twiss_df.E / MASS_ELECTRON_GEV
    emitx = emitnx / relgamma
    emity = emitny / relgamma

    sigma_x = np.sqrt(emitx * twiss_df.BETX + (twiss_df.DX * espread_norm)**2)
    sigma_y = np.sqrt(emity * twiss_df.BETY + (twiss_df.DY * espread_norm)**2)

    gamma_x = _calculate_twiss_gamma(twiss_df.ALFX, twiss_df.BETX)
    gamma_y = _calculate_twiss_gamma(twiss_df.ALFY, twiss_df.BETY)

    sigma_xp = np.sqrt(emitx * gamma_x + (twiss_df.DPX * espread_norm)**2)
    sigma_yp = np.sqrt(emity * gamma_y + (twiss_df.DPY * espread_norm)**2)

    twiss_df = twiss_df.assign(SIGMAX=sigma_x,
                               SIGMAY=sigma_y,
                               SIGMAXP=sigma_xp,
                               SIGMAYP=sigma_yp)

    return twiss_df

def fix_initial_row_energy(twiss_df):
    """Initial row always has 0 energy, so set it to the next element's energy,
    which is fine unless the first element changes the energy (unlikely)"""
    initial = twiss_df.iloc[0]
    nxt = twiss_df.iloc[1]
    if initial.E == 0.0:
        twiss_df.at[0, "E"] = nxt.E


def append_s_column(twiss_df):
    return twiss_df.assign(S=twiss_df.SUML)

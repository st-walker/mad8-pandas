# mad8-pandas
loading mad8 output with pandas

```
import pand8
df = pand8.read("TWISS_CL_T20.txt") # For example
# pandas stuff 😇

# Other bits...
# Fixing strangeness:
assert df.iloc[0].E == 0.0 # Wrong and annoying.
df = pand8.fix_initial_row_energy(df)
assert df.iloc[0].E != 0. # No longer wrong or annoying.


# Adding a few extra useful columns
import matplotlib.pyplot as plt
df = pand8.append_beam_size_columns(df, emitnx=1.4e-6, emitny=1.4e-6, espread_norm=1e-4)

df = pand8.append_twiss_gamma(df)

df.plot("SUML", "SIGMAX")
df.plot("SUML", "GAMX")

plt.show()

```

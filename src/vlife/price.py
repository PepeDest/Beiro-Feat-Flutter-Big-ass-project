"""Price equation hook (the 'telos as arrow' T3 formalism). [Price70, Price72, Frank95]

   w_bar * Delta z_bar = Cov(w, z) + E[ w * Delta z ]
        selection term    ^           transmission term ^
with w_i the fitness of entity i, z_i its trait (here: an organisational score such as Phi),
and Delta z_i = z'_i - z_i the change between entity i and its offspring.
The identity is exact for any population. In this project only the SELECTION term can be measured
(structures in a world do not reproduce); the transmission term is the open 'heredity' chapter.
Using Cov(w, Phi) over structures of one world as a descriptive 'selection differential' is a
NOVEL use (docs/PROVENANCE.md): structures are not a reproducing population."""
import numpy as np


def price_decomposition(w, z, z_child):
    w, z, z_child = (np.asarray(a, float) for a in (w, z, z_child))
    wbar = w.mean()
    lhs = (w * z_child).sum() / w.sum() - z.mean()      # change in mean trait of the offspring generation
    selection = np.mean(w * z) / wbar - z.mean()        # = Cov(w,z)/wbar
    transmission = np.mean(w * (z_child - z)) / wbar
    return lhs, selection, transmission


def selection_differential(w, z):
    """Cov(w/w_bar, z): the Price selection term per unit mean fitness."""
    w = np.asarray(w, float); z = np.asarray(z, float)
    return float(np.mean((w / w.mean()) * z) - z.mean())

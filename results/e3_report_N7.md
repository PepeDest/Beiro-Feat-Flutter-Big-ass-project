# E3 report (auto-generated)

Settings: N=7, tau=1.0, p_out=0.05, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=11340)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.013 | +0.007 | +0.022 |
| C | +0.039 | +0.018 | +0.066 |
| KH | -0.023 | -0.048 | -0.001 |
| IAX | +0.005 | -0.002 | +0.010 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.108 | -0.218 | +0.013 |
| C only | +0.308 | +0.200 | +0.399 |
| P only | +0.087 | +0.051 | +0.122 |
| -KH (simplicity) | -0.262 | -0.361 | -0.157 |
| size (-k) | -0.135 | -0.244 | -0.026 |
| -leak (closure) | +0.111 | +0.073 | +0.151 |
| -IAX | -0.095 | -0.125 | -0.066 |
| fitted linear (cross-fitted) | +0.304 | +0.227 | +0.372 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.106 | +0.023 | +0.186 |
| C only | +0.537 | +0.495 | +0.582 |
| P only | +0.155 | +0.107 | +0.203 |
| -KH (simplicity) | -0.695 | -0.735 | -0.661 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.094 | +0.056 | +0.139 |
| -IAX | -0.176 | -0.210 | -0.138 |
| fitted linear (cross-fitted) | +0.473 | +0.427 | +0.514 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0009, fraction of worlds >0 = 0.38

log(V_driven/V_eq): mean=-0.165 +- 0.014 (s.e. over worlds)


## equilibrium  (worlds=30, structures=3780)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.015 | -0.008 | +0.042 |
| C | +0.173 | +0.133 | +0.223 |
| KH | -0.228 | -0.278 | -0.183 |
| IAX | -0.000 | -0.023 | +0.019 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.629 | +0.590 | +0.669 |
| C only | -0.299 | -0.366 | -0.236 |
| P only | +0.215 | +0.168 | +0.263 |
| -KH (simplicity) | +0.391 | +0.335 | +0.444 |
| size (-k) | +0.552 | +0.501 | +0.598 |
| -leak (closure) | -0.029 | -0.119 | +0.046 |
| -IAX | -0.217 | -0.263 | -0.170 |
| fitted linear (cross-fitted) | +0.730 | +0.665 | +0.782 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.447 | +0.380 | +0.519 |
| C only | +0.735 | +0.666 | +0.791 |
| P only | +0.293 | +0.238 | +0.354 |
| -KH (simplicity) | -0.815 | -0.857 | -0.760 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.059 | -0.035 | +0.140 |
| -IAX | -0.299 | -0.359 | -0.244 |
| fitted linear (cross-fitted) | +0.692 | +0.626 | +0.746 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0279, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.003 +- 0.004 (s.e. over worlds)


## driven  (worlds=30, structures=3780)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.013 | +0.005 | +0.022 |
| C | +0.059 | +0.039 | +0.089 |
| KH | +0.001 | -0.028 | +0.019 |
| IAX | +0.007 | +0.003 | +0.011 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.472 | -0.552 | -0.371 |
| C only | +0.595 | +0.519 | +0.666 |
| P only | -0.024 | -0.076 | +0.024 |
| -KH (simplicity) | -0.579 | -0.655 | -0.489 |
| size (-k) | -0.469 | -0.561 | -0.360 |
| -leak (closure) | +0.128 | +0.080 | +0.174 |
| -IAX | -0.062 | -0.104 | -0.029 |
| fitted linear (cross-fitted) | +0.607 | +0.531 | +0.676 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.099 | -0.213 | +0.015 |
| C only | +0.424 | +0.358 | +0.489 |
| P only | +0.022 | -0.054 | +0.101 |
| -KH (simplicity) | -0.636 | -0.683 | -0.587 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.026 | -0.031 | +0.083 |
| -IAX | -0.149 | -0.199 | -0.103 |
| fitted linear (cross-fitted) | +0.477 | +0.422 | +0.537 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0151, fraction of worlds >0 = 0.07

log(V_driven/V_eq): mean=-0.236 +- 0.015 (s.e. over worlds)


## modular_driven  (worlds=30, structures=3780)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.028 | +0.021 | +0.035 |
| C | +0.088 | +0.075 | +0.106 |
| KH | -0.023 | -0.045 | -0.004 |
| IAX | -0.002 | -0.005 | +0.002 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.481 | -0.560 | -0.402 |
| C only | +0.627 | +0.576 | +0.682 |
| P only | +0.069 | +0.016 | +0.130 |
| -KH (simplicity) | -0.597 | -0.661 | -0.538 |
| size (-k) | -0.488 | -0.564 | -0.416 |
| -leak (closure) | +0.232 | +0.189 | +0.271 |
| -IAX | -0.005 | -0.046 | +0.034 |
| fitted linear (cross-fitted) | +0.645 | +0.558 | +0.713 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.031 | -0.163 | +0.102 |
| C only | +0.453 | +0.393 | +0.514 |
| P only | +0.150 | +0.071 | +0.239 |
| -KH (simplicity) | -0.634 | -0.689 | -0.568 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.197 | +0.146 | +0.245 |
| -IAX | -0.078 | -0.128 | -0.026 |
| fitted linear (cross-fitted) | +0.531 | +0.450 | +0.600 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0155, fraction of worlds >0 = 0.07

log(V_driven/V_eq): mean=-0.261 +- 0.015 (s.e. over worlds)

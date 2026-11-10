# E3 report (auto-generated)

Settings: N=6, tau=1.0, p_out=0.05, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=5580)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.055 | +0.045 | +0.066 |
| C | +0.193 | +0.171 | +0.225 |
| KH | -0.173 | -0.208 | -0.143 |
| IAX | -0.015 | -0.025 | -0.008 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.243 | +0.162 | +0.321 |
| C only | +0.378 | +0.337 | +0.421 |
| P only | +0.149 | +0.108 | +0.186 |
| -KH (simplicity) | -0.002 | -0.055 | +0.046 |
| size (-k) | +0.009 | -0.053 | +0.070 |
| -leak (closure) | +0.313 | +0.271 | +0.350 |
| -IAX | -0.066 | -0.088 | -0.045 |
| fitted linear (cross-fitted) | +0.481 | +0.409 | +0.549 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.601 | +0.540 | +0.658 |
| C only | +0.735 | +0.695 | +0.770 |
| P only | +0.176 | +0.130 | +0.212 |
| -KH (simplicity) | -0.038 | -0.134 | +0.048 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.340 | +0.288 | +0.386 |
| -IAX | -0.141 | -0.162 | -0.117 |
| fitted linear (cross-fitted) | +0.679 | +0.622 | +0.732 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0372, fraction of worlds >0 = 0.81

log(V_driven/V_eq): mean=-0.135 +- 0.012 (s.e. over worlds)


## equilibrium  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.108 | +0.076 | +0.180 |
| C | +0.332 | +0.297 | +0.375 |
| KH | -0.349 | -0.392 | -0.311 |
| IAX | -0.079 | -0.151 | -0.045 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.577 | +0.528 | +0.631 |
| C only | +0.260 | +0.206 | +0.315 |
| P only | +0.130 | +0.107 | +0.158 |
| -KH (simplicity) | +0.157 | +0.114 | +0.206 |
| size (-k) | +0.275 | +0.238 | +0.313 |
| -leak (closure) | +0.427 | +0.366 | +0.487 |
| -IAX | -0.118 | -0.145 | -0.096 |
| fitted linear (cross-fitted) | +0.684 | +0.640 | +0.734 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.724 | +0.641 | +0.788 |
| C only | +0.872 | +0.849 | +0.898 |
| P only | +0.149 | +0.119 | +0.178 |
| -KH (simplicity) | -0.459 | -0.549 | -0.366 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.523 | +0.454 | +0.592 |
| -IAX | -0.160 | -0.188 | -0.128 |
| fitted linear (cross-fitted) | +0.751 | +0.671 | +0.812 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0812, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.000 +- 0.000 (s.e. over worlds)


## driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.049 | +0.035 | +0.065 |
| C | +0.158 | +0.132 | +0.194 |
| KH | -0.129 | -0.160 | -0.100 |
| IAX | +0.002 | -0.008 | +0.011 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.157 | +0.076 | +0.239 |
| C only | +0.399 | +0.332 | +0.461 |
| P only | +0.183 | +0.109 | +0.264 |
| -KH (simplicity) | -0.007 | -0.077 | +0.064 |
| size (-k) | -0.052 | -0.125 | +0.023 |
| -leak (closure) | +0.228 | +0.149 | +0.298 |
| -IAX | -0.096 | -0.131 | -0.059 |
| fitted linear (cross-fitted) | +0.513 | +0.411 | +0.588 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.561 | +0.464 | +0.648 |
| C only | +0.682 | +0.618 | +0.743 |
| P only | +0.204 | +0.136 | +0.286 |
| -KH (simplicity) | +0.196 | +0.052 | +0.335 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.228 | +0.134 | +0.318 |
| -IAX | -0.175 | -0.220 | -0.135 |
| fitted linear (cross-fitted) | +0.689 | +0.619 | +0.751 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0228, fraction of worlds >0 = 0.87

log(V_driven/V_eq): mean=-0.179 +- 0.013 (s.e. over worlds)


## modular_driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.057 | +0.046 | +0.074 |
| C | +0.141 | +0.118 | +0.179 |
| KH | -0.090 | -0.135 | -0.057 |
| IAX | -0.015 | -0.022 | -0.009 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.004 | -0.107 | +0.103 |
| C only | +0.475 | +0.414 | +0.533 |
| P only | +0.134 | +0.060 | +0.206 |
| -KH (simplicity) | -0.155 | -0.232 | -0.070 |
| size (-k) | -0.196 | -0.278 | -0.106 |
| -leak (closure) | +0.286 | +0.241 | +0.329 |
| -IAX | +0.016 | -0.017 | +0.049 |
| fitted linear (cross-fitted) | +0.518 | +0.418 | +0.608 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.518 | +0.429 | +0.620 |
| C only | +0.652 | +0.579 | +0.719 |
| P only | +0.175 | +0.087 | +0.258 |
| -KH (simplicity) | +0.148 | +0.020 | +0.259 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.267 | +0.204 | +0.342 |
| -IAX | -0.087 | -0.124 | -0.054 |
| fitted linear (cross-fitted) | +0.629 | +0.548 | +0.712 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0076, fraction of worlds >0 = 0.57

log(V_driven/V_eq): mean=-0.228 +- 0.016 (s.e. over worlds)

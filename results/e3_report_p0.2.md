# E3 report (auto-generated)

Settings: N=6, tau=1.0, p_out=0.2, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=5580)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.026 | +0.021 | +0.034 |
| C | +0.090 | +0.070 | +0.113 |
| KH | -0.043 | -0.069 | -0.020 |
| IAX | +0.002 | -0.004 | +0.008 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.222 | -0.331 | -0.115 |
| C only | +0.456 | +0.372 | +0.532 |
| P only | +0.115 | +0.078 | +0.149 |
| -KH (simplicity) | -0.394 | -0.483 | -0.304 |
| size (-k) | -0.256 | -0.357 | -0.155 |
| -leak (closure) | +0.106 | +0.064 | +0.149 |
| -IAX | -0.135 | -0.160 | -0.106 |
| fitted linear (cross-fitted) | +0.482 | +0.413 | +0.553 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.097 | +0.025 | +0.173 |
| C only | +0.524 | +0.460 | +0.582 |
| P only | +0.134 | +0.091 | +0.179 |
| -KH (simplicity) | -0.685 | -0.727 | -0.640 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.130 | +0.084 | +0.183 |
| -IAX | -0.169 | -0.199 | -0.139 |
| fitted linear (cross-fitted) | +0.505 | +0.452 | +0.557 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0062, fraction of worlds >0 = 0.40

log(V_driven/V_eq): mean=-0.147 +- 0.014 (s.e. over worlds)


## equilibrium  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.062 | +0.046 | +0.083 |
| C | +0.183 | +0.151 | +0.226 |
| KH | -0.199 | -0.245 | -0.162 |
| IAX | -0.039 | -0.061 | -0.022 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.377 | +0.317 | +0.440 |
| C only | +0.036 | -0.031 | +0.106 |
| P only | +0.252 | +0.226 | +0.282 |
| -KH (simplicity) | +0.103 | +0.044 | +0.166 |
| size (-k) | +0.299 | +0.245 | +0.353 |
| -leak (closure) | +0.050 | -0.034 | +0.142 |
| -IAX | -0.245 | -0.275 | -0.215 |
| fitted linear (cross-fitted) | +0.632 | +0.569 | +0.695 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.349 | +0.240 | +0.452 |
| C only | +0.782 | +0.733 | +0.831 |
| P only | +0.240 | +0.207 | +0.275 |
| -KH (simplicity) | -0.821 | -0.865 | -0.776 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.167 | +0.087 | +0.255 |
| -IAX | -0.230 | -0.265 | -0.194 |
| fitted linear (cross-fitted) | +0.708 | +0.629 | +0.786 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0170, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=-0.005 +- 0.005 (s.e. over worlds)


## driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.012 | +0.003 | +0.022 |
| C | +0.066 | +0.036 | +0.104 |
| KH | -0.002 | -0.036 | +0.030 |
| IAX | +0.015 | +0.011 | +0.019 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.482 | -0.579 | -0.401 |
| C only | +0.618 | +0.557 | +0.673 |
| P only | +0.005 | -0.053 | +0.055 |
| -KH (simplicity) | -0.595 | -0.671 | -0.522 |
| size (-k) | -0.485 | -0.576 | -0.403 |
| -leak (closure) | +0.119 | +0.062 | +0.182 |
| -IAX | -0.128 | -0.174 | -0.084 |
| fitted linear (cross-fitted) | +0.637 | +0.590 | +0.684 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.067 | -0.148 | +0.029 |
| C only | +0.383 | +0.284 | +0.478 |
| P only | +0.034 | -0.050 | +0.108 |
| -KH (simplicity) | -0.590 | -0.657 | -0.531 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.087 | +0.018 | +0.160 |
| -IAX | -0.178 | -0.232 | -0.120 |
| fitted linear (cross-fitted) | +0.391 | +0.319 | +0.460 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0146, fraction of worlds >0 = 0.07

log(V_driven/V_eq): mean=-0.195 +- 0.016 (s.e. over worlds)


## modular_driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.039 | +0.029 | +0.049 |
| C | +0.109 | +0.082 | +0.144 |
| KH | -0.012 | -0.044 | +0.018 |
| IAX | +0.000 | -0.004 | +0.008 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.561 | -0.656 | -0.459 |
| C only | +0.713 | +0.658 | +0.757 |
| P only | +0.087 | +0.027 | +0.155 |
| -KH (simplicity) | -0.692 | -0.757 | -0.616 |
| size (-k) | -0.582 | -0.671 | -0.487 |
| -leak (closure) | +0.148 | +0.098 | +0.197 |
| -IAX | -0.031 | -0.059 | -0.001 |
| fitted linear (cross-fitted) | +0.745 | +0.687 | +0.787 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.008 | -0.108 | +0.134 |
| C only | +0.406 | +0.310 | +0.503 |
| P only | +0.129 | +0.051 | +0.209 |
| -KH (simplicity) | -0.643 | -0.723 | -0.554 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.138 | +0.062 | +0.215 |
| -IAX | -0.099 | -0.151 | -0.041 |
| fitted linear (cross-fitted) | +0.492 | +0.415 | +0.563 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0209, fraction of worlds >0 = 0.13

log(V_driven/V_eq): mean=-0.240 +- 0.019 (s.e. over worlds)

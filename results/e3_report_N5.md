# E3 report (auto-generated)

Settings: N=5, tau=1.0, p_out=0.05, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=2700)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.020 | +0.011 | +0.031 |
| C | +0.104 | +0.069 | +0.137 |
| KH | -0.077 | -0.111 | -0.047 |
| IAX | +0.006 | -0.003 | +0.013 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.085 | -0.198 | +0.024 |
| C only | +0.335 | +0.256 | +0.421 |
| P only | +0.059 | +0.014 | +0.107 |
| -KH (simplicity) | -0.277 | -0.360 | -0.190 |
| size (-k) | -0.118 | -0.215 | -0.021 |
| -leak (closure) | +0.147 | +0.093 | +0.203 |
| -IAX | -0.119 | -0.152 | -0.083 |
| fitted linear (cross-fitted) | +0.356 | +0.276 | +0.442 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.090 | +0.003 | +0.186 |
| C only | +0.587 | +0.519 | +0.656 |
| P only | +0.060 | -0.007 | +0.123 |
| -KH (simplicity) | -0.714 | -0.758 | -0.667 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.196 | +0.126 | +0.273 |
| -IAX | -0.151 | -0.194 | -0.104 |
| fitted linear (cross-fitted) | +0.507 | +0.429 | +0.585 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0011, fraction of worlds >0 = 0.49

log(V_driven/V_eq): mean=-0.147 +- 0.014 (s.e. over worlds)


## equilibrium  (worlds=30, structures=900)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.065 | +0.038 | +0.098 |
| C | +0.233 | +0.181 | +0.289 |
| KH | -0.268 | -0.323 | -0.217 |
| IAX | -0.042 | -0.077 | -0.012 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.546 | +0.482 | +0.613 |
| C only | -0.095 | -0.197 | +0.019 |
| P only | +0.208 | +0.168 | +0.256 |
| -KH (simplicity) | +0.240 | +0.169 | +0.317 |
| size (-k) | +0.462 | +0.399 | +0.528 |
| -leak (closure) | +0.178 | +0.069 | +0.278 |
| -IAX | -0.195 | -0.242 | -0.152 |
| fitted linear (cross-fitted) | +0.712 | +0.648 | +0.768 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.426 | +0.286 | +0.541 |
| C only | +0.819 | +0.765 | +0.858 |
| P only | +0.253 | +0.189 | +0.331 |
| -KH (simplicity) | -0.873 | -0.907 | -0.832 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.269 | +0.135 | +0.379 |
| -IAX | -0.253 | -0.331 | -0.187 |
| fitted linear (cross-fitted) | +0.763 | +0.685 | +0.822 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0232, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.002 +- 0.006 (s.e. over worlds)


## driven  (worlds=30, structures=900)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.014 | +0.004 | +0.022 |
| C | +0.086 | +0.064 | +0.116 |
| KH | -0.030 | -0.061 | -0.005 |
| IAX | +0.009 | +0.003 | +0.016 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.396 | -0.503 | -0.285 |
| C only | +0.508 | +0.414 | +0.600 |
| P only | -0.042 | -0.135 | +0.043 |
| -KH (simplicity) | -0.505 | -0.605 | -0.405 |
| size (-k) | -0.381 | -0.503 | -0.259 |
| -leak (closure) | +0.056 | -0.023 | +0.132 |
| -IAX | -0.108 | -0.168 | -0.045 |
| fitted linear (cross-fitted) | +0.485 | +0.370 | +0.595 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.172 | -0.279 | -0.065 |
| C only | +0.405 | +0.317 | +0.512 |
| P only | -0.052 | -0.164 | +0.053 |
| -KH (simplicity) | -0.620 | -0.698 | -0.532 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.060 | -0.061 | +0.166 |
| -IAX | -0.152 | -0.206 | -0.095 |
| fitted linear (cross-fitted) | +0.345 | +0.231 | +0.460 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0089, fraction of worlds >0 = 0.27

log(V_driven/V_eq): mean=-0.213 +- 0.016 (s.e. over worlds)


## modular_driven  (worlds=30, structures=900)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.023 | +0.012 | +0.038 |
| C | +0.093 | +0.067 | +0.124 |
| KH | -0.026 | -0.062 | +0.003 |
| IAX | +0.007 | -0.001 | +0.014 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.405 | -0.504 | -0.297 |
| C only | +0.592 | +0.523 | +0.652 |
| P only | +0.010 | -0.054 | +0.107 |
| -KH (simplicity) | -0.565 | -0.639 | -0.480 |
| size (-k) | -0.434 | -0.533 | -0.328 |
| -leak (closure) | +0.209 | +0.132 | +0.298 |
| -IAX | -0.055 | -0.118 | +0.011 |
| fitted linear (cross-fitted) | +0.552 | +0.438 | +0.650 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.015 | -0.149 | +0.160 |
| C only | +0.538 | +0.421 | +0.643 |
| P only | -0.022 | -0.126 | +0.102 |
| -KH (simplicity) | -0.648 | -0.715 | -0.567 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.259 | +0.145 | +0.380 |
| -IAX | -0.049 | -0.137 | +0.051 |
| fitted linear (cross-fitted) | +0.500 | +0.395 | +0.599 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0110, fraction of worlds >0 = 0.20

log(V_driven/V_eq): mean=-0.231 +- 0.017 (s.e. over worlds)

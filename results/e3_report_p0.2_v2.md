# E3 report (auto-generated)

Settings: N=6, tau=1.0, p_out=0.2, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=5580)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.033 | +0.026 | +0.043 |
| C | +0.111 | +0.088 | +0.139 |
| KH | -0.065 | -0.095 | -0.039 |
| IAX | +0.005 | -0.003 | +0.011 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.193 | -0.297 | -0.095 |
| C only | +0.422 | +0.337 | +0.496 |
| P only | +0.133 | +0.090 | +0.171 |
| -KH (simplicity) | -0.370 | -0.455 | -0.283 |
| size (-k) | -0.218 | -0.315 | -0.125 |
| -leak (closure) | +0.079 | +0.032 | +0.127 |
| -IAX | -0.154 | -0.180 | -0.128 |
| fitted linear (cross-fitted) | +0.446 | +0.376 | +0.521 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.079 | +0.004 | +0.157 |
| C only | +0.528 | +0.470 | +0.587 |
| P only | +0.161 | +0.115 | +0.207 |
| -KH (simplicity) | -0.740 | -0.787 | -0.697 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.105 | +0.055 | +0.159 |
| -IAX | -0.201 | -0.232 | -0.172 |
| fitted linear (cross-fitted) | +0.505 | +0.451 | +0.565 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0042, fraction of worlds >0 = 0.41

log(V_driven/V_eq): mean=-0.130 +- 0.012 (s.e. over worlds)


## equilibrium  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.064 | +0.041 | +0.093 |
| C | +0.218 | +0.174 | +0.270 |
| KH | -0.234 | -0.292 | -0.187 |
| IAX | -0.033 | -0.062 | -0.008 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.363 | +0.302 | +0.420 |
| C only | +0.027 | -0.043 | +0.107 |
| P only | +0.276 | +0.248 | +0.307 |
| -KH (simplicity) | +0.099 | +0.034 | +0.151 |
| size (-k) | +0.293 | +0.235 | +0.345 |
| -leak (closure) | +0.023 | -0.061 | +0.112 |
| -IAX | -0.268 | -0.299 | -0.240 |
| fitted linear (cross-fitted) | +0.612 | +0.546 | +0.676 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.357 | +0.261 | +0.458 |
| C only | +0.749 | +0.692 | +0.809 |
| P only | +0.288 | +0.249 | +0.327 |
| -KH (simplicity) | -0.823 | -0.867 | -0.780 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.119 | +0.037 | +0.195 |
| -IAX | -0.282 | -0.323 | -0.243 |
| fitted linear (cross-fitted) | +0.693 | +0.602 | +0.777 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0201, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.000 +- 0.000 (s.e. over worlds)


## driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.012 | +0.002 | +0.024 |
| C | +0.077 | +0.047 | +0.114 |
| KH | -0.014 | -0.050 | +0.018 |
| IAX | +0.020 | +0.015 | +0.025 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.438 | -0.525 | -0.349 |
| C only | +0.569 | +0.504 | +0.635 |
| P only | +0.010 | -0.072 | +0.078 |
| -KH (simplicity) | -0.561 | -0.631 | -0.492 |
| size (-k) | -0.423 | -0.510 | -0.341 |
| -leak (closure) | +0.077 | +0.007 | +0.147 |
| -IAX | -0.162 | -0.208 | -0.118 |
| fitted linear (cross-fitted) | +0.598 | +0.549 | +0.648 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.141 | -0.220 | -0.050 |
| C only | +0.414 | +0.309 | +0.515 |
| P only | +0.039 | -0.061 | +0.122 |
| -KH (simplicity) | -0.720 | -0.776 | -0.663 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.079 | -0.007 | +0.167 |
| -IAX | -0.205 | -0.248 | -0.153 |
| fitted linear (cross-fitted) | +0.388 | +0.310 | +0.463 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0135, fraction of worlds >0 = 0.10

log(V_driven/V_eq): mean=-0.172 +- 0.014 (s.e. over worlds)


## modular_driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.051 | +0.040 | +0.063 |
| C | +0.132 | +0.103 | +0.173 |
| KH | -0.035 | -0.074 | +0.000 |
| IAX | +0.002 | -0.003 | +0.009 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.506 | -0.600 | -0.402 |
| C only | +0.669 | +0.614 | +0.721 |
| P only | +0.114 | +0.052 | +0.182 |
| -KH (simplicity) | -0.648 | -0.724 | -0.571 |
| size (-k) | -0.526 | -0.620 | -0.428 |
| -leak (closure) | +0.138 | +0.082 | +0.195 |
| -IAX | -0.034 | -0.068 | +0.002 |
| fitted linear (cross-fitted) | +0.706 | +0.639 | +0.765 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.020 | -0.118 | +0.158 |
| C only | +0.420 | +0.315 | +0.514 |
| P only | +0.156 | +0.080 | +0.228 |
| -KH (simplicity) | -0.678 | -0.763 | -0.593 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.117 | +0.044 | +0.186 |
| -IAX | -0.116 | -0.162 | -0.063 |
| fitted linear (cross-fitted) | +0.510 | +0.428 | +0.581 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0190, fraction of worlds >0 = 0.13

log(V_driven/V_eq): mean=-0.219 +- 0.017 (s.e. over worlds)

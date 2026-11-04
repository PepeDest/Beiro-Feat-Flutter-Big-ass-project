# E3 report (auto-generated)

Settings: N=6, tau=1.0, p_out=0.05, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=5580)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.043 | +0.035 | +0.052 |
| C | +0.154 | +0.134 | +0.181 |
| KH | -0.122 | -0.150 | -0.097 |
| IAX | -0.014 | -0.022 | -0.008 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.189 | +0.103 | +0.273 |
| C only | +0.434 | +0.392 | +0.478 |
| P only | +0.137 | +0.092 | +0.171 |
| -KH (simplicity) | -0.064 | -0.122 | -0.017 |
| size (-k) | -0.050 | -0.119 | +0.017 |
| -leak (closure) | +0.338 | +0.298 | +0.375 |
| -IAX | -0.044 | -0.067 | -0.021 |
| fitted linear (cross-fitted) | +0.478 | +0.403 | +0.550 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.579 | +0.518 | +0.639 |
| C only | +0.724 | +0.681 | +0.764 |
| P only | +0.177 | +0.133 | +0.213 |
| -KH (simplicity) | -0.077 | -0.165 | +0.009 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.339 | +0.280 | +0.395 |
| -IAX | -0.123 | -0.146 | -0.094 |
| fitted linear (cross-fitted) | +0.664 | +0.609 | +0.716 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0237, fraction of worlds >0 = 0.77

log(V_driven/V_eq): mean=-0.146 +- 0.014 (s.e. over worlds)


## equilibrium  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.095 | +0.070 | +0.148 |
| C | +0.264 | +0.236 | +0.299 |
| KH | -0.269 | -0.301 | -0.240 |
| IAX | -0.074 | -0.126 | -0.050 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.576 | +0.532 | +0.628 |
| C only | +0.292 | +0.231 | +0.352 |
| P only | +0.126 | +0.105 | +0.147 |
| -KH (simplicity) | +0.136 | +0.090 | +0.182 |
| size (-k) | +0.257 | +0.218 | +0.299 |
| -leak (closure) | +0.451 | +0.390 | +0.511 |
| -IAX | -0.110 | -0.133 | -0.090 |
| fitted linear (cross-fitted) | +0.702 | +0.662 | +0.751 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.729 | +0.638 | +0.803 |
| C only | +0.895 | +0.875 | +0.913 |
| P only | +0.134 | +0.102 | +0.164 |
| -KH (simplicity) | -0.503 | -0.589 | -0.421 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.550 | +0.478 | +0.620 |
| -IAX | -0.141 | -0.170 | -0.108 |
| fitted linear (cross-fitted) | +0.750 | +0.663 | +0.819 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0592, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.009 +- 0.005 (s.e. over worlds)


## driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.041 | +0.031 | +0.052 |
| C | +0.131 | +0.109 | +0.162 |
| KH | -0.088 | -0.111 | -0.064 |
| IAX | -0.001 | -0.010 | +0.007 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.071 | -0.004 | +0.163 |
| C only | +0.487 | +0.430 | +0.546 |
| P only | +0.176 | +0.107 | +0.250 |
| -KH (simplicity) | -0.099 | -0.163 | -0.035 |
| size (-k) | -0.143 | -0.216 | -0.065 |
| -leak (closure) | +0.273 | +0.213 | +0.333 |
| -IAX | -0.063 | -0.100 | -0.027 |
| fitted linear (cross-fitted) | +0.539 | +0.444 | +0.619 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.547 | +0.473 | +0.620 |
| C only | +0.683 | +0.619 | +0.743 |
| P only | +0.219 | +0.162 | +0.280 |
| -KH (simplicity) | +0.156 | +0.031 | +0.295 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.233 | +0.151 | +0.315 |
| -IAX | -0.164 | -0.202 | -0.125 |
| fitted linear (cross-fitted) | +0.688 | +0.639 | +0.733 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0121, fraction of worlds >0 = 0.77

log(V_driven/V_eq): mean=-0.202 +- 0.014 (s.e. over worlds)


## modular_driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.042 | +0.033 | +0.056 |
| C | +0.114 | +0.096 | +0.143 |
| KH | -0.054 | -0.091 | -0.030 |
| IAX | -0.012 | -0.018 | -0.006 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.081 | -0.194 | +0.031 |
| C only | +0.523 | +0.467 | +0.574 |
| P only | +0.109 | +0.027 | +0.187 |
| -KH (simplicity) | -0.229 | -0.308 | -0.144 |
| size (-k) | -0.264 | -0.352 | -0.176 |
| -leak (closure) | +0.289 | +0.234 | +0.339 |
| -IAX | +0.041 | +0.001 | +0.082 |
| fitted linear (cross-fitted) | +0.526 | +0.428 | +0.620 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.460 | +0.370 | +0.560 |
| C only | +0.595 | +0.523 | +0.672 |
| P only | +0.179 | +0.085 | +0.270 |
| -KH (simplicity) | +0.114 | -0.007 | +0.221 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.235 | +0.159 | +0.316 |
| -IAX | -0.063 | -0.110 | -0.003 |
| fitted linear (cross-fitted) | +0.585 | +0.502 | +0.678 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0003, fraction of worlds >0 = 0.53

log(V_driven/V_eq): mean=-0.244 +- 0.017 (s.e. over worlds)

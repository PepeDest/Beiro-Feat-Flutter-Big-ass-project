# E3 report (auto-generated)

Settings: N=6, tau=0.5, p_out=0.05, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=5580)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.028 | +0.021 | +0.036 |
| C | +0.196 | +0.164 | +0.233 |
| KH | -0.173 | -0.211 | -0.134 |
| IAX | +0.002 | -0.004 | +0.007 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.149 | +0.031 | +0.261 |
| C only | +0.324 | +0.224 | +0.423 |
| P only | -0.001 | -0.049 | +0.049 |
| -KH (simplicity) | -0.256 | -0.354 | -0.161 |
| size (-k) | -0.112 | -0.219 | -0.005 |
| -leak (closure) | +0.211 | +0.165 | +0.255 |
| -IAX | -0.105 | -0.131 | -0.080 |
| fitted linear (cross-fitted) | +0.497 | +0.430 | +0.573 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.493 | +0.437 | +0.554 |
| C only | +0.684 | +0.633 | +0.724 |
| P only | +0.035 | -0.023 | +0.097 |
| -KH (simplicity) | -0.697 | -0.740 | -0.653 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.249 | +0.197 | +0.298 |
| -IAX | -0.171 | -0.201 | -0.141 |
| fitted linear (cross-fitted) | +0.648 | +0.602 | +0.691 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0050, fraction of worlds >0 = 0.62

log(V_driven/V_eq): mean=-0.144 +- 0.015 (s.e. over worlds)


## equilibrium  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.162 | +0.109 | +0.232 |
| C | +0.312 | +0.256 | +0.378 |
| KH | -0.361 | -0.433 | -0.299 |
| IAX | -0.146 | -0.218 | -0.091 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.741 | +0.709 | +0.778 |
| C only | -0.220 | -0.290 | -0.149 |
| P only | +0.225 | +0.196 | +0.257 |
| -KH (simplicity) | +0.281 | +0.222 | +0.340 |
| size (-k) | +0.472 | +0.419 | +0.525 |
| -leak (closure) | +0.032 | -0.050 | +0.123 |
| -IAX | -0.221 | -0.251 | -0.191 |
| fitted linear (cross-fitted) | +0.769 | +0.730 | +0.808 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.695 | +0.651 | +0.743 |
| C only | +0.824 | +0.785 | +0.864 |
| P only | +0.278 | +0.228 | +0.323 |
| -KH (simplicity) | -0.846 | -0.880 | -0.811 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.088 | +0.019 | +0.167 |
| -IAX | -0.271 | -0.316 | -0.223 |
| fitted linear (cross-fitted) | +0.774 | +0.728 | +0.823 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0164, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.019 +- 0.005 (s.e. over worlds)


## driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.012 | +0.001 | +0.024 |
| C | +0.148 | +0.106 | +0.194 |
| KH | -0.102 | -0.147 | -0.060 |
| IAX | +0.012 | +0.006 | +0.019 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.159 | -0.285 | -0.038 |
| C only | +0.525 | +0.439 | +0.605 |
| P only | -0.149 | -0.218 | -0.084 |
| -KH (simplicity) | -0.464 | -0.559 | -0.360 |
| size (-k) | -0.347 | -0.455 | -0.235 |
| -leak (closure) | +0.261 | +0.183 | +0.331 |
| -IAX | -0.086 | -0.131 | -0.036 |
| fitted linear (cross-fitted) | +0.626 | +0.547 | +0.699 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.347 | +0.281 | +0.417 |
| C only | +0.576 | +0.504 | +0.650 |
| P only | -0.101 | -0.192 | -0.016 |
| -KH (simplicity) | -0.590 | -0.650 | -0.523 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.276 | +0.196 | +0.351 |
| -IAX | -0.171 | -0.207 | -0.127 |
| fitted linear (cross-fitted) | +0.547 | +0.467 | +0.618 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0010, fraction of worlds >0 = 0.50

log(V_driven/V_eq): mean=-0.206 +- 0.015 (s.e. over worlds)


## modular_driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.036 | +0.023 | +0.050 |
| C | +0.200 | +0.159 | +0.248 |
| KH | -0.125 | -0.177 | -0.083 |
| IAX | +0.005 | -0.001 | +0.015 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.137 | -0.257 | -0.009 |
| C only | +0.666 | +0.597 | +0.725 |
| P only | -0.079 | -0.166 | +0.011 |
| -KH (simplicity) | -0.585 | -0.664 | -0.499 |
| size (-k) | -0.461 | -0.558 | -0.358 |
| -leak (closure) | +0.341 | +0.306 | +0.378 |
| -IAX | -0.008 | -0.043 | +0.026 |
| fitted linear (cross-fitted) | +0.735 | +0.635 | +0.808 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.437 | +0.327 | +0.549 |
| C only | +0.650 | +0.569 | +0.724 |
| P only | -0.071 | -0.176 | +0.023 |
| -KH (simplicity) | -0.654 | -0.735 | -0.574 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.383 | +0.315 | +0.442 |
| -IAX | -0.070 | -0.114 | -0.019 |
| fitted linear (cross-fitted) | +0.610 | +0.524 | +0.691 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0003, fraction of worlds >0 = 0.37

log(V_driven/V_eq): mean=-0.244 +- 0.018 (s.e. over worlds)

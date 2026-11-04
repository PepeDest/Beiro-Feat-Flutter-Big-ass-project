# E3 report (auto-generated)

Settings: N=6, tau=2.0, p_out=0.05, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=5580)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.018 | +0.013 | +0.025 |
| C | +0.028 | +0.015 | +0.046 |
| KH | -0.009 | -0.029 | +0.008 |
| IAX | +0.003 | -0.003 | +0.008 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.225 | -0.329 | -0.123 |
| C only | +0.343 | +0.253 | +0.427 |
| P only | +0.102 | +0.064 | +0.143 |
| -KH (simplicity) | -0.256 | -0.354 | -0.161 |
| size (-k) | -0.112 | -0.219 | -0.005 |
| -leak (closure) | +0.097 | +0.048 | +0.144 |
| -IAX | -0.105 | -0.131 | -0.080 |
| fitted linear (cross-fitted) | +0.291 | +0.219 | +0.367 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.530 | -0.593 | -0.468 |
| C only | +0.476 | +0.417 | +0.540 |
| P only | +0.148 | +0.102 | +0.200 |
| -KH (simplicity) | -0.697 | -0.740 | -0.653 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.128 | +0.081 | +0.176 |
| -IAX | -0.171 | -0.201 | -0.141 |
| fitted linear (cross-fitted) | +0.372 | +0.313 | +0.430 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0020, fraction of worlds >0 = 0.43

log(V_driven/V_eq): mean=-0.144 +- 0.015 (s.e. over worlds)


## equilibrium  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.027 | +0.017 | +0.040 |
| C | +0.121 | +0.100 | +0.143 |
| KH | -0.160 | -0.190 | -0.136 |
| IAX | -0.006 | -0.019 | +0.006 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.349 | +0.286 | +0.412 |
| C only | -0.085 | -0.165 | -0.001 |
| P only | +0.227 | +0.201 | +0.256 |
| -KH (simplicity) | +0.281 | +0.222 | +0.340 |
| size (-k) | +0.472 | +0.419 | +0.525 |
| -leak (closure) | +0.008 | -0.073 | +0.097 |
| -IAX | -0.221 | -0.251 | -0.191 |
| fitted linear (cross-fitted) | +0.642 | +0.591 | +0.695 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.453 | -0.554 | -0.360 |
| C only | +0.711 | +0.646 | +0.778 |
| P only | +0.277 | +0.229 | +0.315 |
| -KH (simplicity) | -0.846 | -0.880 | -0.811 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.171 | +0.098 | +0.249 |
| -IAX | -0.271 | -0.316 | -0.223 |
| fitted linear (cross-fitted) | +0.583 | +0.463 | +0.675 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0273, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.019 +- 0.005 (s.e. over worlds)


## driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.008 | +0.001 | +0.015 |
| C | +0.035 | +0.016 | +0.060 |
| KH | +0.011 | -0.017 | +0.032 |
| IAX | +0.011 | +0.007 | +0.015 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.448 | -0.542 | -0.342 |
| C only | +0.497 | +0.402 | +0.577 |
| P only | -0.027 | -0.094 | +0.029 |
| -KH (simplicity) | -0.464 | -0.559 | -0.360 |
| size (-k) | -0.347 | -0.455 | -0.235 |
| -leak (closure) | +0.095 | +0.027 | +0.171 |
| -IAX | -0.086 | -0.131 | -0.036 |
| fitted linear (cross-fitted) | +0.491 | +0.415 | +0.568 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.527 | -0.596 | -0.443 |
| C only | +0.298 | +0.204 | +0.382 |
| P only | +0.030 | -0.043 | +0.096 |
| -KH (simplicity) | -0.590 | -0.650 | -0.523 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.059 | -0.010 | +0.135 |
| -IAX | -0.171 | -0.207 | -0.127 |
| fitted linear (cross-fitted) | +0.309 | +0.231 | +0.390 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0123, fraction of worlds >0 = 0.20

log(V_driven/V_eq): mean=-0.206 +- 0.015 (s.e. over worlds)


## modular_driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.030 | +0.020 | +0.042 |
| C | +0.064 | +0.042 | +0.093 |
| KH | +0.009 | -0.016 | +0.030 |
| IAX | -0.000 | -0.005 | +0.006 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.576 | -0.653 | -0.488 |
| C only | +0.618 | +0.540 | +0.685 |
| P only | +0.105 | +0.034 | +0.189 |
| -KH (simplicity) | -0.585 | -0.664 | -0.499 |
| size (-k) | -0.461 | -0.558 | -0.358 |
| -leak (closure) | +0.187 | +0.130 | +0.244 |
| -IAX | -0.008 | -0.043 | +0.026 |
| fitted linear (cross-fitted) | +0.640 | +0.573 | +0.698 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.611 | -0.704 | -0.512 |
| C only | +0.419 | +0.309 | +0.518 |
| P only | +0.137 | +0.038 | +0.238 |
| -KH (simplicity) | -0.654 | -0.735 | -0.574 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.153 | +0.067 | +0.242 |
| -IAX | -0.070 | -0.114 | -0.019 |
| fitted linear (cross-fitted) | +0.445 | +0.339 | +0.539 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0210, fraction of worlds >0 = 0.10

log(V_driven/V_eq): mean=-0.244 +- 0.018 (s.e. over worlds)

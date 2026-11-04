# E3 report (auto-generated)

Settings: tau=1.0, p_out=0.05, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=5580)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.024 | +0.018 | +0.033 |
| C | +0.095 | +0.075 | +0.119 |
| KH | -0.072 | -0.101 | -0.046 |
| IAX | -0.000 | -0.008 | +0.006 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.083 | -0.199 | +0.029 |
| C only | +0.328 | +0.236 | +0.417 |
| P only | +0.085 | +0.047 | +0.130 |
| -KH (simplicity) | -0.256 | -0.354 | -0.161 |
| size (-k) | -0.112 | -0.219 | -0.005 |
| -leak (closure) | +0.120 | +0.074 | +0.166 |
| -IAX | -0.105 | -0.131 | -0.080 |
| fitted linear (cross-fitted) | +0.361 | +0.283 | +0.441 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.103 | +0.031 | +0.179 |
| C only | +0.547 | +0.487 | +0.602 |
| P only | +0.137 | +0.091 | +0.180 |
| -KH (simplicity) | -0.697 | -0.740 | -0.653 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.128 | +0.076 | +0.176 |
| -IAX | -0.171 | -0.201 | -0.141 |
| fitted linear (cross-fitted) | +0.493 | +0.432 | +0.555 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0009, fraction of worlds >0 = 0.49

log(V_driven/V_eq): mean=-0.144 +- 0.015 (s.e. over worlds)


## equilibrium  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.058 | +0.037 | +0.085 |
| C | +0.193 | +0.163 | +0.230 |
| KH | -0.236 | -0.279 | -0.202 |
| IAX | -0.041 | -0.068 | -0.018 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.541 | +0.495 | +0.587 |
| C only | -0.143 | -0.220 | -0.062 |
| P only | +0.227 | +0.199 | +0.258 |
| -KH (simplicity) | +0.281 | +0.222 | +0.340 |
| size (-k) | +0.472 | +0.419 | +0.525 |
| -leak (closure) | +0.038 | -0.045 | +0.133 |
| -IAX | -0.221 | -0.251 | -0.191 |
| fitted linear (cross-fitted) | +0.720 | +0.678 | +0.765 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.376 | +0.263 | +0.478 |
| C only | +0.793 | +0.749 | +0.838 |
| P only | +0.279 | +0.233 | +0.320 |
| -KH (simplicity) | -0.846 | -0.880 | -0.811 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.142 | +0.067 | +0.220 |
| -IAX | -0.271 | -0.316 | -0.223 |
| fitted linear (cross-fitted) | +0.702 | +0.605 | +0.777 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0250, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.019 +- 0.005 (s.e. over worlds)


## driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.010 | +0.000 | +0.020 |
| C | +0.075 | +0.043 | +0.113 |
| KH | -0.030 | -0.067 | +0.004 |
| IAX | +0.011 | +0.007 | +0.015 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.344 | -0.451 | -0.236 |
| C only | +0.508 | +0.421 | +0.586 |
| P only | -0.042 | -0.109 | +0.019 |
| -KH (simplicity) | -0.464 | -0.559 | -0.360 |
| size (-k) | -0.347 | -0.455 | -0.235 |
| -leak (closure) | +0.154 | +0.086 | +0.222 |
| -IAX | -0.086 | -0.131 | -0.036 |
| fitted linear (cross-fitted) | +0.542 | +0.469 | +0.614 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.067 | -0.146 | +0.015 |
| C only | +0.407 | +0.325 | +0.489 |
| P only | +0.016 | -0.069 | +0.092 |
| -KH (simplicity) | -0.590 | -0.650 | -0.523 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.098 | +0.021 | +0.171 |
| -IAX | -0.171 | -0.207 | -0.127 |
| fitted linear (cross-fitted) | +0.382 | +0.301 | +0.461 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0086, fraction of worlds >0 = 0.27

log(V_driven/V_eq): mean=-0.206 +- 0.015 (s.e. over worlds)


## modular_driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.037 | +0.027 | +0.047 |
| C | +0.113 | +0.087 | +0.148 |
| KH | -0.040 | -0.075 | -0.009 |
| IAX | -0.000 | -0.004 | +0.007 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.446 | -0.544 | -0.338 |
| C only | +0.618 | +0.551 | +0.676 |
| P only | +0.072 | +0.002 | +0.144 |
| -KH (simplicity) | -0.585 | -0.664 | -0.499 |
| size (-k) | -0.461 | -0.558 | -0.358 |
| -leak (closure) | +0.168 | +0.112 | +0.223 |
| -IAX | -0.008 | -0.043 | +0.026 |
| fitted linear (cross-fitted) | +0.640 | +0.528 | +0.725 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.000 | -0.126 | +0.134 |
| C only | +0.442 | +0.358 | +0.541 |
| P only | +0.115 | +0.036 | +0.187 |
| -KH (simplicity) | -0.654 | -0.735 | -0.574 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.145 | +0.068 | +0.234 |
| -IAX | -0.070 | -0.114 | -0.019 |
| fitted linear (cross-fitted) | +0.477 | +0.388 | +0.571 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0138, fraction of worlds >0 = 0.20

log(V_driven/V_eq): mean=-0.244 +- 0.018 (s.e. over worlds)

# E3 report (auto-generated)

Settings: N=6, tau=1.0, p_out=0.05, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=5580)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.034 | +0.028 | +0.041 |
| C | +0.128 | +0.108 | +0.156 |
| KH | -0.101 | -0.130 | -0.077 |
| IAX | -0.008 | -0.015 | -0.003 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.048 | -0.049 | +0.139 |
| C only | +0.395 | +0.337 | +0.450 |
| P only | +0.112 | +0.072 | +0.149 |
| -KH (simplicity) | -0.151 | -0.226 | -0.080 |
| size (-k) | -0.088 | -0.170 | -0.005 |
| -leak (closure) | +0.253 | +0.212 | +0.293 |
| -IAX | -0.062 | -0.088 | -0.036 |
| fitted linear (cross-fitted) | +0.426 | +0.350 | +0.499 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.433 | +0.356 | +0.503 |
| C only | +0.619 | +0.559 | +0.671 |
| P only | +0.164 | +0.122 | +0.206 |
| -KH (simplicity) | -0.292 | -0.372 | -0.216 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.251 | +0.189 | +0.311 |
| -IAX | -0.137 | -0.170 | -0.107 |
| fitted linear (cross-fitted) | +0.629 | +0.571 | +0.680 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0097, fraction of worlds >0 = 0.61

log(V_driven/V_eq): mean=-0.148 +- 0.014 (s.e. over worlds)


## equilibrium  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.084 | +0.066 | +0.119 |
| C | +0.232 | +0.206 | +0.261 |
| KH | -0.255 | -0.284 | -0.230 |
| IAX | -0.065 | -0.099 | -0.046 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.538 | +0.498 | +0.579 |
| C only | +0.167 | +0.102 | +0.234 |
| P only | +0.156 | +0.131 | +0.182 |
| -KH (simplicity) | +0.176 | +0.130 | +0.226 |
| size (-k) | +0.325 | +0.285 | +0.369 |
| -leak (closure) | +0.319 | +0.236 | +0.400 |
| -IAX | -0.149 | -0.177 | -0.122 |
| fitted linear (cross-fitted) | +0.726 | +0.686 | +0.769 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.671 | +0.590 | +0.737 |
| C only | +0.876 | +0.851 | +0.899 |
| P only | +0.164 | +0.123 | +0.200 |
| -KH (simplicity) | -0.605 | -0.677 | -0.538 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.435 | +0.354 | +0.512 |
| -IAX | -0.170 | -0.209 | -0.131 |
| fitted linear (cross-fitted) | +0.773 | +0.723 | +0.818 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0394, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.012 +- 0.005 (s.e. over worlds)


## driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.029 | +0.020 | +0.039 |
| C | +0.114 | +0.091 | +0.141 |
| KH | -0.070 | -0.095 | -0.047 |
| IAX | +0.004 | -0.003 | +0.010 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.096 | -0.191 | +0.002 |
| C only | +0.467 | +0.398 | +0.534 |
| P only | +0.105 | +0.034 | +0.180 |
| -KH (simplicity) | -0.230 | -0.303 | -0.147 |
| size (-k) | -0.213 | -0.305 | -0.122 |
| -leak (closure) | +0.206 | +0.138 | +0.271 |
| -IAX | -0.067 | -0.109 | -0.024 |
| fitted linear (cross-fitted) | +0.540 | +0.444 | +0.616 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.398 | +0.318 | +0.487 |
| C only | +0.565 | +0.498 | +0.632 |
| P only | +0.156 | +0.083 | +0.231 |
| -KH (simplicity) | -0.112 | -0.225 | +0.017 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.161 | +0.085 | +0.247 |
| -IAX | -0.166 | -0.205 | -0.120 |
| fitted linear (cross-fitted) | +0.625 | +0.571 | +0.673 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0001, fraction of worlds >0 = 0.57

log(V_driven/V_eq): mean=-0.210 +- 0.015 (s.e. over worlds)


## modular_driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.035 | +0.028 | +0.045 |
| C | +0.100 | +0.079 | +0.131 |
| KH | -0.035 | -0.068 | -0.007 |
| IAX | -0.006 | -0.010 | -0.002 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.299 | -0.397 | -0.190 |
| C only | +0.552 | +0.497 | +0.610 |
| P only | +0.073 | +0.006 | +0.140 |
| -KH (simplicity) | -0.400 | -0.477 | -0.311 |
| size (-k) | -0.377 | -0.469 | -0.277 |
| -leak (closure) | +0.234 | +0.179 | +0.289 |
| -IAX | +0.030 | -0.009 | +0.064 |
| fitted linear (cross-fitted) | +0.562 | +0.458 | +0.651 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.230 | +0.125 | +0.355 |
| C only | +0.415 | +0.316 | +0.517 |
| P only | +0.173 | +0.082 | +0.255 |
| -KH (simplicity) | -0.158 | -0.270 | -0.051 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.156 | +0.075 | +0.242 |
| -IAX | -0.073 | -0.127 | -0.018 |
| fitted linear (cross-fitted) | +0.512 | +0.426 | +0.598 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0101, fraction of worlds >0 = 0.27

log(V_driven/V_eq): mean=-0.247 +- 0.017 (s.e. over worlds)

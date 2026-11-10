# E3 report (auto-generated)

Settings: N=5, tau=1.0, p_out=0.05, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=2700)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.028 | +0.017 | +0.040 |
| C | +0.135 | +0.093 | +0.175 |
| KH | -0.119 | -0.160 | -0.083 |
| IAX | +0.008 | -0.003 | +0.016 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.010 | -0.106 | +0.088 |
| C only | +0.260 | +0.187 | +0.342 |
| P only | +0.065 | +0.016 | +0.110 |
| -KH (simplicity) | -0.212 | -0.298 | -0.131 |
| size (-k) | -0.033 | -0.121 | +0.057 |
| -leak (closure) | +0.131 | +0.075 | +0.188 |
| -IAX | -0.132 | -0.162 | -0.099 |
| fitted linear (cross-fitted) | +0.344 | +0.260 | +0.426 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.076 | -0.015 | +0.168 |
| C only | +0.592 | +0.523 | +0.653 |
| P only | +0.080 | +0.013 | +0.140 |
| -KH (simplicity) | -0.767 | -0.813 | -0.717 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.185 | +0.107 | +0.258 |
| -IAX | -0.153 | -0.192 | -0.112 |
| fitted linear (cross-fitted) | +0.488 | +0.403 | +0.561 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0061, fraction of worlds >0 = 0.56

log(V_driven/V_eq): mean=-0.140 +- 0.013 (s.e. over worlds)


## equilibrium  (worlds=30, structures=900)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.069 | +0.040 | +0.098 |
| C | +0.297 | +0.241 | +0.362 |
| KH | -0.350 | -0.418 | -0.292 |
| IAX | -0.040 | -0.073 | -0.006 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.576 | +0.512 | +0.643 |
| C only | -0.139 | -0.247 | -0.028 |
| P only | +0.200 | +0.151 | +0.252 |
| -KH (simplicity) | +0.283 | +0.215 | +0.360 |
| size (-k) | +0.505 | +0.446 | +0.565 |
| -leak (closure) | +0.160 | +0.039 | +0.278 |
| -IAX | -0.197 | -0.250 | -0.148 |
| fitted linear (cross-fitted) | +0.727 | +0.667 | +0.775 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.384 | +0.224 | +0.511 |
| C only | +0.824 | +0.763 | +0.870 |
| P only | +0.221 | +0.159 | +0.289 |
| -KH (simplicity) | -0.886 | -0.917 | -0.852 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.291 | +0.182 | +0.392 |
| -IAX | -0.220 | -0.290 | -0.157 |
| fitted linear (cross-fitted) | +0.758 | +0.683 | +0.819 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0318, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.000 +- 0.000 (s.e. over worlds)


## driven  (worlds=30, structures=900)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.016 | +0.003 | +0.028 |
| C | +0.110 | +0.081 | +0.150 |
| KH | -0.060 | -0.101 | -0.027 |
| IAX | +0.016 | +0.008 | +0.023 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.289 | -0.408 | -0.180 |
| C only | +0.420 | +0.319 | +0.518 |
| P only | -0.058 | -0.150 | +0.027 |
| -KH (simplicity) | -0.428 | -0.527 | -0.320 |
| size (-k) | -0.266 | -0.388 | -0.135 |
| -leak (closure) | +0.035 | -0.051 | +0.120 |
| -IAX | -0.135 | -0.196 | -0.074 |
| fitted linear (cross-fitted) | +0.454 | +0.350 | +0.549 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.176 | -0.297 | -0.053 |
| C only | +0.441 | +0.358 | +0.537 |
| P only | -0.040 | -0.160 | +0.086 |
| -KH (simplicity) | -0.710 | -0.789 | -0.619 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.028 | -0.090 | +0.137 |
| -IAX | -0.186 | -0.254 | -0.110 |
| fitted linear (cross-fitted) | +0.361 | +0.249 | +0.468 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0059, fraction of worlds >0 = 0.37

log(V_driven/V_eq): mean=-0.199 +- 0.016 (s.e. over worlds)


## modular_driven  (worlds=30, structures=900)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.034 | +0.022 | +0.050 |
| C | +0.117 | +0.088 | +0.153 |
| KH | -0.056 | -0.095 | -0.025 |
| IAX | +0.007 | -0.001 | +0.014 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.317 | -0.419 | -0.207 |
| C only | +0.501 | +0.416 | +0.572 |
| P only | +0.053 | -0.025 | +0.138 |
| -KH (simplicity) | -0.493 | -0.577 | -0.402 |
| size (-k) | -0.339 | -0.441 | -0.229 |
| -leak (closure) | +0.199 | +0.129 | +0.282 |
| -IAX | -0.064 | -0.113 | -0.008 |
| fitted linear (cross-fitted) | +0.499 | +0.383 | +0.612 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.019 | -0.142 | +0.171 |
| C only | +0.511 | +0.398 | +0.598 |
| P only | +0.058 | -0.039 | +0.175 |
| -KH (simplicity) | -0.706 | -0.777 | -0.619 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.237 | +0.134 | +0.353 |
| -IAX | -0.054 | -0.107 | +0.010 |
| fitted linear (cross-fitted) | +0.486 | +0.364 | +0.599 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0075, fraction of worlds >0 = 0.30

log(V_driven/V_eq): mean=-0.220 +- 0.017 (s.e. over worlds)

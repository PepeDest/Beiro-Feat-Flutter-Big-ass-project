# E3 report (auto-generated)

Settings: N=6, tau=1.0, p_out=0.01, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=5580)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.022 | +0.015 | +0.030 |
| C | +0.093 | +0.075 | +0.116 |
| KH | -0.084 | -0.111 | -0.060 |
| IAX | -0.002 | -0.008 | +0.004 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.007 | -0.119 | +0.107 |
| C only | +0.249 | +0.161 | +0.336 |
| P only | +0.071 | +0.030 | +0.114 |
| -KH (simplicity) | -0.178 | -0.276 | -0.078 |
| size (-k) | -0.033 | -0.140 | +0.073 |
| -leak (closure) | +0.111 | +0.066 | +0.159 |
| -IAX | -0.097 | -0.121 | -0.072 |
| fitted linear (cross-fitted) | +0.295 | +0.207 | +0.370 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.109 | +0.037 | +0.183 |
| C only | +0.544 | +0.480 | +0.601 |
| P only | +0.129 | +0.077 | +0.183 |
| -KH (simplicity) | -0.692 | -0.738 | -0.649 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.121 | +0.074 | +0.173 |
| -IAX | -0.187 | -0.216 | -0.156 |
| fitted linear (cross-fitted) | +0.478 | +0.413 | +0.541 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0047, fraction of worlds >0 = 0.53

log(V_driven/V_eq): mean=-0.138 +- 0.013 (s.e. over worlds)


## equilibrium  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.071 | +0.055 | +0.091 |
| C | +0.192 | +0.158 | +0.228 |
| KH | -0.248 | -0.293 | -0.211 |
| IAX | -0.058 | -0.078 | -0.041 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.614 | +0.564 | +0.663 |
| C only | -0.224 | -0.302 | -0.134 |
| P only | +0.201 | +0.175 | +0.232 |
| -KH (simplicity) | +0.367 | +0.306 | +0.426 |
| size (-k) | +0.552 | +0.500 | +0.602 |
| -leak (closure) | +0.033 | -0.060 | +0.122 |
| -IAX | -0.198 | -0.228 | -0.169 |
| fitted linear (cross-fitted) | +0.761 | +0.722 | +0.802 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.385 | +0.289 | +0.488 |
| C only | +0.791 | +0.737 | +0.843 |
| P only | +0.266 | +0.210 | +0.316 |
| -KH (simplicity) | -0.838 | -0.877 | -0.794 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.139 | +0.046 | +0.233 |
| -IAX | -0.258 | -0.312 | -0.203 |
| fitted linear (cross-fitted) | +0.694 | +0.592 | +0.782 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0283, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.003 +- 0.005 (s.e. over worlds)


## driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.004 | -0.006 | +0.013 |
| C | +0.064 | +0.031 | +0.102 |
| KH | -0.034 | -0.071 | -0.001 |
| IAX | +0.011 | +0.007 | +0.014 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.262 | -0.372 | -0.137 |
| C only | +0.410 | +0.321 | +0.492 |
| P only | -0.072 | -0.141 | -0.010 |
| -KH (simplicity) | -0.374 | -0.477 | -0.266 |
| size (-k) | -0.251 | -0.360 | -0.126 |
| -leak (closure) | +0.124 | +0.053 | +0.199 |
| -IAX | -0.090 | -0.128 | -0.045 |
| fitted linear (cross-fitted) | +0.422 | +0.326 | +0.507 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.116 | -0.184 | -0.042 |
| C only | +0.403 | +0.322 | +0.484 |
| P only | -0.015 | -0.108 | +0.065 |
| -KH (simplicity) | -0.595 | -0.669 | -0.515 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.074 | -0.008 | +0.153 |
| -IAX | -0.200 | -0.248 | -0.156 |
| fitted linear (cross-fitted) | +0.346 | +0.268 | +0.424 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0047, fraction of worlds >0 = 0.37

log(V_driven/V_eq): mean=-0.185 +- 0.014 (s.e. over worlds)


## modular_driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.037 | +0.029 | +0.047 |
| C | +0.116 | +0.089 | +0.148 |
| KH | -0.056 | -0.092 | -0.026 |
| IAX | -0.001 | -0.005 | +0.004 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.374 | -0.471 | -0.261 |
| C only | +0.562 | +0.498 | +0.615 |
| P only | +0.084 | +0.016 | +0.156 |
| -KH (simplicity) | -0.526 | -0.606 | -0.442 |
| size (-k) | -0.399 | -0.495 | -0.298 |
| -leak (closure) | +0.177 | +0.127 | +0.227 |
| -IAX | -0.003 | -0.038 | +0.033 |
| fitted linear (cross-fitted) | +0.573 | +0.434 | +0.676 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.057 | -0.070 | +0.178 |
| C only | +0.438 | +0.345 | +0.543 |
| P only | +0.137 | +0.054 | +0.214 |
| -KH (simplicity) | -0.643 | -0.720 | -0.560 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.150 | +0.088 | +0.221 |
| -IAX | -0.103 | -0.147 | -0.054 |
| fitted linear (cross-fitted) | +0.502 | +0.413 | +0.592 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0096, fraction of worlds >0 = 0.23

log(V_driven/V_eq): mean=-0.231 +- 0.017 (s.e. over worlds)

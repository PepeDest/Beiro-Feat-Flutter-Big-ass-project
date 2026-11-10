# E3 report (auto-generated)

Settings: N=6, tau=1.0, p_out=0.05, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=5580)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.044 | +0.036 | +0.053 |
| C | +0.163 | +0.141 | +0.195 |
| KH | -0.146 | -0.180 | -0.117 |
| IAX | -0.010 | -0.018 | -0.003 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.109 | +0.019 | +0.195 |
| C only | +0.340 | +0.284 | +0.394 |
| P only | +0.127 | +0.086 | +0.166 |
| -KH (simplicity) | -0.090 | -0.161 | -0.024 |
| size (-k) | -0.026 | -0.103 | +0.054 |
| -leak (closure) | +0.238 | +0.193 | +0.278 |
| -IAX | -0.077 | -0.102 | -0.052 |
| fitted linear (cross-fitted) | +0.434 | +0.357 | +0.507 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.453 | +0.373 | +0.525 |
| C only | +0.634 | +0.583 | +0.684 |
| P only | +0.173 | +0.132 | +0.213 |
| -KH (simplicity) | -0.278 | -0.357 | -0.203 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.252 | +0.196 | +0.308 |
| -IAX | -0.152 | -0.177 | -0.126 |
| fitted linear (cross-fitted) | +0.644 | +0.590 | +0.695 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0182, fraction of worlds >0 = 0.68

log(V_driven/V_eq): mean=-0.141 +- 0.013 (s.e. over worlds)


## equilibrium  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.092 | +0.067 | +0.143 |
| C | +0.292 | +0.259 | +0.332 |
| KH | -0.327 | -0.364 | -0.292 |
| IAX | -0.067 | -0.116 | -0.040 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.549 | +0.507 | +0.589 |
| C only | +0.141 | +0.074 | +0.210 |
| P only | +0.164 | +0.139 | +0.193 |
| -KH (simplicity) | +0.196 | +0.148 | +0.246 |
| size (-k) | +0.344 | +0.304 | +0.385 |
| -leak (closure) | +0.299 | +0.218 | +0.377 |
| -IAX | -0.159 | -0.190 | -0.134 |
| fitted linear (cross-fitted) | +0.718 | +0.680 | +0.761 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.668 | +0.600 | +0.726 |
| C only | +0.865 | +0.835 | +0.893 |
| P only | +0.170 | +0.138 | +0.205 |
| -KH (simplicity) | -0.603 | -0.669 | -0.534 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.425 | +0.347 | +0.498 |
| -IAX | -0.176 | -0.212 | -0.140 |
| fitted linear (cross-fitted) | +0.779 | +0.730 | +0.824 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0533, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.000 +- 0.000 (s.e. over worlds)


## driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.036 | +0.022 | +0.050 |
| C | +0.137 | +0.111 | +0.169 |
| KH | -0.105 | -0.133 | -0.078 |
| IAX | +0.007 | -0.000 | +0.014 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.000 | -0.095 | +0.096 |
| C only | +0.372 | +0.297 | +0.448 |
| P only | +0.111 | +0.026 | +0.196 |
| -KH (simplicity) | -0.134 | -0.214 | -0.042 |
| size (-k) | -0.112 | -0.205 | -0.019 |
| -leak (closure) | +0.176 | +0.094 | +0.251 |
| -IAX | -0.094 | -0.132 | -0.049 |
| fitted linear (cross-fitted) | +0.500 | +0.407 | +0.584 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.387 | +0.286 | +0.485 |
| C only | +0.544 | +0.470 | +0.618 |
| P only | +0.166 | +0.075 | +0.247 |
| -KH (simplicity) | -0.109 | -0.227 | +0.019 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.148 | +0.050 | +0.241 |
| -IAX | -0.185 | -0.226 | -0.136 |
| fitted linear (cross-fitted) | +0.591 | +0.522 | +0.653 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0068, fraction of worlds >0 = 0.67

log(V_driven/V_eq): mean=-0.185 +- 0.013 (s.e. over worlds)


## modular_driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.047 | +0.038 | +0.061 |
| C | +0.129 | +0.106 | +0.164 |
| KH | -0.069 | -0.109 | -0.038 |
| IAX | -0.010 | -0.015 | -0.007 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.223 | -0.319 | -0.108 |
| C only | +0.506 | +0.436 | +0.568 |
| P only | +0.107 | +0.042 | +0.174 |
| -KH (simplicity) | -0.331 | -0.416 | -0.236 |
| size (-k) | -0.310 | -0.402 | -0.201 |
| -leak (closure) | +0.238 | +0.190 | +0.284 |
| -IAX | +0.023 | -0.009 | +0.047 |
| fitted linear (cross-fitted) | +0.550 | +0.442 | +0.653 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.303 | +0.193 | +0.429 |
| C only | +0.492 | +0.412 | +0.578 |
| P only | +0.184 | +0.107 | +0.268 |
| -KH (simplicity) | -0.122 | -0.262 | +0.008 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.182 | +0.104 | +0.260 |
| -IAX | -0.094 | -0.134 | -0.053 |
| fitted linear (cross-fitted) | +0.585 | +0.500 | +0.660 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0055, fraction of worlds >0 = 0.37

log(V_driven/V_eq): mean=-0.237 +- 0.017 (s.e. over worlds)

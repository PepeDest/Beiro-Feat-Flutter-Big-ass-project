# E3 report (auto-generated)

Settings: N=6, tau=2.0, p_out=0.05, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=5580)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.019 | +0.012 | +0.029 |
| C | +0.041 | +0.025 | +0.060 |
| KH | -0.033 | -0.054 | -0.015 |
| IAX | +0.007 | -0.001 | +0.013 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.162 | -0.264 | -0.067 |
| C only | +0.273 | +0.193 | +0.353 |
| P only | +0.101 | +0.063 | +0.146 |
| -KH (simplicity) | -0.192 | -0.289 | -0.101 |
| size (-k) | -0.032 | -0.134 | +0.069 |
| -leak (closure) | +0.079 | +0.028 | +0.130 |
| -IAX | -0.125 | -0.151 | -0.099 |
| fitted linear (cross-fitted) | +0.148 | +0.062 | +0.234 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.572 | -0.635 | -0.513 |
| C only | +0.482 | +0.419 | +0.548 |
| P only | +0.154 | +0.111 | +0.207 |
| -KH (simplicity) | -0.744 | -0.784 | -0.701 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.118 | +0.068 | +0.166 |
| -IAX | -0.202 | -0.230 | -0.173 |
| fitted linear (cross-fitted) | +0.337 | +0.271 | +0.401 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0043, fraction of worlds >0 = 0.53

log(V_driven/V_eq): mean=-0.145 +- 0.013 (s.e. over worlds)


## equilibrium  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.029 | +0.018 | +0.044 |
| C | +0.148 | +0.121 | +0.175 |
| KH | -0.203 | -0.240 | -0.172 |
| IAX | -0.003 | -0.016 | +0.009 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.372 | +0.301 | +0.435 |
| C only | -0.117 | -0.199 | -0.022 |
| P only | +0.224 | +0.196 | +0.257 |
| -KH (simplicity) | +0.309 | +0.244 | +0.369 |
| size (-k) | +0.498 | +0.445 | +0.550 |
| -leak (closure) | -0.020 | -0.109 | +0.067 |
| -IAX | -0.223 | -0.255 | -0.195 |
| fitted linear (cross-fitted) | +0.655 | +0.607 | +0.706 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.467 | -0.576 | -0.356 |
| C only | +0.696 | +0.628 | +0.767 |
| P only | +0.270 | +0.229 | +0.314 |
| -KH (simplicity) | -0.849 | -0.887 | -0.809 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.151 | +0.072 | +0.227 |
| -IAX | -0.279 | -0.321 | -0.239 |
| fitted linear (cross-fitted) | +0.570 | +0.451 | +0.669 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0368, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.000 +- 0.000 (s.e. over worlds)


## driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.006 | -0.003 | +0.013 |
| C | +0.045 | +0.024 | +0.075 |
| KH | -0.010 | -0.038 | +0.013 |
| IAX | +0.018 | +0.012 | +0.022 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.345 | -0.450 | -0.238 |
| C only | +0.378 | +0.276 | +0.483 |
| P only | -0.016 | -0.077 | +0.044 |
| -KH (simplicity) | -0.362 | -0.464 | -0.257 |
| size (-k) | -0.214 | -0.336 | -0.098 |
| -leak (closure) | +0.055 | -0.028 | +0.132 |
| -IAX | -0.137 | -0.187 | -0.088 |
| fitted linear (cross-fitted) | +0.380 | +0.293 | +0.463 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.597 | -0.670 | -0.512 |
| C only | +0.319 | +0.215 | +0.422 |
| P only | +0.029 | -0.042 | +0.091 |
| -KH (simplicity) | -0.670 | -0.736 | -0.604 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.050 | -0.025 | +0.123 |
| -IAX | -0.213 | -0.268 | -0.159 |
| fitted linear (cross-fitted) | +0.284 | +0.207 | +0.361 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0068, fraction of worlds >0 = 0.40

log(V_driven/V_eq): mean=-0.190 +- 0.013 (s.e. over worlds)


## modular_driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.035 | +0.025 | +0.049 |
| C | +0.082 | +0.060 | +0.114 |
| KH | -0.013 | -0.040 | +0.011 |
| IAX | -0.000 | -0.006 | +0.006 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.513 | -0.587 | -0.431 |
| C only | +0.559 | +0.484 | +0.628 |
| P only | +0.093 | +0.020 | +0.179 |
| -KH (simplicity) | -0.524 | -0.600 | -0.443 |
| size (-k) | -0.380 | -0.475 | -0.276 |
| -leak (closure) | +0.202 | +0.145 | +0.260 |
| -IAX | -0.016 | -0.049 | +0.018 |
| fitted linear (cross-fitted) | +0.566 | +0.448 | +0.660 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.654 | -0.734 | -0.562 |
| C only | +0.430 | +0.321 | +0.528 |
| P only | +0.161 | +0.066 | +0.262 |
| -KH (simplicity) | -0.713 | -0.776 | -0.645 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.151 | +0.069 | +0.243 |
| -IAX | -0.113 | -0.152 | -0.069 |
| fitted linear (cross-fitted) | +0.436 | +0.323 | +0.535 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0171, fraction of worlds >0 = 0.20

log(V_driven/V_eq): mean=-0.245 +- 0.019 (s.e. over worlds)

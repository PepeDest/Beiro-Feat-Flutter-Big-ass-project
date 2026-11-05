# E3 report (auto-generated)

Settings: N=6, tau=1.0, p_out=0.05, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=5580)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.031 | +0.023 | +0.040 |
| C | +0.123 | +0.101 | +0.151 |
| KH | -0.111 | -0.144 | -0.085 |
| IAX | -0.000 | -0.007 | +0.006 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.012 | -0.122 | +0.095 |
| C only | +0.255 | +0.169 | +0.342 |
| P only | +0.091 | +0.051 | +0.132 |
| -KH (simplicity) | -0.192 | -0.289 | -0.101 |
| size (-k) | -0.032 | -0.134 | +0.069 |
| -leak (closure) | +0.100 | +0.052 | +0.145 |
| -IAX | -0.125 | -0.151 | -0.099 |
| fitted linear (cross-fitted) | +0.328 | +0.249 | +0.406 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.082 | +0.004 | +0.158 |
| C only | +0.551 | +0.491 | +0.607 |
| P only | +0.135 | +0.087 | +0.180 |
| -KH (simplicity) | -0.744 | -0.784 | -0.701 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.108 | +0.064 | +0.158 |
| -IAX | -0.202 | -0.230 | -0.173 |
| fitted linear (cross-fitted) | +0.480 | +0.416 | +0.542 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0064, fraction of worlds >0 = 0.58

log(V_driven/V_eq): mean=-0.145 +- 0.013 (s.e. over worlds)


## equilibrium  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.066 | +0.045 | +0.092 |
| C | +0.242 | +0.202 | +0.288 |
| KH | -0.300 | -0.354 | -0.254 |
| IAX | -0.044 | -0.070 | -0.022 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.561 | +0.509 | +0.616 |
| C only | -0.176 | -0.252 | -0.087 |
| P only | +0.226 | +0.199 | +0.260 |
| -KH (simplicity) | +0.309 | +0.244 | +0.369 |
| size (-k) | +0.498 | +0.445 | +0.550 |
| -leak (closure) | +0.016 | -0.072 | +0.105 |
| -IAX | -0.223 | -0.255 | -0.195 |
| fitted linear (cross-fitted) | +0.731 | +0.688 | +0.772 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.366 | +0.254 | +0.478 |
| C only | +0.775 | +0.724 | +0.826 |
| P only | +0.275 | +0.234 | +0.319 |
| -KH (simplicity) | -0.849 | -0.887 | -0.809 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.117 | +0.040 | +0.196 |
| -IAX | -0.279 | -0.321 | -0.239 |
| fitted linear (cross-fitted) | +0.697 | +0.601 | +0.778 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0333, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.000 +- 0.000 (s.e. over worlds)


## driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.010 | -0.000 | +0.021 |
| C | +0.093 | +0.061 | +0.136 |
| KH | -0.058 | -0.099 | -0.025 |
| IAX | +0.017 | +0.012 | +0.022 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.228 | -0.345 | -0.113 |
| C only | +0.389 | +0.291 | +0.487 |
| P only | -0.030 | -0.099 | +0.038 |
| -KH (simplicity) | -0.362 | -0.464 | -0.257 |
| size (-k) | -0.214 | -0.336 | -0.098 |
| -leak (closure) | +0.111 | +0.040 | +0.182 |
| -IAX | -0.137 | -0.187 | -0.088 |
| fitted linear (cross-fitted) | +0.426 | +0.332 | +0.523 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.116 | -0.209 | -0.014 |
| C only | +0.435 | +0.338 | +0.532 |
| P only | -0.008 | -0.110 | +0.084 |
| -KH (simplicity) | -0.670 | -0.736 | -0.604 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.083 | +0.011 | +0.156 |
| -IAX | -0.213 | -0.268 | -0.159 |
| fitted linear (cross-fitted) | +0.366 | +0.274 | +0.463 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0039, fraction of worlds >0 = 0.47

log(V_driven/V_eq): mean=-0.190 +- 0.013 (s.e. over worlds)


## modular_driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.049 | +0.038 | +0.060 |
| C | +0.144 | +0.111 | +0.186 |
| KH | -0.075 | -0.116 | -0.039 |
| IAX | -0.002 | -0.006 | +0.005 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.371 | -0.461 | -0.266 |
| C only | +0.552 | +0.488 | +0.608 |
| P only | +0.076 | +0.004 | +0.148 |
| -KH (simplicity) | -0.524 | -0.600 | -0.443 |
| size (-k) | -0.380 | -0.475 | -0.276 |
| -leak (closure) | +0.173 | +0.117 | +0.232 |
| -IAX | -0.016 | -0.049 | +0.018 |
| fitted linear (cross-fitted) | +0.578 | +0.456 | +0.680 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.004 | -0.145 | +0.134 |
| C only | +0.442 | +0.352 | +0.540 |
| P only | +0.136 | +0.063 | +0.209 |
| -KH (simplicity) | -0.713 | -0.776 | -0.645 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.124 | +0.048 | +0.203 |
| -IAX | -0.113 | -0.152 | -0.069 |
| fitted linear (cross-fitted) | +0.492 | +0.403 | +0.590 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0101, fraction of worlds >0 = 0.27

log(V_driven/V_eq): mean=-0.245 +- 0.019 (s.e. over worlds)

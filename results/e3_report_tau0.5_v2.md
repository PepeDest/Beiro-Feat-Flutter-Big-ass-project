# E3 report (auto-generated)

Settings: N=6, tau=0.5, p_out=0.05, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=5580)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.041 | +0.032 | +0.052 |
| C | +0.251 | +0.217 | +0.296 |
| KH | -0.238 | -0.283 | -0.195 |
| IAX | -0.001 | -0.007 | +0.006 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.226 | +0.118 | +0.329 |
| C only | +0.251 | +0.155 | +0.348 |
| P only | +0.014 | -0.033 | +0.064 |
| -KH (simplicity) | -0.192 | -0.289 | -0.101 |
| size (-k) | -0.032 | -0.134 | +0.069 |
| -leak (closure) | +0.192 | +0.142 | +0.236 |
| -IAX | -0.125 | -0.151 | -0.099 |
| fitted linear (cross-fitted) | +0.496 | +0.428 | +0.571 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.501 | +0.443 | +0.558 |
| C only | +0.694 | +0.647 | +0.734 |
| P only | +0.051 | -0.006 | +0.113 |
| -KH (simplicity) | -0.744 | -0.784 | -0.701 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.224 | +0.177 | +0.273 |
| -IAX | -0.202 | -0.230 | -0.173 |
| fitted linear (cross-fitted) | +0.651 | +0.604 | +0.693 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0086, fraction of worlds >0 = 0.67

log(V_driven/V_eq): mean=-0.145 +- 0.013 (s.e. over worlds)


## equilibrium  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.188 | +0.135 | +0.256 |
| C | +0.394 | +0.320 | +0.478 |
| KH | -0.460 | -0.555 | -0.378 |
| IAX | -0.169 | -0.238 | -0.116 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.756 | +0.724 | +0.791 |
| C only | -0.249 | -0.320 | -0.170 |
| P only | +0.224 | +0.198 | +0.256 |
| -KH (simplicity) | +0.309 | +0.244 | +0.369 |
| size (-k) | +0.498 | +0.445 | +0.550 |
| -leak (closure) | +0.014 | -0.071 | +0.099 |
| -IAX | -0.223 | -0.255 | -0.195 |
| fitted linear (cross-fitted) | +0.780 | +0.743 | +0.815 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.695 | +0.644 | +0.750 |
| C only | +0.821 | +0.774 | +0.863 |
| P only | +0.276 | +0.237 | +0.321 |
| -KH (simplicity) | -0.849 | -0.887 | -0.809 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.070 | -0.001 | +0.148 |
| -IAX | -0.279 | -0.321 | -0.239 |
| fitted linear (cross-fitted) | +0.791 | +0.741 | +0.835 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0213, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.000 +- 0.000 (s.e. over worlds)


## driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.017 | +0.005 | +0.032 |
| C | +0.182 | +0.137 | +0.234 |
| KH | -0.147 | -0.194 | -0.103 |
| IAX | +0.017 | +0.009 | +0.024 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.038 | -0.161 | +0.088 |
| C only | +0.410 | +0.308 | +0.512 |
| P only | -0.128 | -0.192 | -0.074 |
| -KH (simplicity) | -0.362 | -0.464 | -0.257 |
| size (-k) | -0.214 | -0.336 | -0.098 |
| -leak (closure) | +0.228 | +0.163 | +0.293 |
| -IAX | -0.137 | -0.187 | -0.088 |
| fitted linear (cross-fitted) | +0.549 | +0.465 | +0.633 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.335 | +0.261 | +0.418 |
| C only | +0.604 | +0.518 | +0.685 |
| P only | -0.088 | -0.165 | -0.008 |
| -KH (simplicity) | -0.670 | -0.736 | -0.604 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.245 | +0.168 | +0.321 |
| -IAX | -0.213 | -0.268 | -0.159 |
| fitted linear (cross-fitted) | +0.537 | +0.454 | +0.616 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0017, fraction of worlds >0 = 0.57

log(V_driven/V_eq): mean=-0.190 +- 0.013 (s.e. over worlds)


## modular_driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.054 | +0.039 | +0.069 |
| C | +0.256 | +0.207 | +0.317 |
| KH | -0.186 | -0.247 | -0.134 |
| IAX | +0.003 | -0.004 | +0.014 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.041 | -0.154 | +0.078 |
| C only | +0.592 | +0.527 | +0.652 |
| P only | -0.053 | -0.140 | +0.032 |
| -KH (simplicity) | -0.524 | -0.600 | -0.443 |
| size (-k) | -0.380 | -0.475 | -0.276 |
| -leak (closure) | +0.335 | +0.300 | +0.378 |
| -IAX | -0.016 | -0.049 | +0.018 |
| fitted linear (cross-fitted) | +0.694 | +0.587 | +0.776 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.474 | +0.369 | +0.578 |
| C only | +0.656 | +0.585 | +0.724 |
| P only | -0.037 | -0.132 | +0.058 |
| -KH (simplicity) | -0.713 | -0.776 | -0.645 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.357 | +0.296 | +0.421 |
| -IAX | -0.113 | -0.152 | -0.069 |
| fitted linear (cross-fitted) | +0.629 | +0.554 | +0.703 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0027, fraction of worlds >0 = 0.43

log(V_driven/V_eq): mean=-0.245 +- 0.019 (s.e. over worlds)

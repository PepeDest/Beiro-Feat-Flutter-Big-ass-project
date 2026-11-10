# E3 report (auto-generated)

Settings: N=6, tau=1.0, p_out=0.01, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=5580)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.030 | +0.021 | +0.040 |
| C | +0.125 | +0.104 | +0.153 |
| KH | -0.133 | -0.165 | -0.107 |
| IAX | -0.001 | -0.009 | +0.005 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.099 | -0.003 | +0.208 |
| C only | +0.140 | +0.060 | +0.221 |
| P only | +0.079 | +0.038 | +0.118 |
| -KH (simplicity) | -0.076 | -0.161 | +0.020 |
| size (-k) | +0.086 | -0.008 | +0.184 |
| -leak (closure) | +0.092 | +0.043 | +0.143 |
| -IAX | -0.114 | -0.140 | -0.087 |
| fitted linear (cross-fitted) | +0.319 | +0.234 | +0.403 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.069 | -0.012 | +0.143 |
| C only | +0.541 | +0.481 | +0.600 |
| P only | +0.142 | +0.092 | +0.191 |
| -KH (simplicity) | -0.745 | -0.788 | -0.703 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.102 | +0.055 | +0.146 |
| -IAX | -0.202 | -0.234 | -0.170 |
| fitted linear (cross-fitted) | +0.449 | +0.381 | +0.521 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0124, fraction of worlds >0 = 0.63

log(V_driven/V_eq): mean=-0.139 +- 0.013 (s.e. over worlds)


## equilibrium  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.078 | +0.053 | +0.107 |
| C | +0.242 | +0.204 | +0.287 |
| KH | -0.322 | -0.372 | -0.278 |
| IAX | -0.058 | -0.088 | -0.033 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.635 | +0.587 | +0.682 |
| C only | -0.265 | -0.347 | -0.176 |
| P only | +0.204 | +0.170 | +0.238 |
| -KH (simplicity) | +0.399 | +0.341 | +0.463 |
| size (-k) | +0.581 | +0.532 | +0.632 |
| -leak (closure) | +0.016 | -0.087 | +0.109 |
| -IAX | -0.202 | -0.238 | -0.167 |
| fitted linear (cross-fitted) | +0.757 | +0.715 | +0.801 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.369 | +0.254 | +0.485 |
| C only | +0.779 | +0.704 | +0.846 |
| P only | +0.277 | +0.226 | +0.329 |
| -KH (simplicity) | -0.850 | -0.884 | -0.810 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.130 | +0.042 | +0.217 |
| -IAX | -0.278 | -0.330 | -0.225 |
| fitted linear (cross-fitted) | +0.685 | +0.570 | +0.783 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0392, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.000 +- 0.000 (s.e. over worlds)


## driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.008 | -0.003 | +0.019 |
| C | +0.095 | +0.063 | +0.137 |
| KH | -0.081 | -0.124 | -0.045 |
| IAX | +0.016 | +0.011 | +0.020 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.078 | -0.194 | +0.054 |
| C only | +0.232 | +0.124 | +0.333 |
| P only | -0.042 | -0.109 | +0.018 |
| -KH (simplicity) | -0.205 | -0.317 | -0.089 |
| size (-k) | -0.054 | -0.181 | +0.074 |
| -leak (closure) | +0.080 | +0.008 | +0.154 |
| -IAX | -0.125 | -0.170 | -0.077 |
| fitted linear (cross-fitted) | +0.323 | +0.203 | +0.446 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.137 | -0.238 | -0.032 |
| C only | +0.404 | +0.310 | +0.493 |
| P only | +0.011 | -0.085 | +0.094 |
| -KH (simplicity) | -0.662 | -0.734 | -0.591 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.059 | -0.016 | +0.136 |
| -IAX | -0.223 | -0.274 | -0.171 |
| fitted linear (cross-fitted) | +0.341 | +0.239 | +0.435 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0024, fraction of worlds >0 = 0.60

log(V_driven/V_eq): mean=-0.186 +- 0.013 (s.e. over worlds)


## modular_driven  (worlds=30, structures=1860)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.049 | +0.036 | +0.062 |
| C | +0.147 | +0.113 | +0.189 |
| KH | -0.097 | -0.137 | -0.058 |
| IAX | -0.002 | -0.006 | +0.004 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.261 | -0.351 | -0.159 |
| C only | +0.452 | +0.386 | +0.508 |
| P only | +0.075 | +0.003 | +0.152 |
| -KH (simplicity) | -0.423 | -0.501 | -0.337 |
| size (-k) | -0.269 | -0.366 | -0.164 |
| -leak (closure) | +0.180 | +0.128 | +0.228 |
| -IAX | -0.015 | -0.044 | +0.013 |
| fitted linear (cross-fitted) | +0.512 | +0.395 | +0.621 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.025 | -0.163 | +0.104 |
| C only | +0.440 | +0.341 | +0.532 |
| P only | +0.137 | +0.053 | +0.215 |
| -KH (simplicity) | -0.722 | -0.783 | -0.652 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.117 | +0.057 | +0.186 |
| -IAX | -0.105 | -0.150 | -0.056 |
| fitted linear (cross-fitted) | +0.463 | +0.360 | +0.561 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0042, fraction of worlds >0 = 0.30

log(V_driven/V_eq): mean=-0.231 +- 0.017 (s.e. over worlds)

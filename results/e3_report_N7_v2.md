# E3 report (auto-generated)

Settings: N=7, tau=1.0, p_out=0.05, n_worlds/family=30, n_traj=600, dt=0.05, t_max=200.0


## ALL families  (worlds=90, structures=11340)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.018 | +0.010 | +0.028 |
| C | +0.053 | +0.030 | +0.086 |
| KH | -0.049 | -0.078 | -0.026 |
| IAX | +0.008 | -0.001 | +0.015 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.036 | -0.147 | +0.077 |
| C only | +0.241 | +0.145 | +0.339 |
| P only | +0.105 | +0.071 | +0.137 |
| -KH (simplicity) | -0.197 | -0.297 | -0.096 |
| size (-k) | -0.054 | -0.162 | +0.053 |
| -leak (closure) | +0.092 | +0.052 | +0.134 |
| -IAX | -0.119 | -0.146 | -0.093 |
| fitted linear (cross-fitted) | +0.200 | +0.124 | +0.280 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.080 | -0.003 | +0.165 |
| C only | +0.570 | +0.531 | +0.610 |
| P only | +0.163 | +0.123 | +0.202 |
| -KH (simplicity) | -0.768 | -0.794 | -0.741 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.088 | +0.047 | +0.132 |
| -IAX | -0.196 | -0.229 | -0.161 |
| fitted linear (cross-fitted) | +0.467 | +0.417 | +0.507 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0046, fraction of worlds >0 = 0.44

log(V_driven/V_eq): mean=-0.154 +- 0.013 (s.e. over worlds)


## equilibrium  (worlds=30, structures=3780)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.020 | -0.009 | +0.049 |
| C | +0.209 | +0.152 | +0.271 |
| KH | -0.284 | -0.349 | -0.223 |
| IAX | +0.005 | -0.023 | +0.029 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.651 | +0.613 | +0.692 |
| C only | -0.328 | -0.399 | -0.262 |
| P only | +0.229 | +0.196 | +0.268 |
| -KH (simplicity) | +0.414 | +0.365 | +0.468 |
| size (-k) | +0.577 | +0.536 | +0.624 |
| -leak (closure) | -0.046 | -0.140 | +0.027 |
| -IAX | -0.231 | -0.271 | -0.196 |
| fitted linear (cross-fitted) | +0.729 | +0.662 | +0.782 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | +0.443 | +0.375 | +0.515 |
| C only | +0.747 | +0.689 | +0.795 |
| P only | +0.301 | +0.251 | +0.362 |
| -KH (simplicity) | -0.838 | -0.862 | -0.808 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.049 | -0.045 | +0.126 |
| -IAX | -0.306 | -0.368 | -0.253 |
| fitted linear (cross-fitted) | +0.696 | +0.637 | +0.748 |

Price selection term Cov(w/wbar, Phi_orig): mean=+0.0369, fraction of worlds >0 = 1.00

log(V_driven/V_eq): mean=+0.000 +- 0.000 (s.e. over worlds)


## driven  (worlds=30, structures=3780)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.016 | +0.009 | +0.024 |
| C | +0.078 | +0.056 | +0.114 |
| KH | -0.029 | -0.062 | -0.008 |
| IAX | +0.012 | +0.008 | +0.016 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.344 | -0.444 | -0.218 |
| C only | +0.481 | +0.386 | +0.557 |
| P only | +0.005 | -0.049 | +0.053 |
| -KH (simplicity) | -0.466 | -0.555 | -0.349 |
| size (-k) | -0.332 | -0.432 | -0.204 |
| -leak (closure) | +0.102 | +0.045 | +0.151 |
| -IAX | -0.105 | -0.147 | -0.069 |
| fitted linear (cross-fitted) | +0.524 | +0.422 | +0.607 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.098 | -0.227 | +0.014 |
| C only | +0.469 | +0.404 | +0.529 |
| P only | +0.028 | -0.033 | +0.084 |
| -KH (simplicity) | -0.731 | -0.774 | -0.682 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.042 | -0.025 | +0.107 |
| -IAX | -0.199 | -0.249 | -0.152 |
| fitted linear (cross-fitted) | +0.498 | +0.438 | +0.559 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0103, fraction of worlds >0 = 0.20

log(V_driven/V_eq): mean=-0.230 +- 0.015 (s.e. over worlds)


## modular_driven  (worlds=30, structures=3780)

Standardised coefficients (d log V per +1 SD, within-world), 95% cluster bootstrap CI:

| feature | coef | CI low | CI high |
|---|---|---|---|
| P | +0.035 | +0.028 | +0.044 |
| C | +0.105 | +0.092 | +0.126 |
| KH | -0.043 | -0.069 | -0.024 |
| IAX | -0.002 | -0.006 | +0.002 |

Mean within-world Spearman rho (score vs log V):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.414 | -0.503 | -0.326 |
| C only | +0.568 | +0.508 | +0.628 |
| P only | +0.082 | +0.025 | +0.140 |
| -KH (simplicity) | -0.539 | -0.610 | -0.468 |
| size (-k) | -0.407 | -0.497 | -0.322 |
| -leak (closure) | +0.219 | +0.183 | +0.263 |
| -IAX | -0.021 | -0.056 | +0.007 |
| fitted linear (cross-fitted) | +0.610 | +0.523 | +0.678 |

Same, but ranking only among structures OF EQUAL SIZE (controls the size confound):

| score | rho | CI low | CI high |
|---|---|---|---|
| Phi_orig(b=1,l=.25) | -0.103 | -0.252 | +0.044 |
| C only | +0.495 | +0.437 | +0.555 |
| P only | +0.160 | +0.093 | +0.234 |
| -KH (simplicity) | -0.734 | -0.775 | -0.681 |
| size (-k) | +nan | +nan | +nan |
| -leak (closure) | +0.174 | +0.111 | +0.231 |
| -IAX | -0.082 | -0.130 | -0.040 |
| fitted linear (cross-fitted) | +0.557 | +0.491 | +0.621 |

Price selection term Cov(w/wbar, Phi_orig): mean=-0.0129, fraction of worlds >0 = 0.13

log(V_driven/V_eq): mean=-0.233 +- 0.013 (s.e. over worlds)

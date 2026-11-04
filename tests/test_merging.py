from itertools import permutations
from vlife.functional import all_subsets, merge_pairs


def test_merge_pairs_keeps_every_eligible_pair_once():
    # Fix #2 (docs/code_review.md): E4 must use all unordered disjoint pairs with |A u B| <= min(5, N - 1).
    for N, expected in ((5, 75), (6, 270), (7, 686)):
        subs = all_subsets(N)
        pairs = merge_pairs(subs, N, 5)
        assert len(pairs) == expected
        keys = {frozenset((a, b)) for a, b in pairs}
        assert len(keys) == len(pairs)                                    # no pair twice
        assert all(not set(a) & set(b) and len(a) + len(b) <= min(5, N - 1) for a, b in pairs)
        brute = {frozenset((a, b)) for a in subs for b in subs
                 if a != b and not set(a) & set(b) and len(a) + len(b) <= min(5, N - 1)}
        assert keys == brute                                              # nothing missing


def test_merge_pairs_do_not_depend_on_variable_labels():
    # The old filter min(a) > min(b) kept or dropped a pair depending on the variable index. Relabelling the
    # variables must map the pair set onto itself.
    N = 6; subs = all_subsets(N)
    base = {frozenset((a, b)) for a, b in merge_pairs(subs, N, 5)}
    for perm in list(permutations(range(N)))[::97]:
        relab = lambda s: tuple(sorted(perm[i] for i in s))
        assert {frozenset((relab(a), relab(b))) for a, b in (tuple(p) for p in base)} == base

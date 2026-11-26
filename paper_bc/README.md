# Paper B and C: arXiv source (draft 2)

This folder holds the second paper: semantic information in linear Gaussian systems (niche B) and the negative
controls (niche C). Every number comes from `docs/B.md`, `docs/C.md` and the reports in `results/`.

| File | What |
|---|---|
| `main.tex` | The paper (LaTeX, `article` class, 11 pt, 1 inch margins, single column) |
| `refs.bib` | The bibliography |
| `figures/` | The two figures (PDF and PNG) |
| `make_figures.py` | Makes the figures from the result files. Run it from the repository root |
| `abstract_arxiv.txt` | The abstract as plain ASCII text for the arXiv field (limit 1920 characters) |

The figure of the C2 units needs `results/e26_units.csv` (the class and the life of each unit). The script
`experiments/e26b_export_units.py` writes it from the rebuilt C2 data.

## State of draft 2 (2026-11-26)
- All sections have text. There are two figures.
- This PC has no TeX. The draft is not compiled. A script checked the citations, the labels, the environments and the
  braces. A second script checked that each number of the text is in the step documents or the reports.
- `Massey90` is a conference paper with no DOI. We did not check it against a catalogue.
- `Beiro26` is the first paper (`paper/`). It has no arXiv number yet. Put the number in `refs.bib` when it exists.

## Review of draft 1 (as a referee), and what changed
1. The homeostat had no equations, so a reader could not check the proof of Proposition 6. Draft 2 adds them
   (Eq. of Sec. 5), from `src/vlife/agency.py`.
2. Proposition 1 said that every P comes from a garbling, with no construction. Draft 2 gives one, and it allows a
   noise covariance that is only positive semidefinite (projections need zero noise).
3. Draft 1 said "395 organisms count" with no reason. Draft 2 says that these are the organisms that the companion
   study keeps.
4. Draft 1 called V concave in P. It is convex. This was fixed in draft 1, before the commit.

## Open points for the author
1. Compile the draft (Overleaf, pdfLaTeX) and fix any LaTeX error.
2. The proofs of Propositions 1 to 6 are short. A referee can ask for the full Gaussian computation of Proposition 1
   in an appendix.
3. The bound of the observed form after the first step is numerical only. The text says so.
4. Choose the arXiv categories (`cond-mat.stat-mech` or `physics.bio-ph`, with `cs.IT` as a cross-list).

## Build the PDF
On Overleaf: upload this folder and compile with pdfLaTeX. With a TeX distribution:

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

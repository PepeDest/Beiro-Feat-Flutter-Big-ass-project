# Paper B and C: arXiv source (draft 1)

This folder holds the second paper: semantic information in linear Gaussian systems (niche B) and the negative
controls (niche C). Every number comes from `docs/B.md`, `docs/C.md` and the reports in `results/`.

| File | What |
|---|---|
| `main.tex` | The paper (LaTeX, `article` class, 11 pt, 1 inch margins, single column) |
| `refs.bib` | The bibliography |
| `abstract_arxiv.txt` | The abstract as plain ASCII text for the arXiv field (limit 1920 characters) |

## State of draft 1 (2026-11-26)
- All sections have text. There are no figures yet.
- This PC has no TeX. The draft is not compiled. A script checked the citations, the labels, the environments and the
  braces. A second script checked that each number of the text is in the step documents or the reports.
- `Massey90` is a conference paper with no DOI. We did not check it against a catalogue.
- `Beiro26` is the first paper (`paper/`). It has no arXiv number yet. Put the number in `refs.bib` when it exists.

## Build the PDF
On Overleaf: upload this folder and compile with pdfLaTeX. With a TeX distribution:

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

## Still to do
1. Compile the draft and fix any LaTeX error.
2. Add figures: the B2 gap between projections and garblings, and the C2 curves of CLD for rocks and oscillators.
3. Read the draft as a referee would and check each claim against its rule.
4. Choose the arXiv categories (`cond-mat.stat-mech` or `physics.bio-ph`, with `cs.IT` as a cross-list).

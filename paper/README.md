# Paper: arXiv source

| File | What |
|---|---|
| `main.tex` | The paper (LaTeX, `article` class, 11 pt, 1 inch margins, single column) |
| `refs.bib` | The bibliography. arXiv runs BibTeX on it |
| `figures/` | The three figures (PDF and PNG, as pdfLaTeX needs) |
| `make_figures.py` | Makes `fig_s1.pdf` and `fig_s6.pdf` from the reports, and copies `fig_s3.png` |
| `abstract_arxiv.txt` | The abstract as plain ASCII text for the arXiv abstract field (limit 1920 characters) |

## Build the PDF

With a TeX distribution (TeX Live, MiKTeX or Tectonic), from this folder:

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

With Tectonic: `tectonic main.tex`. On Overleaf: upload this folder and compile with pdfLaTeX.

## Upload to arXiv

1. Make a `.zip` of `main.tex`, `refs.bib` and `figures/`. Do not include `.aux`, `.log` or `.pdf` files.
2. Title: copy it from `main.tex`. Do not write it in capital letters.
3. Authors: `Alexander Beiro`.
4. Abstract: paste `abstract_arxiv.txt`. Do not write the word "Abstract".
5. Categories: `physics.bio-ph` as primary, with `cond-mat.stat-mech` and `q-bio.PE` as cross-lists.
6. A first submission to a category needs an endorsement from an arXiv author in that area.

The code and data link in the paper must point to a public repository.

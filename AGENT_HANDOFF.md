# Agent Handoff — Editing Context (May 2026)

This file captures the editing state of the thesis as of the May 2026 macOS-side
work, written for the next agent picking it up on the slurm side. Read
`THESIS_INSTRUCTIONS.md` first for project framing and writing-style rules; this
file is just the recent state.

## Recent commits at the top of `main`

```
282d2c0 figures: tikz tooling and split pipeline figure into preparation + coupled-solve
31d7dd2 build: UiO master-thesis cover via local uiomasterfp template
4c75f9c polish: thesis content, reference-tag postprocessing section, per-case canonical caveat
08a46a9 results: update capped sweep figures and preview setup
acdcd89 methods: clarify ED-zeroed longitudinal strain
c2bdfe8 appendix: clarify capped and pre-cap sweep evidence
b49e08a results: restore capped principal-strain alignment
```

The earlier four are slurm-side (results agent). The top three are macOS-side
(this hand-off). The two streams have been merged cleanly on `main`.

## The single most important conceptual thing

**`reference-tag postprocessing` vs `per-case canonical postprocessing`.**

- *Reference-tag* is the preferred protocol: one fixed reference end-diastolic
  mesh, one set of LV/RV/septum cell tags, reused across every sweep case. Only
  the circulation changes from one case to the next. Defined in chapter 3 at
  `(sec-reference-tag-postprocessing)=` in `03_implementation/implementation.md`.
- *Per-case canonical* is what the **current** chapter-5 figures and chapter-8
  appendix tables are produced under: each capped sweep case is independently
  tetrahedralised (cell counts vary 7936--8109), tagged on its own ED mesh, and
  integrated.
- A **reference-tag rerun is in progress on slurm**. Both chapter 3 and the
  chapter 5 opener already flag this with caveat paragraphs. When the rerun
  lands, update the chapter-5 numbers, the appendix audit row, and lift the
  caveat. Conclusions are not expected to change qualitatively.

## Chapter status

| Chapter | State | Touch with care? |
|---|---|---|
| `intro.md` | Polished. Subtitle split out for the UiO cover. | Yes — don't put chapter-1 content back in. |
| `01_the_question/` | Polished. Strain-direction story consolidated, energy identity moved to appendix. | Yes — don't re-introduce content from intro. |
| `02_the_model/*.md` | All six files polished section-by-section. | **Yes — strongly. Recent reductions were deliberate. Don't revert.** |
| `03_implementation/...` | Has the new `Reference-Tag Postprocessing` section. Per-case-canonical caveat present. | Treat the ref-tag section as canonical for the term. |
| `04_tuning/...` | Capped-sweep updates done by results agent. | OK to polish. |
| `05_results/...` | Mostly results-agent's content. Polish edits applied. Opener now flags ref-tag pending. | Coordinate with the rerun results — don't re-edit numbers until the rerun lands. |
| `06_discussion/...` | Capped-sweep updates done. The cap-justification paragraph runs slightly long; tighten if you want. | OK to polish. |
| `07_conclusion/...` | Capped-sweep updates done. | OK to polish. |
| `08_appendix/...` | `circulation_calibration.md`, `numerical_robustness.md`, `energy_identity_derivation.md`. The third was created when stress-power algebra was moved out of chapter 2. | Numerical-robustness audit row is the natural place to update when the rerun lands. |

## UiO build (don't break this)

Building `myst build --pdf` from the project root produces a UiO master-thesis
PDF at `_build/exports/thesis.pdf`. The export is wired through a local template
at `_templates/uio_thesis/`:

- `template.tex` — report-class with a `\section -> \chapter` remap (so MyST's
  flat heading stream produces conventional thesis chapter formatting), 1in
  margins, the official UiO front-page block via `\uiomasterfp[…]`.
- `template.yml` — declares the template options used by `myst.yml`.
- `uiomasterfp.sty`, `uio-fp-navn-eng.pdf`, `uio-fp-segl.pdf` — the official UiO
  package and logos. **Don't lose these on a clean build.**
- The preface and the AI declaration are **hardcoded in `template.tex`** as
  `\chapter*{}` blocks. Edit them there, not in markdown. Reason: MyST's `parts`
  mechanism only honours `abstract` natively, so custom front-matter chapters
  (`preface`, `ai_declaration`) wouldn't surface into the template via parts.

`landing.md` exists with an empty body. It is the project's TOC root — its
purpose is to make `intro.md` a regular chapter rather than the project's
landing page. Don't add content to it.

UiO cover-page metadata is set in `myst.yml` under `project.exports[0]`:
title, subtitle, supervisors, programme, department, faculty, colour. **Confirm
with Daniel before changing any of these** — they appear on the official cover.

## Style preferences (compact form)

Read `THESIS_INSTRUCTIONS.md` for the long version. The short version:

- Prose, not bullets, in scientific content.
- UK English. Math foreground.
- No adverb padding ("very", "extremely", "highly"). No melodrama. No "leverage",
  no "sounding board", no "hidden hero", no "relentless rise".
- Sparse subheadings — only between genuinely distinct topics.
- Equations embedded in sentences, with notation explained.
- "We" is fine; pure passive voice is often weaker than active.
- Don't conjure citations. If a benchmark needs one and you don't have a
  source, leave `[ADD CITATION]` inline so Daniel can find it.
- Daniel often says "go ahead" with minimal qualification — honour that without
  re-asking, but flag genuinely surprising design choices before making them.

## Tools and conventions

- Push to `main` directly. No PR workflow.
- Slurm side has the simulation runs and figure scripts. The repo has
  `scripts/tikz/` for thesis-side TikZ figures (`python scripts/tikz/build_tikz.py`
  to regenerate). Each `.tex` file in there compiles with pdflatex and
  rasterises to PNG via pdftocairo.
- `references.bib` at the repo root.
- `[ADD CITATION]` is the convention for pending citations.
- File-reference convention in markdown: use markdown links like
  `[filename.md](path/to/filename.md)` for clickable navigation.

## Likely next moves

1. When the reference-tag rerun lands: refresh chapter-5 numbers and tables,
   update the chapter-3 / chapter-5 caveats to past-tense ("the rerun is now
   complete"), update the appendix-table row.
2. Discussion chapter cap-justification paragraph is slightly long.
3. Final-pass polish: any remaining `[ADD CITATION]` markers, figure-width
   unification across chapters, figure-ID renumbering (currently has gaps from
   deleted `fig_2_2`).
4. Whatever Daniel asks for.

## How to ask before acting

- Word-level edits and short polish: just do them.
- Larger restructures (move a section to another chapter, add a new chapter,
  reorder front matter): flag first.
- UiO cover-page metadata: confirm before touching.
- Any change that affects which results are reported (re-running figures,
  swapping result sets, changing simulation outputs into the thesis): confirm
  before doing.

## Sanity checks before pushing

- `myst build --pdf` succeeds and produces `_build/exports/thesis.pdf`.
- No `<<<<<<<` or `>>>>>>>` markers remain in any thesis file.
- `git status` is clean after the commit.
- If touching the UiO template or anything in `_templates/`, render the cover
  page locally to confirm it still looks right.

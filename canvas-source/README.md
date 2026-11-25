# Canvas source: the Writing EOS front end

The Writing EOS design canvas, the app's front end: 19 screens (boards) and the canvas layout. The live canvas is the
claude.ai artifact *Writing EOS App* (https://claude.ai/artifact/HL7wfJWnqk7QcLaBFjdUGZ); this folder is its copy in
the repository.

- `eos-design/project/`: the boards (`*.dc.html`) and `canvas.json`, **copied from the live canvas on
  2026-11-25** (live version `1795611737-263e`, last changed 2026-11-12). Each file's SHA-256 matches the live one.
- `eos-build/`: `build.py` and the per-board sources in `src/`, as of **2026-10-22**.
- `dcpreview/`, `jscheck.py`: preview and check tools.

The artifact platform's own runtime (its `app.js`, `dc-runtime.js`, fonts and translations) comes with the artifact
type and is not the app's code, so it is not copied here.

## Do not run `build.py` as it stands

The boards were corrected on the live canvas after `src/` was written, so `src/` is older than the boards:

- On 2026-11-12 nine boards were corrected on the live canvas only (fixes plan, C2): Blueprint, Model Lab, Library,
  Finish and publish, Home, Story Blueprint, Chapters, Recipes and Autonomy.
- The same day the four quality tiers were taken off six boards (Generate, Recipes, Model Lab, Blueprint, Chapters,
  Editor) after decision D32.

`build.py` writes every board that has a source in `src/` (Autonomy, Bible, Board, Develop, Draft, Ecosystem,
Export, Finish, Generate, Genre, History, Lab, Library, Recipes). Running it would put the October wording back on
eight boards: Autonomy, Develop, Ecosystem, Finish, Generate, Lab, Library and Recipes. Chapter, Editor, Main, Sidebar
and System have no source in `src/`; they exist only as boards.

So the boards in `eos-design/project/` are the current front end. Edit them, or bring `src/` up to date from them
first, before building again.

## Updating this copy

When the live canvas changes, copy its `project/` files over `eos-design/project/` and check each SHA-256 against the
artifact's file list.

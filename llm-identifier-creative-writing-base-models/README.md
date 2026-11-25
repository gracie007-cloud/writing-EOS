# LLM Identifier for Creative Writing: Base Models for Fine-Tuning

Complete catalog of **204 unique Hugging Face GGUF creative-writing models**, mapped to:
- **8 Broader Genre Categories** (`Category A` through `Category H`)
- **Exact Minor/Major Subgenres** from the Genre Matrix taxonomy
- **Full 44-Author Pen Name Roster**
- **19 Standardized Manuscript Formats** (including updated `Comic Book` and `Trilogy` spellings)

**Status (25 November 2026):** these are **bases for later fine-tuning**, not inference targets. Fine-tuning runs on Hugging Face or a local tool such as Unsloth, and local work is not planned for now (hardware). The Writing EOS app does not call these models; its mature tier is the inference-ready catalog in `../llm-identifier-creative-writing-abliterated/`.

## Repository Structure
The files live in the sibling folder `../llm-identifier-creative-writing/`; this folder holds only this README.
- `../llm-identifier-creative-writing/data/llm_identifier_creative_writing_base_models_populated.csv` — Notion-ready CSV (204 unique models)
- `../llm-identifier-creative-writing/data/notion_database_entries.json` — Notion REST API batch payload
- `../llm-identifier-creative-writing/docs/author_personas.md` — Complete 44-author roster & model assignments
- `../llm-identifier-creative-writing/docs/genre_matrix.md` — Category A–H breakdown & counts
- `../llm-identifier-creative-writing/scripts/query_models.py` — CLI model filter (`--pen-name`, `--genre`, `--format`, `--category`, `--uncensored`)
- `../llm-identifier-creative-writing/scripts/notion_importer.py` — Automated Notion REST API importer

## Quick Usage
Run from `../llm-identifier-creative-writing/`:
```bash
python3 scripts/query_models.py --category "Category A" --format "Trilogy"
python3 scripts/query_models.py --pen-name "Naomi McNamara" --uncensored
```

## Importing to Notion
Set the `NOTION_TOKEN` and `NOTION_DATABASE_ID` environment variables, then run:
```bash
python3 scripts/notion_importer.py
```

---
name: interlinear-reader
description: Use when the user sends photos, scans or PDFs of a foreign-language text (worksheet, book page, article, reading assignment) and wants it as an HTML page with a translation over every word, a click-to-reveal vocabulary reader, an interlinear or word-by-word translation, or "die Übersetzung über jedem Wort". Also use when they want to continue, extend or fix such a reader, keep or restore their reading progress, or add another page or worksheet. Builds one self-contained HTML file where each word or phrase reveals its gloss on click, every sentence has a full translation button, revealed items stay revealed with a timestamped log, and the progress is saved in the browser and written back into the HTML file itself.
---

# Interlinear Reader

Turn a foreign-language text into a single HTML file: every word or short
phrase shows its translation above it when clicked, each sentence has a
button for a natural full translation, and progress survives reloads,
moved files and other browsers.

Default target language is German (UI strings are German). Use another
language when the user writes in it or asks for it, and override the UI
strings with `ui` (see Data format).

## Steps

1. **Transcribe exactly.** Read every image or PDF page. Copy the text
   character for character, including accents, `¿ ¡`, headings, numbering
   and comprehension questions. Rejoin words hyphenated across line breaks
   (`comuni-dad` → `comunidad`). Skip page numbers, blank answer lines and
   stray handwriting. When page order is unclear, use the page numbers or
   the logic of the text, and tell the user which order you chose.
   Done when: every sentence of the source appears once, in reading order.

2. **Write the data file** (`<name>.json`, format below). Follow the gloss
   rules, because the user reads the glosses one at a time, so each one
   must make sense by itself.
   Done when: each paragraph has one sentence translation per sentence.

3. **Build.** Run `python3 <skill-dir>/scripts/build.py <name>.json <name>.html`.
   Fix every `ERROR`. Treat every `WARN` (a gloss like `–`) as a bug: merge
   that word into a neighbouring chunk.
   Done when: the build prints `OK` and no warnings.

4. **Verify.** Show the page to the user if the host can render HTML.
   Otherwise open it in a headless browser and check that the count line
   (`0 / N Wörter · 0 / M Sätze`) appears. Spot-check five random glosses
   against the sentence translation.

5. **Deliver.** Give the file path and three sentences at most:
   - Click a word to reveal it, click `DE` for the whole sentence.
   - Progress is kept in this browser automatically.
   - "In Datei speichern" (Chrome/Edge) writes the progress into the HTML
     file itself, then keeps saving it automatically. In Safari/Firefox the
     button downloads a copy with the progress inside, which then replaces
     the old file.

## Gloss rules

- **Chunk by meaning, not by word.** One clickable unit = the smallest
  piece whose translation stands on its own:
  - article + noun: `la~comida/das_Essen`
  - preposition + article (+ noun): `de~la~pesca/vom_Fischfang`,
    `en~universidades/an_Universitäten`
  - fixed expressions: `Sin~embargo/jedoch`, `Hoy~en~día/heutzutage`,
    `a~pesar~de/trotz`, `a~lo~largo~de/entlang`
  - verb periphrases and compound tenses: `ha~tenido/hat_gehabt`,
    `sigue~siendo/ist_weiterhin`, `tienen~que/müssen`
  - `se` constructions and relative clauses: `que~se~prepara/das_zubereitet_wird`
  - noun + adjective that German writes as one word:
    `sector~turístico/Tourismusbereich`, `leche~de~coco/Kokosmilch`
- Keep chunks short (1–4 words). Do not glue whole clauses together.
- Never use `–`, empty or "untranslatable" glosses. If a word has no own
  translation, it belongs in a chunk.
- Gloss in context: correct case, number and verb form for this sentence
  (`fundaron/gründeten`, `trabajan/arbeiten_sie` when the subject is
  implied).
- Names and numbers gloss to themselves; keep a trailing comma or period
  on both sides (`Roatán,/Roatán,`).
- Sentence translations are idiomatic German, not word order copies.

## Data format

```json
{
  "title": "Ficha de trabajo 3",
  "heading": "Ficha de trabajo 3 – Los garífunas: ¿Cómo viven?",
  "storageId": "ficha3",
  "lang": "es",
  "sections": [
    { "label": "Text", "blocks": [
      { "type": "h", "text": "¿Cómo/Wie viven/leben los~garífunas?/die_Garífuna?" },
      { "type": "p",
        "text": "La~comida/Das_Essen es/ist una~parte/ein_Teil importante/wichtiger de~su~cultura./ihrer_Kultur.",
        "sentences": ["Das Essen ist ein wichtiger Teil ihrer Kultur."] }
    ]}
  ]
}
```

- Token = `source/gloss`, separated by spaces. `~` is a space inside the
  source chunk, `_` a space inside the gloss.
- A sentence ends at a source chunk ending in `.`, `?` or `!` (not at list
  numbers like `1.`). `sentences` needs exactly one entry per sentence end;
  the build checks this. Headings (`h`) get no sentence translations.
- `storageId` must be unique per reader and must never change, since it keys the
  saved progress.
- Optional: `ui` (object overriding UI strings, see `L` in the template),
  `sentenceButton` (default `DE`), `locale` (default `de-DE`).
- A full example is in `examples/ficha3.json`.

## Updating an existing reader

Edit the JSON and rebuild to the **same** output path. The build keeps the
progress stored in the existing HTML. Progress is keyed by text (chunk +
gloss + occurrence), so unchanged chunks stay revealed. Only chunks you
rewrite lose their reveal. Tell the user when a re-chunk resets words they
had revealed.

To import a progress list the user pasted (e.g. "Agradecemos → Wir danken
13.11., 09:17"), match each line to its chunk in reading order and add it to
`legacy.seed` as `[wordIndex, epochMillis]`. The index counts glossed tokens
from 0. Then rebuild. `legacy.wordsKey` / `legacy.sentsKey` migrate an old
position-based localStorage save of the same text once.

## Do not

- Do not split the output into several files or load anything from a CDN;
  the reader must work offline from a single file.
- Do not put answers to comprehension questions in the page unless asked.
- Do not change `storageId` of an existing reader.

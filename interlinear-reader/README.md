# interlinear-reader

Turns photos, scans or PDFs of a foreign-language text into one offline HTML file. Clicking a word or short phrase reveals its translation above it, and a button per sentence shows a natural full translation. Revealed items stay revealed and appear in a timestamped log. Progress is saved in the browser and can be written back into the HTML file itself, so it survives moving the file or opening it in another browser.

Triggers when you send a text and ask for a translation over every word, a click-to-reveal vocabulary reader, or an interlinear translation. It also triggers when you want to extend such a reader or restore its progress.

Install:

```sh
npx skills add github.com/luisKisters/skills --skill interlinear-reader
```

Build a reader from a data file:

```sh
python3 scripts/build.py examples/ficha3.json ficha3.html
```

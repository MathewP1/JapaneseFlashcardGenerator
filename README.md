## Japanese flashcard generator

This is my attempt to make process of generating flashcards for vocabulary easier.

### How to use
Create .csv file with 2 columns: `Vocab` - this is for vocabulary written with Kanji/kana and `Vocab-English` - for translation to english.

Based on this, the script will generate new csv file with additional columns:
- `Vocab-Furigana` - with furigana in this format `漢字[ふりがな]`
- `Vocab-Kana` - with kana only - **doesn't work now**
- `Vocab-Type` - fetches the part of speech (e.g. `godan verb with ru ending`) from Jisho website
- `Kanji-Meaning` - fetches the meaning of kanjis from Jisho website


The resulting csv file can be imported to Anki.

### Future plans
- Use pykakasi to perform conversions to furigana and kana


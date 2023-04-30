import furigana
import argparse as ap
import sys
import csv
import requests
from bs4 import BeautifulSoup

KANJI_COLUMN = "Vocab"
FURIGANA_COLUMN = "Vocab-Furigana"
KANA_COLUMN = "Vocab-Kana"
KANJI_MEANING_COLUMN = "Kanji-Meanings"
VOCAB_TYPE_COLUMN = "Vocab-Type"
COLUMN_ORDER = [KANJI_COLUMN, FURIGANA_COLUMN, KANA_COLUMN, "Vocab-English", VOCAB_TYPE_COLUMN, KANJI_MEANING_COLUMN]


# get first word from string of words, separated by commas, can have leading spaces
def get_first_word(text):
    return text.split(",")[0].strip()


# From japanese text, return list of kanji
def get_kanji(text):
    kanji = []
    for c in text:
        if 0x4e00 <= ord(c) <= 0x9faf:
            kanji.append(c)
    return kanji


# Get part of speach from Jisho website
def get_part_of_speech(word):
    url = "https://jisho.org/word/" + word
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        part_of_speech = soup.find("div", {"class": "concept_light clearfix"}) \
            .find("div", {"class": "concept_light-meanings"}) \
            .find("div", {"class": "meanings-wrapper"}) \
            .find("div", {"class": "meaning-tags"})
        # Get first word from meaning string
        part_of_speech = get_first_word(part_of_speech.text)
    except AttributeError:
        part_of_speech = ""
    print("Part of speech of " + word + ": " + part_of_speech)
    return part_of_speech


# Get kanji meaning from Jisho website
def get_kanji_meaning(kanji):
    url = "https://jisho.org/search/" + kanji + "%20%23kanji"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    meaning = soup.find("div", {"class": "kanji-details__main-meanings"}).text
    # Get first word from meaning string
    meaning = get_first_word(meaning)
    print("Meaning of " + kanji + ": " + meaning)
    return meaning


def process_csv(file):
    file_contents = {}
    with open(file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for h in header:
            file_contents[h] = []

        for row in reader:
            for i, h in enumerate(header):
                file_contents[h].append(row[i])

    file_contents[FURIGANA_COLUMN] = []
    file_contents[KANA_COLUMN] = []
    file_contents[KANJI_MEANING_COLUMN] = []
    file_contents[VOCAB_TYPE_COLUMN] = []
    for val in file_contents[KANJI_COLUMN]:
        file_contents[FURIGANA_COLUMN].append(furigana.add_furigana(val))
        file_contents[KANA_COLUMN].append(furigana.to_hiragana(val))
        file_contents[VOCAB_TYPE_COLUMN].append(get_part_of_speech(val))
        kanjis = get_kanji(val)
        if len(kanjis) > 0:
            kanji_meanings = []
            for kanji in kanjis:
                kanji_meanings.append(get_kanji_meaning(kanji))
            file_contents[KANJI_MEANING_COLUMN].append("; ".join(kanji_meanings))
        else:
            file_contents[KANJI_MEANING_COLUMN].append("")

    output_file = file.replace(".csv", "-output.csv")
    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        # writer.writerow(COLUMN_ORDER)
        for i in range(len(file_contents[KANJI_COLUMN])):
            writer.writerow([file_contents[c][i] for c in COLUMN_ORDER])


def main():
    parser = ap.ArgumentParser(description="CSV file converter")
    parser.add_argument("file", metavar="file", type=str, help="CSV file to process")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if process_csv(args.file) is False:
        print("Error processing CSV file.")


if __name__ == '__main__':
    main()

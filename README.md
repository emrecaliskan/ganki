# Ganki

Ganki is a Python library for creating [Anki](https://apps.ankiweb.net/) decks from websites or local files using ChatGPT.

## Installation

Use your favorite package manager to install

```bash
#pip
pip install git+https://github.com/emrecaliskan/ganki

#poetry
poetry add git+https://github.com/emrecaliskan/ganki

```

## Usage

1. Create a deck using the `create-deck` command. 

    By default, this will create a deck called `ganki-deck.apkg` (you can specify output path with `--output` option)

    ```bash
    ganki create-deck https://nakamotoinstitute.org/bitcoin/
    ```

2. Import the `.apkg` file into Anki (File->Import).


## License
[MIT](https://choosealicense.com/licenses/mit/)

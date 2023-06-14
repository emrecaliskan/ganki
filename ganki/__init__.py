import logging

import genanki
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PlaywrightURLLoader, TextLoader
from rich.console import Console
from rich.logging import RichHandler
from rich.text import Text

from ganki.qachain import QAGenerationChainMod

logger = logging.getLogger("rich")

## not sure why this has to be hardcoded, but docs says it does
DECK_ID = 2059400110
MODEL_ID = 1607392319


class Ganki:
    DEFAULT_GENANKI_MODEL = genanki.Model(
        MODEL_ID,
        "Simple Model",
        fields=[
            {"name": "Question"},
            {"name": "Answer"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Question}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ],
    )

    def __init__(self, model_name="gpt-3.5", temperature=0):
        self.model = ChatOpenAI(temperature=temperature, model_name=model_name)

    def _create_deck_from_doc(self, doc, deck_name) -> genanki.Deck:
        deck = genanki.Deck(DECK_ID, deck_name)
        chain = QAGenerationChainMod.from_llm(self.model)
        logger.info(f"Generating questions ...", extra={"markup": True})
        question_and_answers = chain.run(doc.page_content)
        for qa in question_and_answers:
            note = genanki.Note(
                model=self.DEFAULT_GENANKI_MODEL, fields=[qa["question"], qa["answer"]]
            )
            deck.add_note(note)
        return deck

    def create_deck_from_url(self, url, deck_name: str) -> genanki.Deck:
        logger.info(f"Loading page from  [blue]{url}[/blue]", extra={"markup": True})
        loader = PlaywrightURLLoader(urls=[url], remove_selectors=["header", "footer"])
        doc = loader.load()[0]
        return self._create_deck_from_doc(doc, deck_name)

    def create_deck_from_file(self, file, deck_name: str) -> genanki.Deck:
        loader = TextLoader(file)
        doc = loader.load()[0]
        return self._create_deck_from_doc(doc, deck_name)

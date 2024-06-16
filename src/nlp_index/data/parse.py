import json
from pathlib import Path
from typing import Annotated
import typer
import pandas as pd
from nlp_index.config import logger


app = typer.Typer()


def filter_relevant_keys(documents: dict):
    relevant_keys = ["id", "date", "from", "from_id", "text"]
    return [
        {key: message[key] for key in relevant_keys}
        for message in documents["messages"]
        if message["type"] == "message"
    ]


def preprocess_text_field(messages: list[dict]) -> list[str]:
    """
    Remove the nested structure of the text field (showing formatting) in the messages and return a list of strings.
    e.g 'text': [
        'Для интересующихся:  ...',
        {'type': 'link', 'text': 'https://gist.github.com/dveselov/af9bc55b4be16fe1fe92d4b5347f1027'},
        ''
    ] → "Для интересующихся:  ... https://gist.github.com/dveselov/af9bc55b4be16fe1fe92d4b5347f1027"
    """
    texts = []

    for message in messages:
        message_text = ""

        for part in message["text"]:
            if isinstance(part, dict):
                message_text += part["text"]
            else:
                message_text += part

        texts.append(message_text)

    return texts


def parse_documents(raw_documents: dict):
    messages = filter_relevant_keys(raw_documents)

    df = pd.DataFrame(messages)
    df["text"] = preprocess_text_field(messages)

    logger.info(f"Parsed {len(df)} messages")
    logger.info("Documents structure: ")
    logger.info(df.sample(5))

    return df


@app.command(
    help="Parse the input JSON file of the telegram chat export and save the prepared csv with only relevant information."
)
def main(
    raw_documents_path: Annotated[Path, typer.Option(help="Path to the raw documents")] = Path(
        "data/raw/chat_export.json"
    ),
    prepared_documents_path: Annotated[Path, typer.Option(help="Path to which to save the prepared documents")] = Path(
        "data/prepared/messages.csv"
    ),
):
    raw_documents = json.loads(raw_documents_path.read_text())
    prepared_documents = parse_documents(raw_documents)
    prepared_documents.to_csv(prepared_documents_path, index=False)


if __name__ == "__main__":
    app()

import json
from pathlib import Path

from bs4 import BeautifulSoup
from rich.progress import Progress

from nlp_index.config import log


def parse_one_file(data: str) -> list[dict[str, str]]:
    bs = BeautifulSoup(data, "lxml")
    all_messages = bs.find_all(class_="text")

    message_store = []
    good_count = 0
    bad_count = 0

    for message in all_messages:
        try:
            message_dict = {
                "text": message.text.strip(),
                "time": message.parent.find(class_="date")["title"].strip(),
                "author": message.parent.find(class_="from_name").text.strip(),
            }
            good_count += 1
            message_store.append(message_dict)
        except (TypeError, KeyError, AttributeError):
            bad_count += 1

    log(f"Correctly parsed {good_count} messages. Dropped {bad_count} messages.")

    return message_store


all_messages = []
data_dir = Path(__file__).parent.parent / "data" / "raw" / "chat_export"
files = sorted(list(data_dir.iterdir()))


with Progress() as progress:
    task = progress.add_task("Parsing files", total=len(files))
    log = progress.console.log

    for path in files:
        input_data = path.read_text()
        new_messages = parse_one_file(input_data)
        all_messages.extend(new_messages)
        progress.advance(task)


log(f"Done with {len(all_messages)} messages")


message_dump = json.dumps(all_messages, ensure_ascii=False, indent=2)
Path("./data/prepared/messages.json").write_text(message_dump)

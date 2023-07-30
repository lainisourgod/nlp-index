import json
from pathlib import Path

from llama_index import Document, VectorStoreIndex
from llama_index.node_parser import SimpleNodeParser

messages = json.loads(
    (Path(__file__).parent.parent / "data" / "prepared" / "messages.json").read_text()
)

# XXX: for first investigation to not burn all money on shitty experiments
messages = messages[:100]

documents = [
    Document(
        text=message["text"],
        extra_info=dict(time=message["time"], author=message["author"]),
    )
    for message in messages
]


parser = SimpleNodeParser()
nodes = parser.get_nodes_from_documents(documents, show_progress=True)


index = VectorStoreIndex(nodes, show_progress=True)
index_dir = Path(__file__).parent.parent / "data" / "prepared" / "index"
index.storage_context.persist(persist_dir=index_dir)

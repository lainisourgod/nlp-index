from pathlib import Path

from llama_index import StorageContext, load_index_from_storage

# rebuild storage context
index_dir = Path(__file__).parent.parent / "data" / "prepared" / "index"
storage_context = StorageContext.from_defaults(persist_dir=index_dir)

# load index
index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()
response = query_engine.query("кто хотел сделать русскую модель для Spacy?")
print(response)

from llama_index.core import SimpleDirectoryReader
docs = SimpleDirectoryReader(input_dir="./data", recursive=True).load_data()
print(docs)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
embed_model = HuggingFaceEmbedding()
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
db = chromadb.PersistentClient(path="./beau_chromadb")
chroma_collection = db.get_or_create_collection("beau_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(docs,storage_context=storage_context, embed_model=embed_model)
# Load embeddings from disk
db2 = chromadb.PersistentClient(path="./beau_chromadb")
chroma_collection = db2.get_or_create_collection("beau_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)
# Init Ollama
from llama_index.llms.ollama import Ollama
llm = Ollama(model="llama3", request_timeout=45.0)
# Query Data
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("Who is the author and where is he from?")
print(response)
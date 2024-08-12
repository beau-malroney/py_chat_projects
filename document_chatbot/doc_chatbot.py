import streamlit as st
import chromadb
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

data_dir = "./data"
chromadb_path = "./beau_chromadb"
chromadb_collection_name = "beau_collection"

st.set_page_config(page_title="Chat with the docs, powered by LlamaIndex", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Chat with docs, powered by LlamaIndex 💬🦙")
st.info("Check out the full tutorial to build this app in our [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)", icon="📃")

####UPLOAD DOCUMENTS################################################################################
uploaded_files = st.file_uploader(
    "Choose a CSV file", accept_multiple_files=True
)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)
####################################################################################################

if "messages" not in st.session_state:  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about Streamlit's open-source Python library!",
        }
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    Settings.llm = Ollama(
        model="llama3",
        temperature=0.2,
        embed_model="local",
        system_prompt="""You are an expert on 
        Python and your 
        job is to answer technical questions. 
        Assume that all questions are related 
        to the Python. Keep 
        your answers technical and based on 
        facts – do not hallucinate features.""",
    )    
    docs = SimpleDirectoryReader(input_dir=data_dir, recursive=True).load_data()
    print(docs)
    embed_model = HuggingFaceEmbedding()    
    # Create chromadb
    db = chromadb.PersistentClient(path=chromadb_path)
    # Create chromadb collection
    chroma_collection = db.get_or_create_collection(chromadb_collection_name)
    # Write embeddings from docs to chromadb
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(docs,storage_context=storage_context, embed_model=embed_model)
    # Load embeddings from disk
    db2 = chromadb.PersistentClient(path=chromadb_path)
    chroma_collection = db2.get_or_create_collection(chromadb_collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)
    return index

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = load_data().as_chat_engine(
        chat_mode="condense_question", verbose=True, streaming=True
    )

if prompt := st.chat_input(
    "Ask a question"
):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Write message history to UI
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response_stream = st.session_state.chat_engine.stream_chat(prompt)
        st.write_stream(response_stream.response_gen)
        message = {"role": "assistant", "content": response_stream.response}
        # Add response to message history
        st.session_state.messages.append(message)
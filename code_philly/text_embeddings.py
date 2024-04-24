import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding

def text_embeddings(text,embed_model,collection_name):
    doc = Document(text=text)

    # vector_index = VectorStoreIndex.from_documents(documents=[doc])
    if embed_model!='openAI':
        embed_model = HuggingFaceEmbedding(model_name=embed_model)
    elif embed_model=='text-embedding-ada-002-v2':
        embed_model = OpenAIEmbedding(model="text-embedding-ada-002-v2")
    elif embed_model=='text-embedding-3-small':
        embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    elif embed_model=='text-embedding-3-large':
        embed_model = OpenAIEmbedding(model="text-embedding-3-large")
    doc = Document(text=text)
    db = chromadb.PersistentClient(path="./vector_db")
    chroma_collection = db.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents=[doc], storage_context=storage_context, embed_model=embed_model
    )

    return embed_model
from llama_index.core import (VectorStoreIndex,SimpleDirectoryReader,StorageContext,ServiceContext,load_index_from_storage)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.groq import Groq
import warnings

warnings.filterwarnings('ignore')


model_name = "sentence-transformers/all-MiniLM-L6-v2"
groq_model = "llama3-70b-8192"
groq_api_key = "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"
persist_dir="./storage_mini"





def process_data(file_path):
    reader = SimpleDirectoryReader(input_files=[file_path])
    documents = reader.load_data()
    text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
    nodes = text_splitter.get_nodes_from_documents(documents, show_progress=True)
    embed_model = HuggingFaceEmbedding(model_name=model_name)
    llm = Groq(model=groq_model, api_key=groq_api_key)
    service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)
    vector_index = VectorStoreIndex.from_documents(documents, show_progress=True, service_context=service_context, node_parser=nodes)
    vector_index.storage_context.persist(persist_dir=persist_dir)
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    index = load_index_from_storage(storage_context, service_context=service_context)
    
    query_engine = index.as_query_engine(service_context=service_context, similarity_top_k=5)
    return query_engine



# def querys(query_engine, query):
#     resp = query_engine.query(query)
#     return resp.response



# file_path = "/home/abhijitingole/Projects/POC_CustomChat_Bot/Frequently Asked Questions 1.pdf"
# query_engine = process_data(file_path)
# while True:
#     query = "how many labels in dasboard"
#     response = querys(query_engine, query)

#     print(response)
##################################


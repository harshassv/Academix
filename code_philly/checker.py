from Youtube_Transcript import y_transcript
from llama_index.core import Document
from llama_index.core.node_parser import CodeSplitter
from llama_index.core import SimpleDirectoryReader
import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
from git import Repo
from langchain_community.document_loaders import UnstructuredURLLoader
from llama_index.core.node_parser import SentenceSplitter
from RAG import RAG,RAG_query
from vector_storing import vector_storing
from vector_load import vector_load
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex,SummaryIndex,StorageContext,SimpleKeywordTableIndex
from llama_index.embeddings.openai import OpenAIEmbedding


def checker(data):

    # code_query = ''

    response_ext = data
    # response_ext = {'url':'https://github.com/stanford-futuredata/FrugalGPT','repo_name':'FrugalGPT'}
    # response_ext = {'url':'https://docs.sweep.dev/blogs/chunking-2m-files'}
    h_file = open('history.txt','r')
    history = h_file.read()
    print('in checker')
    h_file.close()
    # print(response_ext['url'])
    # print(history)

    if response_ext['url'] not in history:

        if 'youtube' in response_ext['url'].lower():
            print('youtube')
            transcript_text = y_transcript(response_ext['url'].split('=')[-1])
            if 'video_title' in response_ext:
                document = Document(text=transcript_text,
                                        metadata = {"video_title": response_ext['video_title'], "video_url": response_ext['url']})
            else:
                document = Document(text=transcript_text,
                                        metadata = {"video_url": response_ext['url']})
            documents = [document]
            parser = SentenceSplitter(chunk_size=1024)
            nodes = parser.get_nodes_from_documents(documents)
            RAG(nodes)
            print('done')
            # print(documents)

            h_file=open('history.txt','w')
            h_file.write(data['url'])
            h_file.close()

        elif 'github' in response_ext['url'].lower():
            print(' in github')
            print(response_ext)
            repo_name = response_ext['repo_name']
            try:
                repo_path = ".\\{}\\".format(repo_name)
                repo = Repo.clone_from(response_ext['url'], to_path=repo_path)
                splitter = CodeSplitter('python')
                documents = SimpleDirectoryReader("./{}".format(repo_name),recursive=True,required_exts=[".py", ".ipynb"]).load_data()
                for i in documents:
                    i.metadata['repo_name']=repo_name
                    i.metadata['repo_link']=response_ext['url']+'/blob/master/'+i.metadata['file_path'][i.metadata['file_path'].find(repo_name)+len(repo_name):]
                nodes = splitter.get_nodes_from_documents(documents)
                # print(nodes[1].metadata)
                code_index = vector_storing("./new_embeddings/code","text-embedding-3-small","vector_store",nodes,"VectorStoreIndex")
                code_query = code_index.as_query_engine()
                response = code_query.query(response_ext['query'])
                print(str(response))

                
            except:
                code_index = vector_load("./new_embeddings/code","text-embedding-3-small","vector_store","VectorStoreIndex")
                code_query = code_index.as_query_engine()
                response = code_query.query(response_ext['query'])
                print(str(response))
            

        else:
            print('in others link')
            loader = UnstructuredURLLoader(urls=[response_ext['url']],  show_progress_bar=True)
            loader = UnstructuredURLLoader(urls=[response_ext['url']],  show_progress_bar=True)
            documents = loader.load()
            document = Document(text=documents[0].page_content)
            parser = SentenceSplitter(chunk_size=1024)
            nodes = parser.get_nodes_from_documents([document])
            index = vector_storing("./others_embeddings/top_k","text-embedding-3-small","vector_store",nodes,"VectorStoreIndex")
            others_engine = index.as_query_engine()
            response = others_engine.query(response_ext['query'])
            print(str(response))

            # print(data)
            # print(document)




        
        # print(nodes)



        

    # do webpage text stuff
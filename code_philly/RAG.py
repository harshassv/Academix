# from parser import parser
from llama_index.core import Document,Settings
import nest_asyncio
from vector_storing import vector_storing
from vector_load import vector_load
from llama_index.llms.together import TogetherLLM
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine import RouterQueryEngine
from sentence_transformers import CrossEncoder
from llama_index.core.selectors import (
    PydanticMultiSelector,
    PydanticSingleSelector,
    LLMSingleSelector, 
    LLMMultiSelector
)
from llama_index.core.node_parser import CodeSplitter
from llama_index.core import SimpleDirectoryReader
from llama_index.core.tools import QueryEngineTool


nest_asyncio.apply()
Settings.chunk_size = 1024

def RAG(nodes):
    
     # Storing nodes in Chroma DB

    vector_storing("./embeddings/top_k","text-embedding-3-small","vector_store",nodes,"VectorStoreIndex")

    vector_storing("./embeddings/summaries","text-embedding-3-small","summary",nodes,"SummaryIndex")

    vector_storing("./embeddings/key_words","text-embedding-3-small","key_words_store",nodes,"SimpleKeywordTableIndex")
    

def RAG_query(query,llm_id=None):
    
    if llm_id:
        model = TogetherLLM(model=llm_id, api_key="")
    else:
        model=OpenAI()
    print("ModelName = ",model)

    try:

        vector_index = vector_load("./embeddings/top_k","text-embedding-3-small","vector_store","VectorStoreIndex")

        print(vector_index.index_struct)

        vector_query_engine = vector_index.as_query_engine(similarity_top_k=15,llm=model)
        
        vector_tool = QueryEngineTool.from_defaults(
            query_engine=vector_query_engine,
            description=(
                "Useful for retrieving specific context and if you don't know to use any other tool then you can use this tool as defualt, incase of any confusions."
            ),
        )
    
    except:
        pass

    summary_index = vector_load("./embeddings/summaries","text-embedding-3-small","summary","SummaryIndex")

    # Query Data from the persisted index
    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize", use_async=True,llm=model
    )

    summary_tool = QueryEngineTool.from_defaults(
        query_engine=summary_query_engine,
        description=(
            "Useful for summarization. Use this tool only in the case of summarization"
        ),
    )

    key_words_index = vector_load("./embeddings/key_words","text-embedding-3-small","key_words_store","SimpleKeywordTableIndex")

    key_words_query_engine = key_words_index.as_query_engine(similarity_top_k=15,llm=model)

    key_words_tool = QueryEngineTool.from_defaults(
        query_engine=key_words_query_engine,
        description=(
            "Useful for searching based on specific key words"
        ),
    )

    # code_index = vector_load("./new_embeddings/code","text-embedding-3-small","vector_store","VectorStoreIndex")
    # print(code_index.index_struct)

    # code_engine = code_index.as_query_engine(similarity_top_k=10,llm=model)

    # code_tool = QueryEngineTool.from_defaults(
    #     query_engine=code_engine,
    #     description=(
    #         "Useful for code or programming realted queries."
    #     ),
    # )


    query_fusion_retriever = QueryFusionRetriever(
        [vector_index.as_retriever()],
        similarity_top_k=5,
        num_queries=3,  # set this to 1 to disable query generation
        mode="reciprocal_rerank",
        use_async=True,
        verbose=True,
        llm=model
        # query_gen_prompt="...",  # we could override the query generation prompt here
    )

    # nodes_with_scores = query_fusion_retriever.retrieve("what is frugal GPT and it's score on different datasets compared to ChatGPT 3 and 4")


    query_fusion_query_engine = RetrieverQueryEngine.from_args(query_fusion_retriever,llm=model)


    query_fusion_tool = QueryEngineTool.from_defaults(
        query_engine=query_fusion_query_engine,
        description=(
            "Split complex queries into sub queries"
        ),
    )


    query_engine = RouterQueryEngine(
        selector=PydanticMultiSelector.from_defaults(),
        query_engine_tools=[
            vector_tool,
            summary_tool,
            key_words_tool,
            # code_tool,
            query_fusion_tool
        ],llm=model
    )
    response = query_engine.query(query)
    response_str = str(response)
    text = ''
    for i in range(len(response.source_nodes)):
        text+=response.source_nodes[i].text
    model = CrossEncoder('vectara/hallucination_evaluation_model')
    scores = model.predict([
    [response_str, text]
    ])

    # print(str(response), query)
    print(scores[0])
    if scores[0] > 0.5:
        return response_str 
    else:
        return response_str
    # return response_str + str(' Hallucinaion score is :'+ str(scores[0]))
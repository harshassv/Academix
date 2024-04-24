from langchain_community.tools import DuckDuckGoSearchRun

def duck_duck_go_search(search_query):
    search = DuckDuckGoSearchRun()
    return search.run(search_query)
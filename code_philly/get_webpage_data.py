from langchain_community.document_loaders import UnstructuredURLLoader

def get_webpage_data(urls):
    loader = UnstructuredURLLoader(urls=urls,  show_progress_bar=True)
    data = loader.load()
    return data

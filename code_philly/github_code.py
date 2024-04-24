import os
from git import Repo
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language

os.environ["GIT_PYTHON_REFRESH"] = "quiet"
def github_code(url):
    repo_path = ".\\github_code\\"
    repo = Repo.clone_from(url, to_path=repo_path)


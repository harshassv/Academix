# if file location is passed then do parsing

# from pdf_parser import parser
from llama_index.core import Document,Settings
import nest_asyncio
from markdown_parser import markdown_parser
from RAG import RAG,RAG_query

def pdf_RAG():
    nest_asyncio.apply()

    Settings.chunk_size = 1024

    # parser('./paper.pdf')

    current_pfile = 'parsed_pdf.md'

    with open(current_pfile, 'r', encoding="UTF-8") as f:
        parsed_text = f.read()

    title = parsed_text[parsed_text.find(' '):parsed_text.find('\n')]

    title = title.strip()


    documents = []
    for para in parsed_text.split('##'):
            section = para[:para.find('\n')].strip()
            if section.lower() != 'references':
                # print(section , para)
                doc = Document(text=para, metadata={"file_name": title, "paper_name": title, "section": section})
                documents.append(doc)


    base_nodes, objects = markdown_parser(documents)

    nodes = base_nodes + objects

    print('bulding nodes')

    RAG(nodes)

    # response = RAG_query('can you summarise the entire Frugal GPT paper')

    # print(response)

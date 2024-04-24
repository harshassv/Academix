import nest_asyncio
from llama_parse import LlamaParse
from pdf_RAG import pdf_RAG


def pdf_parser(file_location):
    nest_asyncio.apply()
    parser = LlamaParse(
        api_key="llx-GjG5HhPfs23JS7ffTRbsqHwPOS1nR3yzL5Tft8XVrojruUCG",  # can also be set in your env as LLAMA_CLOUD_API_KEY
        result_type="markdown"  # "markdown" and "text" are available
    )

    # sync
    documents = parser.load_data(file_location)

    # Dumping parsed document in markdown file
    current_pfile = './parsed_pdf.md'

    with open(current_pfile, 'w', encoding="UTF-8") as f:
        f.write(documents[0].text)

    pdf_RAG()
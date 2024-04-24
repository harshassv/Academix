from youtube_transcript_api import YouTubeTranscriptApi
from llama_index.core import Document
from llama_index.core import VectorStoreIndex

text = YouTubeTranscriptApi.get_transcript('vV_WdTBbww4')

transcript_text = ''

for transcript in text:
    if transcript['text'] != '[Music]':
        transcript_text+=transcript['text']

# print(transcript_text)

doc = Document(text=transcript_text)

vector_index = VectorStoreIndex.from_documents(documents=[doc])
# vector_index.as_query_engine()

query_engine = vector_index.as_query_engine()
response = query_engine.query(
    "what is xz vulnerability ? summarise me "
)
print(response)





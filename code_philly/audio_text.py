from openai import OpenAI
from RAG import RAG


client = OpenAI()

def audio_text(file_location):
    audio_file= open(file_location)
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    RAG(transcription.text)
    return transcription.text
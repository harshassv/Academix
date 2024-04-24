from youtube_transcript_api import YouTubeTranscriptApi

def y_transcript(video_id):
    text = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = ''
    for transcript in text:
        if transcript['text'] != '[Music]':
            transcript_text+=transcript['text']
    return transcript_text
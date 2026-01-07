from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_text(url):
    video_id = re.search(r"v=([^&]+)", url).group(1)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([t["text"] for t in transcript])

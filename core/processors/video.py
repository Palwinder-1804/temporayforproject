import re
from youtube_transcript_api import YouTubeTranscriptApi


def _extract_youtube_id(url: str) -> str:
    """
    Extract YouTube video ID from various URL formats.
    """
    match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    if match:
        return match.group(1)
    return ""


def process_video(url: str) -> str:
    """
    Extract transcript text from a YouTube video URL.

    Responsibilities:
    - Extract video ID
    - Fetch captions if available
    - Fallback gracefully if captions are disabled
    """

    if not url:
        return ""

    try:
        video_id = _extract_youtube_id(url)
        if not video_id:
            return ""

        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join(segment.get("text", "") for segment in transcript)

        return " ".join(text.split())

    except Exception as e:
        print(f"Video transcript unavailable: {e}")
        return ""

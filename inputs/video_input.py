import whisper
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("medium", device=device)

def video_to_text(path: str) -> str:
    result = model.transcribe(path)
    return result["text"]

import whisper
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("medium", device=device)

def video_to_text(video_path):
    result = model.transcribe(video_path)
    return result["text"]

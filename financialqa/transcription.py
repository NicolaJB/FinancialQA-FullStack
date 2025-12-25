import whisper

class WhisperTranscriber:
    def __init__(self, model_name: str = "base"):
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading Whisper model: {model_name} on {device}...")
        self.model = whisper.load_model(model_name, device=device)

    def transcribe_audio(self, audio_path: str) -> str:
        result = self.model.transcribe(audio_path)
        return result["text"]

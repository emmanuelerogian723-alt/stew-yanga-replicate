"""Stew Yanga - Nigerian multilingual ASR (Igbo, Yoruba, Hausa)."""
from cog import BasePredictor, Input, Path
import torch, soundfile as sf
from transformers import WhisperProcessor, WhisperForConditionalGeneration

MODELS = {
    "igbo": "Erog0291/stew-audio-0.1-asr-ig",
    "yoruba": "Erog0291/stew-audio-0.1-asr-yo",
    "hausa": "Erog0291/stew-audio-0.1-asr-ha",
}

class Predictor(BasePredictor):
    def setup(self):
        self.models = {}
        for lang, rid in MODELS.items():
            proc = WhisperProcessor.from_pretrained(rid)
            model = WhisperForConditionalGeneration.from_pretrained(rid)
            model.generation_config.forced_decoder_ids = None
            model.config.forced_decoder_ids = None
            self.models[lang] = (proc, model.eval())

    def predict(self, audio: Path = Input(description="Audio file (wav/mp3/flac)"),
                language: str = Input(choices=["igbo", "yoruba", "hausa"],
                                      default="igbo",
                                      description="Nigerian language of the speech")) -> str:
        wav, sr = sf.read(str(audio), dtype="float32")
        if wav.ndim > 1:
            wav = wav.mean(1)
        proc, model = self.models[language]
        feats = proc.feature_extractor(wav, sampling_rate=sr,
                                       return_tensors="pt").input_features
        with torch.no_grad():
            ids = model.generate(feats, max_new_tokens=440, num_beams=5)
        return proc.tokenizer.decode(ids[0], skip_special_tokens=True).strip()

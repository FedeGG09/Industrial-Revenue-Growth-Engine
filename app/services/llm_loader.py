from dataclasses import dataclass
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from app.core.config import settings


@dataclass
class LLMResponse:
    text: str


class TransformersLocalLLM:
    def __init__(self, model_id: str, use_4bit: bool = True, use_8bit: bool = False):
        self.model_id = model_id
        quant_config = None
        if use_4bit or use_8bit:
            quant_config = BitsAndBytesConfig(
                load_in_4bit=use_4bit,
                load_in_8bit=use_8bit,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            token=settings.hf_token,
            use_fast=True,
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            token=settings.hf_token,
            device_map="auto",
            quantization_config=quant_config,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def generate(self, prompt: str, max_new_tokens: int = 512) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.2,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)


class OllamaLikeLLM:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str, max_new_tokens: int = 512) -> str:
        import httpx

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": max_new_tokens},
        }
        r = httpx.post(f"{self.base_url}/api/generate", json=payload, timeout=120)
        r.raise_for_status()
        return r.json().get("response", "")


def build_llm():
    if settings.llm_backend.lower() == "ollama":
        return OllamaLikeLLM(base_url="http://localhost:11434", model=settings.hf_model_id)
    return TransformersLocalLLM(
        model_id=settings.hf_model_id,
        use_4bit=settings.use_4bit,
        use_8bit=settings.use_8bit,
    )

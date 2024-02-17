from typing import List

import torch
from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

from clients.translate_client_base import TranslateClientBase
from models.subtitle import Subtitle


class LocalLlmClient(TranslateClientBase):
    def __init__(self, model_name: str, use_gpu: bool = False):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoGPTQForCausalLM.from_quantized(
            model_name,
            model_basename='model',
            use_safetensors=True,
            device="cuda:0" if use_gpu else None
        )

    def translate(self, subtitles: List[Subtitle]) -> List[Subtitle]:
        return [
            Subtitle(
                index=str(idx),
                time_frame=subtitle.time_frame,
                text=self.__get_translation(subtitle.text)
            ) for idx, subtitle in enumerate(subtitles)
        ]

    def __get_translation(self, text: str) -> str:
        prompt = f'Translate this from Japanese to English:\nJapanese: {text}\nEnglish:'

        input_ids = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            max_length=96,
            truncation=True
        ).input_ids.cuda()

        with torch.no_grad():
            generated_ids = self.model.generate(
                input_ids=input_ids,
                num_beams=5,
                max_new_tokens=96,
                do_sample=True,
                temperature=0.6,
                top_p=0.9
            )

        outputs = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

        if len(outputs) != 1:
            print(f'Could not translate "{text}"')
            return text

        raw_output: str = outputs[0]
        processed_output = raw_output.replace(prompt, '')

        print(processed_output)

        return processed_output

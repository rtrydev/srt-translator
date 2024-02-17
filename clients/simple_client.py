from typing import List

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

from clients.translate_client_base import TranslateClientBase
from models.subtitle import Subtitle


class SimpleClient(TranslateClientBase):
    def __init__(self, model_name: str, src_lang: str = 'jpn_Jpan', tgt_lang: str = 'eng_Latn', use_gpu: bool = False):
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.translator = pipeline(
            'translation',
            model=model,
            tokenizer=tokenizer,
            src_lang=src_lang,
            tgt_lang=tgt_lang,
            device=0 if use_gpu else -1
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
        output = self.translator(text, max_length=512)
        translation_text = output[0]['translation_text']

        print(translation_text)

        return translation_text

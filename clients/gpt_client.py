from typing import List

from clients.translate_client_base import TranslateClientBase
from models.sequential_data import SequentialData
from models.subtitle import Subtitle

import requests

SYSTEM_PROMPT = '''
Function as a direct Japanese-English translation tool.
If you are supplied with text marked as 'Previous', use it for context.
Do not translate the context.
The translation should consist of a single line of text without any additions.
'''

USER_PROMPT_TEMPLATE = '''
Previous: "[PREV]"

[TL_LN]
'''


class GptClient(TranslateClientBase):
    def __init__(self, api_token: str, gpt_model: str = 'gpt-4'):
        self.api_token = api_token
        self.system_prompt = SYSTEM_PROMPT
        self.user_prompt_template = USER_PROMPT_TEMPLATE
        self.gpt_model = gpt_model

    def translate(self, subtitles: List[Subtitle]) -> List[Subtitle]:
        result: List[Subtitle] = []
        sequential_data = self.__prepare_sequential_data(subtitles)

        for idx, data in enumerate(sequential_data):
            prompt = self.__prepare_prompt(data)
            result.append(
                Subtitle(
                    index=str(idx),
                    time_frame=subtitles[idx].time_frame,
                    text=self.__get_result_from_api(prompt)
                )
            )

        return result

    def __prepare_sequential_data(self, subtitles: List[Subtitle]) -> List[SequentialData]:
        texts = [
            subtitle.text
            for subtitle in subtitles
        ]

        return [
            SequentialData(
                previous_line=texts[i - 1] if i > 0 else None,
                current_line=texts[i]
            ) for i in range(len(texts))
        ]

    def __prepare_prompt(self, data: SequentialData) -> str:
        user_prompt = self.user_prompt_template

        if data.previous_line is None:
            user_prompt = user_prompt.replace('Previous: "[PREV]"\n\n', '')
        else:
            user_prompt = user_prompt.replace('[PREV]', data.previous_line)

        return user_prompt.replace('[TL_LN]', data.current_line)

    def __get_result_from_api(self, prompt: str, max_retries: int = 3) -> str:
        data = None
        retries = 0

        while retries < max_retries:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.api_token}'
                },
                json={
                    'model': self.gpt_model,
                    'messages': [
                        {
                            'role': 'system',
                            'content': self.system_prompt
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                }
            )

            if response.json().get('choices') is None:
                print('An error occurred while processing the prompt:', prompt)
                retries += 1

                continue

            data = response.json().get('choices')[0]
            print(data.get('message', {}).get('content'))
            break

        if data is None:
            return '...'

        response_content: str = data.get('message', {}).get('content').replace('\n', '')

        if response_content.startswith('"') and response_content.endswith('"'):
            return response_content[1:-1]

        return response_content

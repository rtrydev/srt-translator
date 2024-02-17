from clients.gpt_client import GptClient
from clients.local_llm_client import LocalLlmClient
from clients.simple_client import SimpleClient
from clients.translate_client_base import TranslateClientBase
from enums.gpt_models import GptModels
from enums.local_llm_models import LocalLlmModels
from enums.mt_models import MTModels
from utils.file_loader import FileLoader
from utils.srt_parser import SrtParser
from utils.srt_saver import SrtSaver

if __name__ == '__main__':
    file_name = 'subs.srt'
    lines = FileLoader.load_lines(file_name)
    subtitles = SrtParser.parse_lines(lines)

    # client: TranslateClientBase = GptClient(
    #     gpt_model=GptModels.GPT3TURBO,
    #     api_token='<OPENAI TOKEN>'
    # )

    client: TranslateClientBase = SimpleClient(
        model_name=MTModels.OPUS,
        use_gpu=True
    )

    # client: TranslateClientBase = LocalLlmClient(
    #     model_name=LocalLlmModels.ALMA,
    #     use_gpu=True
    # )

    translation = client.translate(subtitles)

    SrtSaver.save(translation, f'tl_{file_name}')

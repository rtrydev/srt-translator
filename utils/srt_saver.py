from typing import List

from models.subtitle import Subtitle


class SrtSaver:
    @staticmethod
    def save(subtitles: List[Subtitle], result_path: str) -> None:
        result_string = ''

        for subtitle in subtitles:
            result_string += f'{subtitle.index}\n{subtitle.time_frame}\n{subtitle.text}\n\n'

        with open(result_path, 'w') as file:
            file.write(result_string)

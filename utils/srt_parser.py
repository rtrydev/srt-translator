from typing import List

from models.subtitle import Subtitle


class SrtParser:
    @staticmethod
    def parse_lines(lines: List[str]) -> List[Subtitle]:
        subtitles: List[Subtitle] = []
        current_sub = {}

        for i in range(len(lines)):
            if current_sub.get('index') is None:
                current_sub['index'] = lines[i].replace('\n', '')
                continue

            if current_sub.get('time_frame') is None:
                current_sub['time_frame'] = lines[i].replace('\n', '')
                continue

            if lines[i] != '\n':
                if current_sub.get('text') is None:
                    current_sub['text'] = ''

                current_sub['text'] += lines[i].replace('\n', '')
                continue

            subtitles.append(Subtitle(
                index=current_sub['index'],
                time_frame=current_sub['time_frame'],
                text=current_sub['text']
            ))
            current_sub = {}

        return subtitles

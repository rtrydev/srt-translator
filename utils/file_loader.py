from typing import List


class FileLoader:
    @staticmethod
    def load_lines(file_name: str) -> List[str]:
        with open(file_name) as file:
            lines = file.readlines()

        return lines

from dataclasses import dataclass
from typing import Optional


@dataclass
class SequentialData:
    previous_line: Optional[str]
    current_line: str

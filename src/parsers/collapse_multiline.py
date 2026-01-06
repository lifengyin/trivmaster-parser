import copy
from ..models.models import FormattedLine
from typing import List, Tuple
import re

def strip_question(text: str) -> str:
    return re.sub(r'^(\d+)\.\s*', '', text.strip())

def strip_answer(text: str) -> (str, int):
    return re.sub(r'^A:(\s+)', '', text.strip())


def collapse_multiline(formatted_lines: List[FormattedLine]) -> List[FormattedLine]:
    collapsed_lines = []

    for line in formatted_lines:
        if line.type == "question":
            line.text = strip_question(line.text)

        elif line.type == "answer":
            line.text = strip_answer(line.text)
        
        if line.type == "continuation":
            if collapsed_lines[-1].type == "question" or collapsed_lines[-1].type == "answer":
                collapsed_lines[-1].text += " " + line.text
        else:
            collapsed_lines.append(copy.deepcopy(line))

    return collapsed_lines
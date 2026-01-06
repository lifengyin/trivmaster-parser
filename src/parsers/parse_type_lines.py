from ..models.models import FormattedLine
from typing import List
import re
import copy

PATTERN_IGNORE = r'^([A-Z\s]*(QUARTER|HALF|END OF GAME)[A-Z\s]*)|(PACK[\s\d]*)$'
PATTERN_QUESTION = r'^(\d+)\.\s+(.*)'
PATTERN_ANSWER = r'^A:(\s+).*'

def parse_type_lines(lines: List[FormattedLine]) -> List[FormattedLine]:
    lines_with_types = []

    for line in lines:
        if re.match(PATTERN_IGNORE, line.text):
            line.type = "ignore"
        elif re.match(PATTERN_QUESTION, line.text):
            line.type = "question"
        elif re.match(PATTERN_ANSWER, line.text):
            line.type = "answer"
        elif line.is_bold:
            line.type = "section"
        else:
            line.type = "continuation"
        
        lines_with_types.append(copy.deepcopy(line))

    return lines_with_types
from typing import List, Dict, Any, Optional
from ..models.models import (
    BaseSection, StreakSection, JackpotSection, QuestionWithAnswer, 
    Section, FormattedLine, SectionType
)
import re

def finalize_section(current_section: Optional[Dict[str, Any]], sections: List[Section]) -> None:
    if current_section is None:
        return
    if current_section["type"] == "streak" and current_section.get("question_text"):
        sections.append(StreakSection(
            title=current_section["title"],
            description=current_section.get("description", None),
            question_text=current_section["question_text"],
            answers=current_section["answers"]
        ))
    elif current_section["type"] == "jackpot" and current_section.get("answer"):
        sections.append(JackpotSection(
            title=current_section["title"],
            description=current_section.get("description", None),
            answer=current_section["answer"],
            questions=current_section["questions"]
        ))
    elif current_section["type"] not in ["streak", "jackpot"]:
        sections.append(BaseSection(
            title=current_section["title"],
            type=current_section["type"],
            description=current_section.get("description", None),
            questions=current_section.get("questions", [])
        ))

SECTION_PATTERNS = {
    "blitz": r'^\d+-Part Blitz',
    "jailbreak": r'^(\d+-)?Part Jailbreak',
    "double jump": r'^Double Jump',
    "set of 3": r'^Set of 3',
    "set of 4": r'^Set of 4',
    "splits": r'^Splits:.*',
    "jackpot": r'^Jackpot',
    "streak": r'^Streak',
}

def parse_section_type(line: FormattedLine) -> Optional[SectionType]:
    for section_type, pattern in SECTION_PATTERNS.items():
        if re.match(pattern, line.text):
            return section_type
    return None

def parse_sections(collapsed_lines: List[FormattedLine]) -> List[Section]:
    sections: List[Section] = []
    current_section: Optional[Dict[str, Any]] = None

    for line in collapsed_lines:
        if line.type == "section":
            finalize_section(current_section, sections)
            
            section_type = parse_section_type(line)
            if section_type == "streak":
                current_section = {"type": "streak", "title": line.text, "question_text": None, "answers": []}
            elif section_type == "jackpot":
                current_section = {"type": "jackpot", "title": line.text, "questions": [], "answer": None}
            else:
                current_section = {"type": section_type, "title": line.text, "questions": []}
                
        elif line.type == "question":
            if current_section["type"] == "streak":
                current_section["question_text"] = line.text
            elif current_section["type"] == "jackpot":
                current_section["questions"].append(line.text)
            else:
                current_section["questions"].append(QuestionWithAnswer(question_text=line.text, answer=None))
                
        elif line.type == "answer":
            if current_section["type"] == "streak":
                current_section["answers"].append(line.text)
            elif current_section["type"] == "jackpot":
                current_section["answer"] = line.text
            elif current_section["questions"]:
                current_section["questions"][-1].answer = line.text
        
        elif line.type == "continuation":
            if "description" in current_section:
                current_section["description"] += " " + line.text
            else:
                current_section["description"] = line.text
    
    finalize_section(current_section, sections)
    return sections
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional, Union, Tuple

@dataclass
class Pack:
    title: str
    sections: List[Section] = field(default_factory=list)
    total_questions: int = 0

LineType = Literal["ignore", "question", "answer", "section", "continuation"]

@dataclass
class FormattedLine:
    text: str
    is_bold: bool
    underlined: List[Tuple[str, int, int]] = field(default_factory=list)
    type: Optional[LineType] = None

SectionType = Literal["blitz", "jailbreak", "double jump", "set of 3", "set of 4", "jackpot", "streak"]

@dataclass
class Section:
    title: str
    type: SectionType
    description: Optional[str] = None

@dataclass
class BaseSection(Section):
    questions: List[QuestionWithAnswer] = field(default_factory=list)

@dataclass(kw_only=True)
class StreakSection(Section):
    question_text: str
    type: SectionType = "streak"
    answers: List[Answer] = field(default_factory=list)

@dataclass(kw_only=True)
class JackpotSection(Section):
    type: SectionType = "jackpot"
    questions: List[str] = field(default_factory=list)
    answer: Answer

@dataclass
class QuestionWithAnswer:
    question_text: str
    answer: Answer

@dataclass
class Answer:
    answerline: str
    full_text: str
    accept: Options
    prompt: Options
    reject: Options

@dataclass
class Options:
    operator: Literal["AND", "OR"]
    options: List[Union[Options, str]]
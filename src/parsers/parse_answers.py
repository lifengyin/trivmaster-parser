import re
import json
from typing import List
from ..models.models import Answer, Section, BaseSection, StreakSection, JackpotSection, FormattedLine

def find_underlined(
    string: str,
) -> List[str]:
    return re.findall(r'<u>(.*?)</u>', string)

def convert_list_to_options(list: List[str], operator: str):
    if len(list) == 0:
        return []
    if len(list) == 1:
        return list[0]
    else:
        return {
            'operator': operator,
            'options': list,
        }

def parse_clause(text: str, clause_type: str):
    clause_content = text[len(clause_type):].strip()
    split_clause = clause_content.split(', ')

    total_options = []
    for split_clause_item in split_clause:
        options = find_underlined(split_clause_item)
        total_options.append(convert_list_to_options(options, 'AND'))

    return convert_list_to_options(total_options, 'OR')


def parse_answer_terms(text: str):     
    primary_text = text.split('(')[0].strip()
    primary_matched = find_underlined(primary_text)
    primary_operator = 'AND'

    clauses = [c[1:-1] for c in re.findall(r'\([^\)]+\)', text)]

    accept = []
    prompt = []
    reject = []
    
    for clause in clauses:
        if re.match(r'^(accept (either|any) |either )', clause):
            primary_operator = 'OR'

        elif re.match(r'^(prompt on partial )', clause):
            combined_underlined = ' '.join(primary_matched)
            for partial_answer in combined_underlined.split(' '):
                prompt.append(partial_answer)
        
        elif clause.startswith('accept: '):
            accept.append(parse_clause(clause, 'accept: '))
        
        elif clause.startswith('prompt on: '):
            prompt.append(parse_clause(clause, 'prompt on: '))
        
        elif clause.startswith('reject:'):
            reject.append(parse_clause(clause, 'reject:'))
    
    accept.insert(0, convert_list_to_options(primary_matched, primary_operator))
    
    return {
        'accept': convert_list_to_options(accept, 'OR'),
        'prompt': convert_list_to_options(prompt, 'OR'),
        'reject': convert_list_to_options(reject, 'OR'),
    }

def parse_answer_operators(text: str) -> Answer:
    operator = ""
    if (' OR ' in text):
        operator = "OR"
    elif (' AND ' in text):
        operator = "AND"
    
    if operator: 
        split_text = text.split(operator)
    else:
        split_text = [text]

    accept = []
    prompt = []
    reject = []
    for split_text_item in split_text:
        options = parse_answer_terms(split_text_item.strip())
        accept.append(options['accept'])
        if len(options['prompt']):
            prompt.append(options['prompt'])
        if len(options['reject']):
            reject.append(options['reject'])

    return {
        'answer_text': text,
        'accept': convert_list_to_options(accept, operator),
        'prompt': convert_list_to_options(prompt, operator),
        'reject': convert_list_to_options(reject, 'OR'),
    }


def parse_answers_in_sections(sections: List[Section]) -> List[Section]:
    for section in sections:
        if isinstance(section, BaseSection):
            for question in section.questions:
                question.answer = parse_answer_operators(question.answer)
        elif isinstance(section, StreakSection):
            for i, answer in enumerate(section.answers):
                section.answers[i] = parse_answer_operators(answer)
        elif isinstance(section, JackpotSection):
            section.answer = parse_answer_operators(section.answer)
    
    return sections
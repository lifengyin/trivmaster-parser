from ..models.models import FormattedLine
import json

MAX_Y_DISTANCE = 2
MAX_X1_DISTANCE = 0.5
MAX_X2_DISTANCE = 2

def is_line_bold(line_chars):
    non_whitespace_chars = [c for c in line_chars if c.get("text", "").strip()]
    
    if not non_whitespace_chars:
        return False
    
    for char in non_whitespace_chars:
        fontname = char.get("fontname", "").lower()
        if "bold" not in fontname:
            return False
    return True

def extract_underlined_ranges(text_line, underlines, line_chars):
    """Extract ranges of underlined text as (start_index, end_index) tuples."""
    underlined_ranges = []

    for underline in underlines:
        if (
            abs(underline['top'] - underline['bottom']) <= 2 and
            0 < text_line['bottom'] - underline['top'] < MAX_Y_DISTANCE
        ):
            underlined_chars = [
                c for c in line_chars
                if underline['x0'] - MAX_X1_DISTANCE <= c['x0'] <= underline['x1'] - MAX_X2_DISTANCE
            ]

            if underlined_chars:
                start_index = line_chars.index(underlined_chars[0])
                end_index = line_chars.index(underlined_chars[-1]) + 1
                underlined_ranges.append((start_index, end_index))

    return underlined_ranges


def insert_underline_tags(text, underlined_ranges):
    reversed_ranges = sorted(underlined_ranges, key=lambda x: x[0], reverse=True)
    
    for start_index, end_index in reversed_ranges:
        underlined_text = text[start_index:end_index]
        text = text[:start_index] + f"<u>{underlined_text}</u>" + text[end_index:]
    
    return text


def extract_to_formatted_lines(pdf):
    formatted_lines = []

    for page in pdf.pages[1:]:
        for text_line in page.extract_text_lines(keep_blank_chars=True):
            line_chars = sorted(text_line["chars"], key=lambda c: c["x0"])
            text = "".join([c["text"] for c in line_chars])
            
            underlined_ranges = extract_underlined_ranges(text_line, page.lines, line_chars)
            text_with_underlines = insert_underline_tags(text, underlined_ranges)
            
            formatted_lines.append(FormattedLine(
                text=text_with_underlines,
                is_bold=is_line_bold(line_chars)
            ))

    return formatted_lines
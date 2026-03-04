import pdfplumber

from ..models.models import Pack

from .find_pdfs import find_pdfs
from .extract_to_formatted_lines import extract_to_formatted_lines
from .parse_type_lines import parse_type_lines
from .collapse_multiline import collapse_multiline
from .parse_sections import parse_sections
from .parse_answers import parse_answers_in_sections
from .write_output import write_output


def parse_pdfs(pdf_dir: str, output_dir: str):
    pdf_paths = find_pdfs(pdf_dir)

    for pdf_path in pdf_paths:
        with pdfplumber.open(pdf_path) as pdf:
            formatted_lines = extract_to_formatted_lines(pdf)
            formatted_lines_with_types = parse_type_lines(formatted_lines)
            collapsed_lines = collapse_multiline(formatted_lines_with_types)
            sections = parse_sections(collapsed_lines)
            sections_with_answers = parse_answers_in_sections(sections)

            pack = Pack(
                title=pdf_path.stem,
                sections=sections_with_answers
            )

            write_output(pack, output_dir, pdf_dir, pdf_path)

if __name__ == "__main__":
    parse_pdfs("pdfs", "dist")
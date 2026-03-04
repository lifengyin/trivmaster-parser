from pathlib import Path

def find_pdfs(dir_path):
    pdf_dir = Path(dir_path)
    if not pdf_dir.exists():
        raise FileNotFoundError(f"Directory {dir_path} does not exist.")

    pdf_paths = [p for p in pdf_dir.rglob("*.pdf") if p.is_file()]
    if not pdf_paths:
        raise FileNotFoundError(f"No PDF files found in {dir_path}.")

    return pdf_paths
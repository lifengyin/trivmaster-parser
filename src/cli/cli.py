import typer
from pathlib import Path
from typing import Optional

from ..parsers.main import process_pdfs

app = typer.Typer(help="PDF Scraper CLI - Extract questions and answers from PDF files")

@app.command()
def scrape(
    pdf_dir: Optional[str] = typer.Option(
        "./pdfs",
        "--pdf-dir",
        "-p",
        help="Directory containing PDF files to process"
    ),
    output_dir: Optional[str] = typer.Option(
        "./dist",
        "--output-dir",
        "-o",
        help="Directory to write output JSON files"
    ),
):
    """
    Scrape PDF files and extract questions, answers, and sections.
    """
    typer.echo(f"Processing PDFs from: {pdf_dir}")
    typer.echo(f"Writing output to: {output_dir}")
    
    try:
        process_pdfs(pdf_dir, output_dir)
        typer.echo(typer.style("✓ Successfully processed all PDFs", fg=typer.colors.GREEN))
    except FileNotFoundError as e:
        typer.echo(typer.style(f"✗ Error: {e}", fg=typer.colors.RED), err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(typer.style(f"✗ Unexpected error: {e}", fg=typer.colors.RED), err=True)
        raise typer.Exit(1)

def main():
    app()

if __name__ == "__main__":
    main()


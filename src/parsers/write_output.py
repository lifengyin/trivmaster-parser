import json
from dataclasses import asdict
from pathlib import Path

from ..models.models import Pack

def write_output(pack: Pack, output_dir: str, pdf_dir: str, pdf_path: Path) -> None:
    output_relative_path = pdf_path.relative_to(Path(pdf_dir)).with_suffix(".json")
    output_path = Path(output_dir) / output_relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        pack_dict = asdict(pack)
        json.dump(pack_dict, f, indent=4)
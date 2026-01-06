from typing import List
from ..models.models import Pack
import json
from dataclasses import asdict

def write_output(pack: Pack) -> None:
    with open('dist/' + pack.title + ".json", "w") as f:
        pack_dict = asdict(pack)
        json.dump(pack_dict, f, indent=4)
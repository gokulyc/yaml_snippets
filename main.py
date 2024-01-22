import json
import yaml
import pathlib
from rich import print as rprint
import os

ROOT_YAML_DIR = pathlib.Path("yaml_snips").resolve()
ROOT_JSON_OUT_DIR = pathlib.Path("json_out").resolve()


def generate_json_from_yaml(yaml_file_path: os.PathLike, json_out_dir: os.PathLike):
    json_file_name = f"{yaml_file_path.stem}.json"
    out = yaml.safe_load(yaml_file_path.read_text())
    # rprint(out)
    json.dump(
        out,
        (json_out_dir / json_file_name).open(mode="w"),
        default=str,
    )


if __name__ == "__main__":
    file_gen = ROOT_YAML_DIR.rglob("*.yaml")
    # rprint(list(file_gen))
    for yaml_file_path in file_gen:
        generate_json_from_yaml(yaml_file_path, ROOT_JSON_OUT_DIR)
        rprint(f"Wrote {yaml_file_path.stem} !!!")
    
    # for yaml_file_path in file_gen:
    #     out = yaml.safe_load(yaml_file_path.read_text())
    #     rprint(out)
    #     rprint("--------------")

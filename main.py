import json
import yaml
import pathlib
from rich import print as rprint
import os
from yaml.composer import ComposerError
from dotenv import load_dotenv

rprint(f"Is .env loaded : {load_dotenv()}")

IS_DEBUG = True if os.getenv("DEBUG") == "True" else False

# rprint(f"IS_DEBUG : {IS_DEBUG=} {type(IS_DEBUG)}")

ROOT_YAML_DIR = pathlib.Path("yaml_snips").resolve()
ROOT_JSON_OUT_DIR = pathlib.Path("json_out").resolve()


def generate_json_from_yaml(yaml_file_path: pathlib.Path, json_out_dir: pathlib.Path):
    json_file_name = f"{yaml_file_path.stem}.json"
    try:
        out = yaml.safe_load(yaml_file_path.read_text())
        json.dump(
            out,
            (json_out_dir / json_file_name).open(mode="w"),
            default=str,
        )
        rprint(f"Wrote {json_file_name} !")
    except ComposerError:
        rprint("Multi docs found in stream...")
        out = yaml.safe_load_all(yaml_file_path.read_text())
        for i, doc in enumerate(out):
            json_file_name = f"{yaml_file_path.stem}_{i}.json"
            json.dump(
                doc,
                (json_out_dir / json_file_name).open(mode="w"),
                default=str,
            )
            rprint(f"Wrote {json_file_name} !!!")


def rprint_yaml_to_json(yaml_file_path: pathlib.Path):
    try:
        out = yaml.safe_load(yaml_file_path.read_text())
        rprint(f"{yaml_file_path.stem}")
        rprint(out)
        rprint("--------------")
    except ComposerError as e:
        rprint("Multi docs found in stream...")
        out = yaml.safe_load_all(yaml_file_path.read_text())
        rprint(list(out))
        rprint("--------------")


if __name__ == "__main__":
    file_path_list = list(ROOT_YAML_DIR.rglob("*.yaml"))
    rprint(f"File(s) found : {len(file_path_list)}")

    if IS_DEBUG:
        for yaml_file_path in file_path_list:
            rprint_yaml_to_json(yaml_file_path)
    else:
        for yaml_file_path in file_path_list:
            generate_json_from_yaml(yaml_file_path, ROOT_JSON_OUT_DIR)

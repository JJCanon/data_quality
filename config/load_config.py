# Libraries
from pathlib import Path
import yaml

# Function to read yaml files
def load_yaml(filename="parameters.yaml"):
    project_root = Path(__file__).resolve().parent.parent
    yaml_path = project_root / "config" / filename

    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
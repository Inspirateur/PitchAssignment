import json
from pathlib import Path


def log(filename, row):
	Path("logs").mkdir(exist_ok=True)
	with open(f"logs/{filename}.jsonl", "a") as f:
		json.dump(row, f)
		f.write("\n")

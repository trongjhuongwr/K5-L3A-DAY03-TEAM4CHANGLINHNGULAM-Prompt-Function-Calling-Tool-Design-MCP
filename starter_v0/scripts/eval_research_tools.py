"""Run only the three new read-only tool routing cases, without delivery cases."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
NEW_CASES = {"G11_resolve_account_directory", "G12_deduplicate_existing_items", "G13_collect_claim_evidence"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", default="openrouter")
    parser.add_argument("--model", default=None)
    parser.add_argument("--version", default="tools-v1")
    args = parser.parse_args()
    dataset = json.loads((ROOT / "data" / "eval_group.json").read_text(encoding="utf-8"))
    dataset["cases"] = [case for case in dataset["cases"] if case["id"] in NEW_CASES]
    if {case["id"] for case in dataset["cases"]} != NEW_CASES:
        raise SystemExit("Missing expected research-tool cases in eval_group.json")
    dataset["dataset_id"] = "research_tools_extension"
    dataset["description"] = "Read-only routing subset G11-G13; does not exercise send."
    output = ROOT / "analysis" / "eval_research_tools.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(dataset, ensure_ascii=False, indent=2), encoding="utf-8")
    command = [
        sys.executable, str(ROOT / "run_eval.py"), "--provider", args.provider,
        "--version", args.version, "--suite", "group", "--eval-cases", str(output),
    ]
    if args.model:
        command.extend(["--model", args.model])
    subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()

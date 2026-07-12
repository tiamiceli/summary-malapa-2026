"""Run the MaLAPA 2026 analysis pipeline end to end.

Executes the two notebooks in order, headless (like scripts), so the data
side-effects are regenerated without opening JupyterLab:

  1. step_1_prepare_data.ipynb          -> writes step_1_output/
  2. step_2_explore_contributions.ipynb -> reads step_1_output/, writes step_2_output/

Usage:
    uv run main.py
"""

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

NOTEBOOKS = [
    "step_1_prepare_data.ipynb",
    "step_2_explore_contributions.ipynb",
]


def run_notebook(notebook: str) -> None:
    print(f"→ Running {notebook} ...", flush=True)
    # `jupyter execute` runs the notebook top to bottom without saving outputs
    # back into the .ipynb; run from the repo root so the notebooks' relative
    # paths (source_data/, step_1_output/, ...) resolve.
    subprocess.run(["jupyter", "execute", notebook], cwd=REPO_ROOT, check=True)
    print(f"✓ Finished {notebook}\n", flush=True)


def main() -> None:
    for notebook in NOTEBOOKS:
        run_notebook(notebook)
    print("Pipeline complete. Outputs in step_1_output/ and step_2_output/.")


if __name__ == "__main__":
    main()

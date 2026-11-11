"""Run the task against four agents in fresh workspaces and print their rewards.

    python run_demo.py
"""
import importlib.util
import shutil
import tempfile
from pathlib import Path

from grader.grade import grade

ROOT = Path(__file__).parent


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


AGENTS = {
    "does nothing": lambda ws: None,
    "trusts the emails": load("baselines/naive_trust_emails.py", "naive").run,
    "tampers with the inputs": load("baselines/tamper_inputs.py", "tamper").tamper,
    "reference solution": load("solution/reconcile.py", "ref").reconcile,
}

if __name__ == "__main__":
    for name, agent in AGENTS.items():
        ws = Path(tempfile.mkdtemp(prefix="workspace-"))
        try:
            shutil.copytree(ROOT / "task" / "files", ws, dirs_exist_ok=True)
            agent(ws)
            reward, problems = grade(ws)
            print(f"{name:<26} reward = {reward}")
            for p in problems[:3]:
                print(f"    - {p}")
        finally:
            shutil.rmtree(ws, ignore_errors=True)

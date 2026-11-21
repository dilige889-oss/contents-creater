"""Prompt templates loaded from YAML, expanded into concrete jobs."""
from dataclasses import dataclass, field
from itertools import product
from pathlib import Path

import yaml

from .safety import check_prompt, with_safety_negative


@dataclass
class Job:
    name: str
    prompt: str
    negative: str
    width: int = 1024
    height: int = 1344
    seed: int = 0
    steps: int = 30
    guidance: float = 6.0
    meta: dict = field(default_factory=dict)


def load_template(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def expand(template: dict) -> list[Job]:
    """Every combination of `variables` x `seeds` becomes one Job."""
    base = template["prompt"]
    variables: dict = template.get("variables", {})
    seeds = template.get("seeds", [0])
    negative = with_safety_negative(template.get("negative", ""))
    keys = list(variables)
    combos = list(product(*(variables[k] for k in keys))) or [()]

    jobs = []
    for i, combo in enumerate(combos):
        values = dict(zip(keys, combo))
        prompt = base.format(**values)
        check_prompt(prompt)
        for seed in seeds:
            jobs.append(Job(
                name=f"{template['name']}_{i:03d}_s{seed}",
                prompt=prompt,
                negative=negative,
                width=template.get("width", 1024),
                height=template.get("height", 1344),
                seed=seed,
                steps=template.get("steps", 30),
                guidance=template.get("guidance", 6.0),
                meta=values,
            ))
    return jobs

import tempfile
from pathlib import Path

import pytest

from creator.cli import main
from creator.prompts import expand, load_template
from creator.safety import UnsafePromptError, check_prompt

ROOT = Path(__file__).resolve().parent.parent


def test_expand_counts_combinations():
    jobs = expand(load_template(ROOT / "templates/editorial_portrait.yaml"))
    assert len(jobs) == 3 * 2 * 2 * 2
    assert all("lingerie" in j.negative for j in jobs)


@pytest.mark.parametrize("bad", ["woman in lingerie", "nude portrait", "sexy pose"])
def test_blocks_unsafe_prompts(bad):
    with pytest.raises(UnsafePromptError):
        check_prompt(bad)


def test_allows_fashion_prompt():
    check_prompt("editorial portrait, camel wool coat, hotel lounge")


def test_cli_end_to_end_mock():
    with tempfile.TemporaryDirectory() as d:
        main([str(ROOT / "templates/consistent_character.yaml"), "--out", d, "--limit", "3"])
        out = Path(d) / "character_mina"
        assert len(list(out.glob("*.png"))) == 3
        assert (out / "collage.jpg").exists()
        assert (out / "manifest.json").exists()

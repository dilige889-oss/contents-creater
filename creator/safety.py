"""Content guard: keeps prompts in safe-for-work fashion/editorial territory."""
import re

BLOCKED_TERMS = [
    "nude", "naked", "nsfw", "topless", "lingerie", "underwear", "panties",
    "thong", "bra", "bikini", "cleavage", "crotch", "erotic", "sexy", "seductive",
    "explicit", "porn", "fetish", "see-through", "sheer", "upskirt", "spread legs",
    "child", "teen", "minor", "schoolgirl", "loli",
    "celebrity", "lookalike", "look-alike", "in the style of a real person",
]

SAFETY_NEGATIVE = (
    "nsfw, nudity, lingerie, underwear, cleavage, suggestive pose, "
    "revealing clothing, see-through fabric"
)


class UnsafePromptError(ValueError):
    pass


def check_prompt(text: str) -> None:
    """Raise UnsafePromptError if the prompt contains a blocked term."""
    lowered = text.lower()
    hits = [t for t in BLOCKED_TERMS if re.search(rf"\b{re.escape(t)}\b", lowered)]
    if hits:
        raise UnsafePromptError(f"Blocked terms in prompt: {', '.join(hits)}")


def with_safety_negative(negative: str) -> str:
    return f"{negative}, {SAFETY_NEGATIVE}" if negative else SAFETY_NEGATIVE

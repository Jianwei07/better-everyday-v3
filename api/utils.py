# api/utils.py

import re
from typing import List, Dict, Any

def extract_eva_response(raw: str) -> dict:
    import re
    patterns = [r"(?<=RESPONSE:)(.*)", r"(?<=ANSWER:)(.*)"]
    answer = None
    for pat in patterns:
        match = re.search(pat, raw, re.DOTALL)
        # Fix: Only treat as answer if it's not empty after stripping
        if match:
            candidate = match.group(1).strip()
            if candidate and candidate.upper() != "ANSWER:":
                answer = candidate
                break
    if not answer:
        # If no marker or only empty after marker, fallback to raw (but cleaned)
        answer = raw.strip()
        # If it's still only 'ANSWER:' or blank, fallback to default
        if not answer or answer.upper() == "ANSWER:":
            answer = "I'm sorry, I couldn't find a specific answer for you right now."

    # Remove leading dashes/markdown and split blocks
    answer = re.sub(r"^[-–—]+\s*", "", answer)
    answer = answer.strip()
    blocks = [b.strip() for b in re.split(r"(?:\n\s*[-•*]\s+|\n\d+\.\s+)", answer) if b.strip()]
    return {
        "cleaned_text": answer,
        "answer_blocks": blocks,
        "raw": raw.strip()
    }
# api/utils.py (Optimized for robust handling of empty/malformed LLM outputs)

import re
from typing import List, Dict, Any

def extract_eva_response(raw_llm_output: Any) -> dict:
    # --- Debugging: Keep these crucial debug prints ---
    print(f"[DEBUG] extract_eva_response: Input type before any processing: {type(raw_llm_output)}")
    print(f"[DEBUG] extract_eva_response: Input raw (first 200 chars): '{str(raw_llm_output)[:200]}...'")
    print(f"[DEBUG] extract_eva_response: Input raw (FULL REPR for problematic cases): {repr(raw_llm_output)}")

    # --- Aggressive Type Coercion (Still Needed as a Guard) ---
    if not isinstance(raw_llm_output, str):
        print(f"[CRITICAL ERROR] extract_eva_response received non-string input! Attempting aggressive str() conversion.")
        try:
            raw_llm_output = str(raw_llm_output)
            print(f"[CRITICAL ERROR] Conversion successful. New type: {type(raw_llm_output)}. New repr: {repr(raw_llm_output)}")
        except Exception as e:
            print(f"[CRITICAL ERROR] Failed to convert to str! Error: {e}")
            raw_llm_output = f"Error: Could not process LLM response. Raw input was problematic. Error: {e}"

    # --- Step 1: Initial cleanup of common LLM artifacts and unwanted prefixes ---
    cleaned_output = raw_llm_output.strip()

    initial_strip_patterns = r"""
        ^\s*(AI:|Response:|Answer:|Revised Answer:)\s*| # LLM markers
        ^\s*"?(?:In the podcast|Great question|I\s*do not know based on the provided context|The host or guest name is not available in the provided context)\.?\s*"?\s*| # Conversational/Fallback intros
        ^\s*---+\s*| # Horizontal rules
        ^\s*#+\s*.*?\n| # Markdown headers
        ^\s*USER QUESTION:.*?\n| # Repeated prompt elements
        ^\s*CONTEXT:.*?\n|
        ^\s*INSTRUCTIONS:.*?\n|
        ^\s*ORIGINAL (?:ANSWER|RESPONSE|ANSWER TO CRITIQUE):.*?\n|
        ^\s*PREVIOUS ANSWER:.*?\n|
        ^\s*\d+\.\s+If the ORIGINAL ANSWER is.*?:\s*| # Specific instruction line repetition
        ^\s*(?:Yes, )?it (?:is )?true that the brain and body are connected\.?\s*| # Specific observed LLM opening
        ^\s*[Hh]i there!?\s*| # "Hi there!"
        ^\s*[Tt]hanks for reaching out\.?\s* # "Thanks for reaching out."
    """
    for _ in range(3): # Run multiple times to catch nested/sequential patterns
        new_cleaned_output = re.sub(initial_strip_patterns, "", cleaned_output, flags=re.DOTALL | re.IGNORECASE | re.VERBOSE).strip()
        if new_cleaned_output == cleaned_output:
            break
        cleaned_output = new_cleaned_output

    # Remove wrapping quotes
    if cleaned_output.startswith('"') and cleaned_output.endswith('"'):
        cleaned_output = cleaned_output.strip('"')

    # --- Step 2: Extract the primary answer, cutting off unwanted follow-ups ---
    final_answer = cleaned_output

    unwanted_sections_markers = [
        "QUESTION:", "INSTRUCTIONS:", "CONTEXT:",
        "ORIGINAL ANSWER:", "PREVIOUS ANSWER:", "REVISED ANSWER:", "RESPONSE:",
        "ORIGINAL ANSWER TO CRITIQUE:"
    ]
    for marker in unwanted_sections_markers:
        if marker in final_answer.upper():
            final_answer = final_answer.split(marker)[0].strip()
            break

    # --- Step 3: Handle numeric list formatting issues (FIXED REGEX) ---
    # Fix awkward list numbering (e.g., "1        1. Prioritize" to "1. Prioritize")
    try:
        final_answer = re.sub(r"^\s*\d+\s*(\d+\.\s+)", r"\1", final_answer, flags=re.MULTILINE).strip()
    except TypeError as te:
        print(f"[CRITICAL ERROR] TypeError during list formatting re.sub! Error: {te}")
        final_answer = f"Error processing list format: {te}. Raw: {raw_llm_output[:100]}..."
    
    # Standardize bullet/number spacing (e.g., "-item" to "- item" or "1.item" to "1. item")
    final_answer = re.sub(r"^\s*([*-]|\d+\.)\s*", r"\1 ", final_answer, flags=re.MULTILINE).strip()

    # --- Step 4: Handle empty or generic answers after all processing ---
    # Enhanced check for truly empty or unhelpful output after cleaning
    if not final_answer or final_answer in ["-", ".", ""] or re.fullmatch(r"^(#+\s*.*?\n*)*\s*$", final_answer.strip(), re.DOTALL | re.IGNORECASE):
        final_answer = "I'm sorry, I couldn't find a specific answer for you right now based on the available context."
    elif final_answer.upper().startswith("THE CONTEXT DOES NOT CONTAIN THE ANSWER"):
        final_answer = "I don't know based on the provided context."
    elif final_answer.upper().startswith("I DON'T KNOW BASED ON THE PROVIDED CONTEXT."):
        pass


    # --- Step 5: Split into blocks for frontend display ---
    try:
        blocks = [b.strip() for b in re.split(r"(?:\n\s*[-•*]\s+|\n\d+\.\s+)", final_answer) if b.strip()]
    except TypeError as te:
        print(f"[CRITICAL ERROR] TypeError during final re.split for blocks! Error: {te}")
        blocks = [f"Error during final formatting: {te}. Please try again."]
    
    if not blocks and final_answer:
        blocks = [final_answer]
    elif not blocks and not final_answer:
        final_answer = "I'm sorry, I couldn't find a specific answer for you right now based on the available context."
        blocks = [final_answer]

    return {
        "cleaned_text": final_answer,
        "answer_blocks": blocks,
        "raw": raw_llm_output.strip()
    }
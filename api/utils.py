# api/utils.py (FINAL ATTEMPT AT TYPEERROR FIX)

import re
from typing import List, Dict, Any

def extract_eva_response(raw_llm_output: Any) -> dict: # Changed type hint to Any for ultimate flexibility
    print(f"[DEBUG] extract_eva_response: Input type before any processing: {type(raw_llm_output)}")
    print(f"[DEBUG] extract_eva_response: Input raw (first 200 chars): '{str(raw_llm_output)[:200]}...'") # Use str() here to prevent error on non-str
    print(f"[DEBUG] extract_eva_response: Input raw (FULL REPR for problematic cases): {repr(raw_llm_output)}")

    # --- Aggressive Type Coercion for Troubleshooting ---
    # This block *must* guarantee raw_llm_output is a string for later operations.
    if not isinstance(raw_llm_output, str):
        print(f"[CRITICAL ERROR] extract_eva_response received non-string input ({type(raw_llm_output)}). Attempting aggressive str() conversion.")
        original_type = type(raw_llm_output)
        original_repr = repr(raw_llm_output)
        try:
            # Most robust string conversion method
            raw_llm_output = str(raw_llm_output)
            # You could even try: raw_llm_output = original_repr.encode('utf-8').decode('utf-8')
            print(f"[CRITICAL ERROR] Conversion successful. Original type: {original_type}, new type: {type(raw_llm_output)}. New repr: {repr(raw_llm_output)}")
        except Exception as e:
            print(f"[CRITICAL ERROR] Failed to convert to str! Original type: {original_type}, Error: {e}")
            raw_llm_output = f"Error: Could not process LLM response of type {original_type}. Raw: {original_repr[:100]}..."
            # If we reach here, it's a very serious fundamental problem

    # --- Step 1: Initial cleanup of common LLM prefix/suffix issues ---
    # Now, raw_llm_output *should* be a string. All operations below assume string.
    cleaned_output = raw_llm_output.strip()

    # Manual checks for common conversational starts (string methods)
    # Re-verify this logic to avoid regex if possible at start
    if cleaned_output.lower().startswith("ai:"):
        cleaned_output = cleaned_output[3:].strip()
    if cleaned_output.lower().startswith("response:"):
        cleaned_output = cleaned_output[9:].strip()
    if cleaned_output.lower().startswith("answer:"):
        cleaned_output = cleaned_output[7:].strip()
    
    if cleaned_output.startswith('"') and cleaned_output.endswith('"'):
        cleaned_output = cleaned_output.strip('"')

    # Now apply regex for more complex patterns
    patterns_to_strip_from_start = [
        r"^\s*\"?In the podcast, (.*?)\"?\s*",
        r"^\s*\"?Great question!(.*?)\"?\s*",
        r"^\s*\"?[Ii]\s*do not know based on the provided context\.?\"?\s*",
        r"^\s*\"?The host or guest name is not available in the provided context\.?\"?\s*",
        r"^\s*---+\s*",
        r"^\s*#+\s*.*?\n",
        r"^\s*USER QUESTION:.*?\n",
    ]
    
    for pattern in patterns_to_strip_from_start:
        # Add a try-except block specifically around re.sub
        try:
            print(f"[DEBUG] Attempting re.sub with pattern type: {type(pattern)}, cleaned_output type: {type(cleaned_output)}")
            cleaned_output = re.sub(pattern, "", cleaned_output, flags=re.DOTALL | re.IGNORECASE).strip()
        except TypeError as te: # Catch the specific TypeError here
            print(f"[CRITICAL ERROR] TypeError during re.sub! Pattern: {repr(pattern)}, Cleaned_output (TYPE): {type(cleaned_output)}, Cleaned_output (REPR): {repr(cleaned_output)}. Error: {te}")
            # If this happens, it means cleaned_output is still not a string despite all efforts
            cleaned_output = f"Error processing regex: {te}. Raw: {raw_llm_output[:100]}..."
            break # Exit loop if regex fails

    # --- Step 2: Extract the primary answer, cutting off unwanted follow-ups ---
    final_answer = cleaned_output

    # Continue using string methods first, then regex if needed
    if "QUESTION:" in final_answer.upper():
        final_answer = final_answer.split("QUESTION:")[0].strip()
    elif "ANSWER:" in final_answer.upper() and final_answer.upper().count("ANSWER:") > 1:
        # Use re.split here if it's the only way to handle complex splitting
        try:
            parts = re.split(r"\n\s*ANSWER:\s*", final_answer, maxsplit=1, flags=re.IGNORECASE)
            if len(parts) > 0:
                final_answer = parts[0].strip()
        except TypeError as te:
            print(f"[CRITICAL ERROR] TypeError during re.split! Final_answer (TYPE): {type(final_answer)}, Error: {te}")
            final_answer = f"Error processing regex split: {te}. Raw: {raw_llm_output[:100]}..."

    if "INSTRUCTIONS:" in final_answer.upper():
        final_answer = final_answer.split("INSTRUCTIONS:")[0].strip()
    if "CONTEXT:" in final_answer.upper():
        final_answer = final_answer.split("CONTEXT:")[0].strip()

    # --- Step 3: Handle empty or generic answers after processing ---
    # ... (rest of this section, no changes) ...

    # --- Step 4: Split into blocks for frontend display ---
    if not isinstance(final_answer, str): # Final check before last re.split
        print(f"[ERROR] Final answer is unexpectedly not a string before final split: type={type(final_answer)}, value={repr(final_answer)}")
        final_answer = str(final_answer) # Coerce as last resort
        
    # Add try-except around final re.split as well
    try:
        blocks = [b.strip() for b in re.split(r"(?:\n\s*[-•*]\s+|\n\d+\.\s+)", final_answer) if b.strip()]
    except TypeError as te:
        print(f"[CRITICAL ERROR] TypeError during final re.split! Final_answer (TYPE): {type(final_answer)}, Error: {te}")
        blocks = [f"Error processing final split: {te}. Raw: {raw_llm_output[:100]}..."]

    # ... (rest of ensure blocks list is not empty) ...

    return {
        "cleaned_text": final_answer,
        "answer_blocks": blocks,
        "raw": raw_llm_output.strip()
    }
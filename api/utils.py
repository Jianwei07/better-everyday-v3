# api/utils.py (SIMPLIFIED VERSION)

import re
from typing import List, Dict, Any

def extract_eva_response(raw_llm_output: str) -> dict:
    """
    Extracts the answer from raw LLM output, handles common LLM artifacts,
    and formats it into structured blocks.
    """
    print(f"[DEBUG] extract_eva_response received type: {type(raw_llm_output)}")
    print(f"[DEBUG] extract_eva_response received raw (first 200 chars): '{raw_llm_output[:200]}...'")

    # --- Step 1: Initial cleanup of common LLM prefix/suffix issues ---
    # Remove leading/trailing whitespace
    cleaned_output = raw_llm_output.strip()

    # If the LLM starts with conversational filler despite instructions, remove it.
    # This is a heuristic. Adjust patterns based on common unwanted outputs from your LLM.
    # Example fillers: "Hi, I'm Eva...", "Great question!", "Answer:\n", "Response:\n"
    patterns_to_strip_from_start = [
        r"^\s*(AI:|Response:|Answer:)\s*", # AI: or Response: or Answer:
        r"^\s*\"?In the podcast, (.*?)\"?\s*", # "In the podcast..."
        r"^\s*\"?Great question!(.*?)\"?\s*", # "Great question!"
        r"^\s*\"?[Ii]\s*do not know based on the provided context\.?\"?\s*", # "I do not know..."
        r"^\s*\"?The host or guest name is not available in the provided context\.?\"?\s*", # "The host or guest name is not available..."
        r"^\s*---+\s*", # Any leading '---'
        r"^\s*#+\s*.*?\n", # Any leading markdown headers (e.g., # Dr Tara Swart)
        r"^\s*USER QUESTION:.*?\n", # If LLM repeats user question at start
    ]
    
    for pattern in patterns_to_strip_from_start:
        cleaned_output = re.sub(pattern, "", cleaned_output, flags=re.DOTALL | re.IGNORECASE).strip()

    # Remove wrapping quotes if present (e.g., LLM sometimes wraps the entire answer in quotes)
    if cleaned_output.startswith('"') and cleaned_output.endswith('"'):
        cleaned_output = cleaned_output.strip('"')

    # --- Step 2: Extract the primary answer, cutting off unwanted follow-ups ---
    final_answer = cleaned_output

    # Cut off if LLM starts another 'QUESTION:' or 'ANSWER:' turn
    if "QUESTION:" in final_answer.upper():
        final_answer = final_answer.split("QUESTION:")[0].strip()
    # If there are multiple "ANSWER:" markers, take only the first part
    elif "ANSWER:" in final_answer.upper() and final_answer.upper().count("ANSWER:") > 1:
        parts = re.split(r"\n\s*ANSWER:\s*", final_answer, maxsplit=1, flags=re.IGNORECASE)
        if len(parts) > 0: # Ensure there's at least one part
            final_answer = parts[0].strip() # Take content before the second "ANSWER:"
        
    # Also cut off any leftover prompt instructions the LLM might repeat
    if "INSTRUCTIONS:" in final_answer.upper():
        final_answer = final_answer.split("INSTRUCTIONS:")[0].strip()
    if "CONTEXT:" in final_answer.upper(): # If LLM mistakenly repeats context section
        final_answer = final_answer.split("CONTEXT:")[0].strip()


    # --- Step 3: Handle empty or generic answers after processing ---
    if not final_answer: # If answer is empty after all cleaning
        final_answer = "I'm sorry, I couldn't find a specific answer for you right now based on the available context."
    elif final_answer.upper().startswith("THE HOST OR GUEST NAME IS NOT AVAILABLE"):
        pass # Keep this specific response as is
    elif final_answer.upper() == "I DO NOT KNOW BASED ON THE PROVIDED CONTEXT.":
        pass # Keep this specific response as is


    # --- Step 4: Split into blocks for frontend display ---
    # Ensure final_answer is a string before splitting.
    # This check should ideally never trigger if the `raw_llm_output` always comes in as string.
    if not isinstance(final_answer, str):
        print(f"[ERROR] Final answer is not a string before splitting: type={type(final_answer)}, value={final_answer}")
        final_answer = str(final_answer) # Coerce to string to prevent TypeError on split
        
    blocks = [b.strip() for b in re.split(r"(?:\n\s*[-•*]\s+|\n\d+\.\s+)", final_answer) if b.strip()]
    
    # Ensure blocks list is not empty if a final_answer exists
    if not blocks and final_answer:
        blocks = [final_answer] # Put the whole answer in one block if no separators found
    elif not blocks and not final_answer: # If both are empty (should be caught by final_answer logic above)
        final_answer = "I'm sorry, I couldn't find a specific answer for you right now based on the available context."
        blocks = [final_answer]

    return {
        "cleaned_text": final_answer,
        "answer_blocks": blocks,
        "raw": raw_llm_output.strip() # Keep original raw for debug if needed
    }
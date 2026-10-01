import os
import hashlib
import time
import re
import logging
from google import genai
from pydantic import ValidationError
from typing import List, Optional
from app.schemas.flashcard import Flashcard, FlashcardOutput

logger = logging.getLogger(__name__)

def _fetch_cards(client: genai.Client, model_name: str, prompt: str) -> List[FlashcardOutput]:
    max_retries = 2
    last_error = None

    for attempt in range(max_retries):
        try:
            logger.info(f"Generating flashcards using model: {model_name}, attempt: {attempt + 1}")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=0.3,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=8192,
                    response_mime_type="application/json",
                    response_schema=list[FlashcardOutput],
                ),
            )
            
            if not hasattr(response, 'parsed') or response.parsed is None:
                raise Exception("Response did not contain parsed structured output")
                
            return response.parsed

        except Exception as e:
            last_error = str(e)
            logger.error(f"Attempt {attempt + 1} failed: {last_error}")
            
            if "429" in last_error or "RESOURCE_EXHAUSTED" in last_error:
                match = re.search(r'retry in ([\d\.]+)s', last_error)
                if match:
                    delay = float(match.group(1)) + 1
                    if delay > 30:
                        raise Exception(f"Google API rate limit exceeded. Please wait {int(delay)} seconds and try again.")
                    time.sleep(delay)
                else:
                    time.sleep(25)
            elif "503" in last_error or "UNAVAILABLE" in last_error:
                time.sleep(10)
            else:
                time.sleep(2)

    raise Exception(f"AI generation failed after {max_retries} attempts. Last error: {last_error}")


def generate_flashcards(content: str, num_cards: int = 15) -> list[dict]:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise Exception("Missing API key configuration")
        
    client = genai.Client(api_key=api_key)
    model_name = 'gemini-flash-lite-latest'
    
    prompt = f"""
    You are an academic study assistant. Generate exactly {num_cards} high-value active-recall flashcards from the supplied study material.
    Do not invent facts. Prioritize concepts that are important for exams and understanding.
    Create clear questions whose answers require recall. Avoid duplicate or trivial questions.
    Provide the source_page integer if it can be found in the text (e.g. "--- Page 1 ---"). If not, leave it null.
    
    Material:
    {content}
    """

    parsed_cards = _fetch_cards(client, model_name, prompt)
    
    unique_cards = {}
    for card_out in parsed_cards:
        q_key = card_out.question.strip().lower()
        if q_key not in unique_cards:
            unique_cards[q_key] = card_out

    # Targeted retry if too few cards
    if len(unique_cards) < 10 and len(content) > 1000:
        logger.info(f"Only got {len(unique_cards)} cards. Source is large enough. Requesting more...")
        missing_count = num_cards - len(unique_cards)
        retry_prompt = f"""
        You are an academic study assistant. I previously asked for flashcards, but you only provided {len(unique_cards)}.
        Please generate exactly {missing_count} MORE unique high-value active-recall flashcards from the material.
        Do NOT repeat any of the previous concepts.
        
        Material:
        {content}
        """
        try:
            extra_cards = _fetch_cards(client, model_name, retry_prompt)
            for card_out in extra_cards:
                q_key = card_out.question.strip().lower()
                if q_key not in unique_cards:
                    unique_cards[q_key] = card_out
        except Exception as e:
            logger.warning(f"Targeted retry failed, continuing with what we have. Error: {e}")

    final_cards = list(unique_cards.values())[:num_cards]
    
    result = []
    for item in final_cards:
        card_dict = item.model_dump()
        # Generate a deterministic unique ID based on the question
        card_dict["id"] = hashlib.md5(card_dict["question"].strip().lower().encode()).hexdigest()
        
        try:
            Flashcard(**card_dict)
            result.append(card_dict)
        except ValidationError as e:
            logger.error(f"Validation failed for a card: {e}")
            continue

    if not result:
        raise Exception("All generated cards failed validation or none were returned.")
        
    if len(result) < 10 and len(content) > 1000:
        logger.warning(f"Source material had sufficient length but model only generated {len(result)} cards.")

    logger.info(f"Successfully generated {len(result)} valid flashcards")
    return result

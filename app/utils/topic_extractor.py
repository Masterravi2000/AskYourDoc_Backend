from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def extract_topic(query: str) -> str:
    prompt = f"""
    Extract the main topic, entity, product, project, document, or subject
    that the user is asking about.

    Remove question words, instructions, and conversational words.
    Return ONLY the main topic as plain text.

    Examples:
    "What is Strength?" -> "Strength"
    "What is FishPay?" -> "FishPay"
    "Summarize FishPay" -> "FishPay"
    "Tell me about the Strength app" -> "Strength"
    "What is the purpose of FishPay?" -> "FishPay"
    "Explain the architecture of FishPay" -> "FishPay"

    USER QUERY:
    {query}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    return response.text.strip()
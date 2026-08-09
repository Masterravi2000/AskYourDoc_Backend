from google import genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def build_context(ranked_results):
    context_parts = []
    
    for index, result in  enumerate(ranked_results, start=1):
               context_parts.append(
               f"""
               SOURCE {index}
               File: {result['file_name']}
               File Type: {result['file_type']}
               Page: {result['page_number']}
               Slide: {result['slide_number']}

               Content:
               {result['content']}
               """
               )
    return "\n".join(context_parts)




def generate_answer(query: str, context: str):

    prompt = f"""
      You are NexAI, the AI assistant inside NexDoc.

      Answer the user's question using ONLY the provided document context.

      Rules:
      - Understand the user's intent semantically, not only by exact keyword matching.
      - The user may ask about a topic using different wording, such as:
      "Strength", "What is Strength?", "Tell me about Strength",
      "Summarize Strength", or "Explain the Strength app".
     - If the DOCUMENT CONTEXT contains information that is clearly relevant
     to the user's topic or question, use that information to answer.
     - You may combine relevant information from multiple context chunks/sources.
     - Do not require the user's exact words to appear in the context.
     - Do not use outside knowledge.
     - Do not invent or assume information that is not supported by the context.
     - If the context is unrelated to the user's question/topic, return:
     "I couldn't find the answer in the provided documents."
     - source_ids MUST contain only SOURCE numbers that actually support the answer.
     - If multiple sources support the answer, include all relevant sources.
     - Do not include unsupported sources.

       USER QUESTION:
       {query}

       DOCUMENT CONTEXT:
       {context}
       """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "string"
                    },
                    "source_ids": {
                        "type": "array",
                        "items": {
                            "type": "integer"
                        }
                    }
                },
                "required": ["answer", "source_ids"]
            }
        }
    )

    return json.loads(response.text)





def build_sources(ranked_results, source_ids):

    sources = []

    for source_id in source_ids:

        index = source_id - 1

        if 0 <= index < len(ranked_results):

            result = ranked_results[index]

            sources.append({
                "file_name": result["file_name"],
                "file_type": result["file_type"],
                "file_size": result["file_size"],
                "page_number": result["page_number"],
                "slide_number": result["slide_number"],
                "last_modified": result["last_modified"]
            })

    return sources





def ask_ai(query: str, ranked_results):

    if not ranked_results:
        return {
            "answer": "I couldn't find relevant information in your documents.",
            "sources": []
        }

    context = build_context(ranked_results)

    ai_result = generate_answer(query, context)

    sources = build_sources(
        ranked_results,
        ai_result["source_ids"]
    )

    return {
        "answer": ai_result["answer"],
        "sources": sources
    }
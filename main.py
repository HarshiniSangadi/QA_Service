from fastapi import FastAPI, Query
import requests

app = FastAPI(title="Aurora QA Service")

# URL for the public member messages API
MEMBER_API = "https://november7-730026606190.europe-west1.run.app/messages"

def get_member_messages():
    """
    Fetch member messages from the API.
    Returns a list of dictionaries, each representing a member.
    """
    response = requests.get(MEMBER_API)
    response.raise_for_status()
    return response.json()

def find_answer(question: str, members: list):
    """
    Simple keyword-based approach to answer questions about member data.
    Checks for member name and the type of question (trip, cars, restaurants).
    """
    q_lower = question.lower()

    for member in members:
        member_name = member.get("name", "").lower()
        if member_name and member_name in q_lower:
            if "trip" in q_lower or "travel" in q_lower:
                return member.get("trip", "Trip information not available.")
            elif "car" in q_lower or "vehicle" in q_lower:
                return str(member.get("cars", "Car information not available."))
            elif "restaurant" in q_lower or "food" in q_lower:
                fav_restaurants = member.get("favorite_restaurants", [])
                return ", ".join(fav_restaurants) if fav_restaurants else "No favorite restaurants listed."
            else:
                # fallback: return basic info
                return str(member)
    return "No matching member or information found."

@app.get("/ask")
def ask(q: str = Query(..., description="Ask a question about a member")):
    """
    Endpoint to answer a natural language question.
    """
    messages = get_member_messages()
    answer = find_answer(q, messages)
    return {"answer": answer}

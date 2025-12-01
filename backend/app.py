from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils.query_parser import parse_query
from utils.safe_responses import is_safe_query, get_safe_response
from utils.recommender import recommend_phones, compare_phones

app = FastAPI(title="Smartphone Assistant API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify your frontend URL here for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_endpoint(request: Request):
    """
    Main chat endpoint to handle user queries about smartphones.
    """
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid or empty JSON in request body."})
    user_query = data.get("query", "")

    # Safety Check 
    if not is_safe_query(user_query):
        return JSONResponse({"answer": get_safe_response(user_query)})
    
    parsed_query = parse_query(user_query)
    intent = parsed_query.get("intent")
    
     # 3️⃣ Respond based on intent
    if intent == "recommendation":
        results = recommend_phones(
            brand=parsed_query.get("brand"),
            budget=parsed_query.get("budget"),
            features=parsed_query.get("features")
        )
        return JSONResponse({
            "answer": f"Here are some phone recommendations. {results}",
        })

    elif intent == "comparison":
        comparisons = compare_phones(parsed_query.get("phones_to_compare", []))
        return JSONResponse({
            "answer": f"Here is the comparison result:\n{comparisons}"
        })


    else:
        return JSONResponse({
            "answer": "Sorry, I didn't understand that. Try asking about phone recommendations or comparisons."
        })

@app.get("/")
def root():
    return {"message": "Smartphone Assistant API is running!"}
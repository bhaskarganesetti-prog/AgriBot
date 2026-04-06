from fastapi import APIRouter
from schemas import ChatbotInput, ChatbotResponse

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@router.post("/process_query", response_model=ChatbotResponse)
def process_query(data: ChatbotInput):
    response_text = generate_response(data.query)
    return ChatbotResponse(text=response_text)


def generate_response(query: str) -> str:
    query = query.lower().strip()

    crop_info = {
        "rice": "Rice grows best in warm, humid conditions with lots of water. Ideal temperature: 20-37°C, Rainfall: 100-200cm.",
        "wheat": "Wheat prefers cool and dry weather. Ideal temperature: 15-20°C, Rainfall: 30-100cm.",
        "maize": "Maize needs warm weather and moderate rainfall. Ideal temperature: 18-27°C.",
        "sugarcane": "Sugarcane thrives in tropical climates with high rainfall. Temperature: 20-35°C.",
        "cotton": "Cotton grows in warm and dry climates. Temperature: 20-30°C, needs good sunshine.",
        "mango": "Mangoes grow well in tropical and subtropical regions with dry winters.",
        "banana": "Bananas need a warm, humid climate with regular rainfall.",
        "grapes": "Grapes prefer a warm, dry climate with cold winters to induce dormancy.",
        "apple": "Apples grow best in cool climates with cold winters.",
        "tomato": "Tomatoes need warm temperatures and well-drained soil. Ideal: 20-27°C.",
    }

    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    for greet in greetings:
        if greet in query:
            return "Hello! I am your agriculture assistant. Ask me about any crop or use the Prediction tool!"

    for crop, info in crop_info.items():
        if crop in query:
            return f"🌱 {crop.capitalize()}: {info}"

    if "predict" in query or "best crop" in query or "recommend" in query:
        return "To get a crop recommendation, please go to the Prediction screen and enter your soil and weather parameters!"

    if "soil" in query:
        return "Healthy soil is key! You should check NPK levels, pH, and moisture. The ideal pH for most crops is 6.0-7.0."

    if "fertilizer" in query:
        return "Common fertilizers include Urea (N), Superphosphate (P), and Muriate of Potash (K). Use based on soil test results."

    if "irrigation" in query or "water" in query:
        return "Irrigation method depends on the crop. Drip irrigation is best for water-saving. Flood irrigation suits paddy fields."

    if "weather" in query or "temperature" in query or "humidity" in query:
        return "Weather affects crop growth greatly. Enter your local weather data in the Prediction tool for the best crop recommendation."

    return "I'm here to help with agriculture queries! Ask me about crops, soil, fertilizers, or irrigation. You can also use the Prediction tool for AI-based crop recommendations."

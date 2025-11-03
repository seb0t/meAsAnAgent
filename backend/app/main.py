from fastapi import FastAPI
from routers import chat, health
from services.llm_google import router as models_router
from services.chatbot import router as chatbot_router
from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables
first_name = os.getenv('FIRST_NAME', 'jonh')
second_name = os.getenv('SECOND_NAME', 'Snow')
full_name = f"{first_name} {second_name}"
email = os.getenv('EMAIL', 'mail@example.com')
github_page = os.getenv('GITHUB_PAGE' , "")

app = FastAPI(
    title="AI Career Agent Backend",
    description=f"API per interrogare la knowledge base della carriera di {full_name}",
    version="0.1.0",
    contact={
        "name": full_name,
        "url": f"https://github.com/{github_page}",
        "email": email,
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(chat.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(models_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
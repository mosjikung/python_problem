from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import engine
import model
import router

# generate model to table postgresql
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://nrc-management.xcoshop.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def Home():
    return "Welcome Home"


app.include_router(router.router)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import expediente, persona


app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "API funcionando"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expediente.router)
app.include_router(expediente.router)
app.include_router(persona.router)
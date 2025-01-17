from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from search import SearchEngine

app = FastAPI()
searchEngine = SearchEngine()

# Mount static files
app.mount("/ui", StaticFiles(directory="./src/public", html=True), name="static")


@app.get("/api/")
def index(query: str):
    return searchEngine.perform_search(query)

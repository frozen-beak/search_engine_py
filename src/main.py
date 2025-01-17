from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .search import SearchEngine

app = FastAPI()
searchEngine = SearchEngine()


@app.get("/api/search")
def index(query: str):
    return searchEngine.perform_search(query)


# Mount static files
app.mount("/", StaticFiles(directory="./src/public", html=True), name="static")

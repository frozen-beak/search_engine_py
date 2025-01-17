from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from .search import SearchEngine

app = FastAPI()
searchEngine = SearchEngine()


@app.get("/api/search")
def search_query(query: str):
    return searchEngine.perform_search(query)


@app.get("/api/health")
def health_check():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "ok"},
    )


# Serve static files over default route
app.mount("/", StaticFiles(directory="./src/public", html=True), name="static")

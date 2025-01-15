from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from search import (
    compute_idf,
    read_documents,
    build_inverted_index,
    compute_tf_idf,
    search,
    decode_filename,
)
from pydantic import BaseModel
import base64

# Search Engine
documents, filenames = read_documents("./cars")
total_docs = len(documents)
inverted_index = build_inverted_index(documents)
idf = compute_idf(inverted_index, total_docs)
tf_idf_matrix = compute_tf_idf(documents, idf)

app = FastAPI()

# Mount static files
app.mount("/ui", StaticFiles(directory="./src/public", html=True), name="static")

class CarResult(BaseModel):
    name: str
    link: str
    desc: str
    engine: str
    weight: str
    power: str
    zero_to_sixty: str
    torque: str
    top_speed: str
    score: float

def decode_filename(encoded_filename):
    encoded_str = encoded_filename.split("'")[1]
    decoded_bytes = base64.b64decode(encoded_str)
    link = decoded_bytes.decode("utf-8")
    return link

def extract_car_name(link):
    path = link.strip('/').split('/')[-1]
    camel_case_parts = [part.capitalize() if not part.isdigit() else part for part in path.split('-')]
    name = ' '.join(camel_case_parts)
    return name

def split_document(doc_text):
    parts = doc_text.split('\n\n', 1)

    desc = parts[0] if len(parts) >= 1 else ''
    specs = parts[1] if len(parts) >= 2 else ''

    return desc, specs

def parse_specifications(specs_text):
    spec_dict = {}
    lines = specs_text.strip().split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            spec_dict[key] = value
    return spec_dict

@app.get("/")
def index(query:str):
    results = search(query, documents, idf, tf_idf_matrix, top_n=5)
    
    final_results = []
    for idx, score in results:
        filename = filenames[idx]
        link = decode_filename(filename)
        doc_text = documents[idx]
        
        name = extract_car_name(link)
        desc, specs = split_document(doc_text)
        spec_dict = parse_specifications(specs)
        
        result = CarResult(
            name=name,
            link=link,
            desc=desc,
            engine=spec_dict.get("engine", ""),
            weight=spec_dict.get("weight", ""),
            power=spec_dict.get("power", ""),
            zero_to_sixty=spec_dict.get("0-62", ""),
            torque=spec_dict.get("torque", ""),
            top_speed=spec_dict.get("top speed", ""),
            score=score
        )
        
        final_results.append(result)
    
    return final_results

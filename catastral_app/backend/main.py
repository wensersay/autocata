from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
from pdf_processor import extract_cadastral_data
from doc_generator import generar_docx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/procesar")
def procesar_pdf(file: UploadFile = File(...)):
    contents = file.file.read()
    data = extract_cadastral_data(contents)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        output_path = generar_docx(data, tmp.name)
    return FileResponse(output_path, filename="certificacion_generada.docx")

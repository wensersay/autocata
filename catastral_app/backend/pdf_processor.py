from typing import Dict, List
import fitz  # PyMuPDF
import re

def extract_cadastral_data(pdf_bytes: bytes) -> Dict:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    full_text = re.sub(r'[\n\r]+', ' ', full_text)
    full_text = re.sub(r'\s{2,}', ' ', full_text)
    data = {
        "referencia_catastral": re.search(r"Referencia catastral:?\s*([A-Z0-9]{20})", full_text),
        "direccion": re.search(r"(LG|CL|RU|BO|AV)\s+[^,\d]+[\d\[\]A-Za-z,\s]*PORRIÑO.*?PONTEVEDRA", full_text),
        "superficie_m2": re.search(r"Superficie gráfica[:\s]+(\d+[\.,]?\d*)\s*m2", full_text),
        "valor_catastral": re.search(r"Valor catastral[^\d]*(\d+[.,]\d{2})\s*\u20ac?", full_text),
        "titulares": re.findall(r"([A-Z ]+\s[A-Z]+)\s+(\d{8}[A-Z])\s+(\d{1,3},\d{2})%", full_text),
    }
    if data["referencia_catastral"]:
        data["referencia_catastral"] = data["referencia_catastral"].group(1)
    if data["direccion"]:
        data["direccion"] = data["direccion"].group(0)
    if data["superficie_m2"]:
        data["superficie_m2"] = float(data["superficie_m2"].group(1).replace(',', '.'))
    if data["valor_catastral"]:
        data["valor_catastral"] = float(data["valor_catastral"].group(1).replace(',', '.'))
    if data["titulares"]:
        data["titulares"] = [
            {"nombre": t[0].title(), "nif": t[1], "porcentaje": float(t[2].replace(',', '.'))}
            for t in data["titulares"]
        ]
    return data

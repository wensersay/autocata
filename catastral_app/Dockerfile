FROM python:3.11-slim
WORKDIR /app
COPY backend/ ./
RUN pip install --no-cache-dir fastapi uvicorn python-docx pymupdf
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Auth Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy backend code + frontend
COPY auth.py requirements.txt index.html /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "auth.py"]

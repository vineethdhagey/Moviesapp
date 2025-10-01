# Add Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy backend code (frontend is not needed here if served by auth)
COPY add.py requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "add.py"]

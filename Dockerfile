
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/project/src/backend

WORKDIR /project

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application and database folder
COPY src/backend /app/
COPY src/frontend /frontend/
COPY database/ ./database/

EXPOSE 5000

# Start the Flask application
CMD ["python", "-m", "flask", "--app", "app", "run", "--host=0.0.0.0", "--port=5000"]

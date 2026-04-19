FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x setup_git.sh && ./setup_git.sh

ENV PORT=5021

EXPOSE 5021

CMD ["sh", "-c", "python app.py"]

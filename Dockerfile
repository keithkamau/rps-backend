FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create startup script
RUN echo '#!/bin/bash\npython3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"\ngunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 run:app' > /app/start.sh && chmod +x /app/start.sh

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["/app/start.sh"]

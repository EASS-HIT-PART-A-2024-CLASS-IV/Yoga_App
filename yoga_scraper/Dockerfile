FROM python:3.13.0a3-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

RUN pip install selenium
RUN pip install bs4

COPY scrape_yoga_classes.py /app/scrape_yoga_classes.py

CMD ["python", "/app/scrape_yoga_classes.py"]
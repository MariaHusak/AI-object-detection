FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir git+https://github.com/facebookresearch/sam2.git

COPY segment-anything-2/sam2/configs /usr/local/lib/python3.11/site-packages/sam2/configs
COPY segment-anything-2/sam2/configs/sam2.1 /usr/local/lib/python3.11/site-packages/sam2/sam2.1

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.13

WORKDIR /app

# Copy dependencies first
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Create uploads folder (important!)
RUN mkdir -p uploads

EXPOSE 5000

CMD ["python", "app.py"]
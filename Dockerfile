FROM python:3.8.0-alpine3.10
RUN apk add --no-cache git
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "start.py"]

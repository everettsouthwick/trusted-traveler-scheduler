FROM python:alpine

WORKDIR /app

# Needed for python to show logs in all processes
ENV PYTHONUNBUFFERED 1

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "ttp.py"]

FROM python:3.11-slim

WORKDIR /app

RUN pip install pwntools

COPY server/intel_server.py /app/intel_server.py

EXPOSE 31337

CMD ["python", "/app/intel_server.py"]

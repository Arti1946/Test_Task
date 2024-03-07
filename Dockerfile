FROM python:3.12
LABEL author="Arch"
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY --chmod=0755 entrypoint.sh /usr/local/bin/
COPY . .
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["uvicorn main:app --reload --port 8000"]
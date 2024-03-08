FROM python:3.12
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY --chmod=0755 entrypoint.sh /usr/local/bin/
COPY . .
ENTRYPOINT ["sh", "/usr/local/bin/entrypoint.sh"]
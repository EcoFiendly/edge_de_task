FROM python:3.10
WORKDIR /etl
ADD requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "code/main.py"]
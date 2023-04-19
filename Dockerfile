FROM python:3.11.3-slim-buster

ENV FLASK_APP="main.py"

WORKDIR /fuelpricehunter

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]

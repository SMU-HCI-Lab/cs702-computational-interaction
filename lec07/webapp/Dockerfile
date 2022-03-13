FROM python:3.6.5-slim

WORKDIR /app
ADD . /app

COPY requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
EXPOSE 80

CMD ["python", "main.py"]

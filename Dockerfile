FROM python:3.8-buster

WORKDIR /usr/src/app
RUN mkdir /usr/src/app/files

RUN apt-get update
RUN apt-get install poppler-utils -y
RUN apt-get install tesseract-ocr -y
RUN apt-get install tesseract-ocr-por -y

COPY requirements.txt ./
RUN pip3 install numpy opencv-python-headless gunicorn
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "server:app" ]

FROM python:3.8-buster

WORKDIR /usr/src/app
RUN mkdir /usr/src/app/files

RUN apt-get update
RUN apt-get install poppler-utils -y
RUN apt-get install tesseract-ocr -y
RUN apt-get install tesseract-ocr-por -y

COPY requirements.txt ./
RUN pip3 install numpy opencv-python-headless
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./server.py" ]

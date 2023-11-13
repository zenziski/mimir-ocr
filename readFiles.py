from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os
import re
import json
import cv2
import numpy as np

def preprocess_image(imagePath):
    img = cv2.imread(imagePath)

    # converte para esquema de cores HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # range de vermelho
    lowerRed = np.array([0, 70, 50])
    upperRed = np.array([10, 255, 255])

    # aplica a mascara para pegar somente partes vermelhas
    maskRed = cv2.inRange(hsv, lowerRed, upperRed)

    # aplica bitwise para pegar somente partes vermelhas
    redOnly = cv2.bitwise_and(img, img, mask=maskRed)

    # inverte a mascara para pegar outras partes que nao sao vermelhas
    maskNonRed = cv2.bitwise_not(maskRed)

    # aplica bitwise para pegar somente partes que nao sao vermelhas
    nonRedOnly = cv2.bitwise_and(img, img, mask=maskNonRed)

    # converte as duas imagens em escalas de cinza
    grayRed = cv2.cvtColor(redOnly, cv2.COLOR_BGR2GRAY)
    grayNonRed = cv2.cvtColor(nonRedOnly, cv2.COLOR_BGR2GRAY)

    # trata imagem para remover ruidos
    kernel = np.ones((1, 1), np.uint8)
    imgRed = cv2.dilate(grayRed, kernel, iterations=1)
    imgRed = cv2.erode(imgRed, kernel, iterations=1)
    imgNonRed = cv2.dilate(grayNonRed, kernel, iterations=1)
    imgNonRed = cv2.erode(imgNonRed, kernel, iterations=1)

    # aplica threshold adaptativo para binarizar as imagens
    imgRed = cv2.adaptiveThreshold(imgRed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    imgNonRed = cv2.adaptiveThreshold(imgNonRed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    
    # combinando as duas imagens
    combinedImg = cv2.bitwise_or(imgRed, imgNonRed)

    cv2.imwrite(imagePath, combinedImg)

def main(path):
    returnData = []
    data = []
    for file in os.scandir(path):
        inputFilepath = path + "/" + file.name
        print(file.name, flush=True)
        text = ''
        if (file.name.endswith('.pdf')): #é um arquivo pdf
            text = extract_text(inputFilepath)
            #não é um arquivo que contem um texto selecionalvel, entao transforma em imagem e usa o tesseract
            if (len(str(text)) < 50):
                text = ''
                images = convert_from_path(inputFilepath, dpi=400)
                for i in range(len(images)):
                    imageFilepath = "./page"+ str(i) +".jpg"
                    images[i].save(imageFilepath, "JPEG")
                    text = text + pytesseract.image_to_string(Image.open(imageFilepath), lang="por")
                    os.remove(imageFilepath)
        elif (file.name.endswith('.jpg') or file.name.endswith('.png')): #é uma imagem
            text = pytesseract.image_to_string(Image.open(inputFilepath), lang="por")
        
        data = getData(text)
        returnData.append({"filename": file.name, "cnpj": data[0], "cpf": data[1], "rg": data[2], "date": data[3]})
    return returnData

#Função que retorna os dados extraidos conforme arquivo de regex
def getData(text):
    print(text, flush=True)
    f = open('regex.json')
    regexes = json.load(f)
    
    #1. CNPJ
    cnpj = None
    cpf = None
    date = None
    rg = None
    regex = regexes["cnpj"]
    results = re.findall(regex, text)
    if (len(results) > 0):
        cnpj = results[0]
        cnpj = "".join(e for e in cnpj if e.isalnum())
    regex = regexes["cpf"]
    results = re.findall(regex, text)
    if (len(results) > 0):
        cpf = results[0]
        cpf = "".join(e for e in cpf if e.isalnum())
    regex = regexes["data"]
    results = re.findall(regex, text)
    if (len(results) > 0):
        date = results[0]
    regex = regexes["rg"]
    results = re.findall(regex, text)
    if (len(results) > 0):
        rg = results[0]

    return cnpj, cpf, rg, date

from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os
import re
import json
import cv2
import numpy as np

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    # converte para esquema de cores HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # range de vermelho
    lower_red = np.array([0, 70, 50])
    upper_red = np.array([10, 255, 255])
    # aplica a mascara para pegar somente partes vermelhas
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    # aplica bitwise para pegar somente partes vermelhas
    red_only = cv2.bitwise_and(img, img, mask=mask_red)
    # inverte a mascara para pegar outras partes que nao sao vermelhas
    mask_non_red = cv2.bitwise_not(mask_red)
    # aplica bitwise para pegar somente partes que nao sao vermelhas
    non_red_only = cv2.bitwise_and(img, img, mask=mask_non_red)
    # converte as duas imagens em escalas de cinza
    gray_red = cv2.cvtColor(red_only, cv2.COLOR_BGR2GRAY)
    gray_non_red = cv2.cvtColor(non_red_only, cv2.COLOR_BGR2GRAY)
    # trata imagem para remover ruidos
    kernel = np.ones((1, 1), np.uint8)
    img_red = cv2.dilate(gray_red, kernel, iterations=1)
    img_red = cv2.erode(img_red, kernel, iterations=1)
    img_non_red = cv2.dilate(gray_non_red, kernel, iterations=1)
    img_non_red = cv2.erode(img_non_red, kernel, iterations=1)
    # aplica threshold adaptativo para binarizar as imagens
    img_red = cv2.adaptiveThreshold(img_red, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    img_non_red = cv2.adaptiveThreshold(img_non_red, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    # combinando as duas imagens
    combined_img = cv2.bitwise_or(img_red, img_non_red)

    cv2.imwrite(image_path, combined_img)

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
        
        data = getData(text, file.name)
        returnData.append({"filename": file.name, "cnpj": data[0], "cpf": data[1], "rg": data[2], "date": data[3]})
    return returnData

#Função que retorna os dados extraidos conforme arquivo de regex
def getData(text, filename):
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

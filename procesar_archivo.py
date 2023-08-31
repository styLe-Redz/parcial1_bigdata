import boto3
from datetime import datetime
from bs4 import BeautifulSoup


def f():
    nombre = str(datetime.today().strftime('%Y-%m-%d'))
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('parcial1lectura')
    obj_tiempo = bucket.Object(str("news/raw/" +
                                   "eltiempo-" + nombre +
                                   ".html"))
    body_tiempo = obj_tiempo.get()['Body'].read()
    obj_publimetro = bucket.Object(str("news/raw/" +
                                       "publimetro-" + nombre +
                                       ".html"))
    body_publimetro = obj_publimetro.get()['Body'].read()
    html_tiempo = BeautifulSoup(body_tiempo, 'html.parser')
    html_publimetro = BeautifulSoup(body_publimetro, 'html.parser')
    data_noticias_tiempo = html_tiempo.find_all('article')
    data_noticias_publimetro = html_publimetro.find_all('article')
    csv_tiempo = ""
    csv_publimetro = ""
    linea_0 = "Nombre, Categoria, Link\n"
    for i in range(len(data_noticias_tiempo)):
        link = "eltiempo.com" + \
               data_noticias_tiempo[i].find('a',
                                            class_='title page-link')['href']
        name = data_noticias_tiempo[i]['data-name'].replace(",", "")
        category = data_noticias_tiempo[i]['data-seccion']
        csv_tiempo += linea_0 + name + "," + \
            category + "," + \
            link + \
            "\n"
    for i in range(len(data_noticias_publimetro)):
        link = "publimetro.co" + data_noticias_publimetro[i].find('a')['href']
        name = (data_noticias_publimetro[i].find('a').text).replace(",", "")
        category = link.split('/')[1]
        csv_publimetro += linea_0 + name + "," + \
            category + "," + \
            link + \
            "\n"
    boto3.client('s3').put_object(Body=csv_tiempo,
                                  Bucket='parcial1lectura',
                                  Key=str('headlines/final' +
                                          '/periodico=eltiempo/year=' +
                                          nombre[:4]+'/month=' +
                                          nombre[5:7]+'/day=' +
                                          nombre[8:]+'/eltiempo.csv'))
    boto3.client('s3').put_object(Body=csv_publimetro,
                                  Bucket='parcial1lectura',
                                  Key=str('headlines/final' +
                                          '/periodico=publimetro/year=' +
                                          nombre[:4]+'/month=' +
                                          nombre[5:7]+'/day=' +
                                          nombre[8:]+'/publimetro.csv'))

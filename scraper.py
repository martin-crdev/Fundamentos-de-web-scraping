import requests 
import lxml.html as html
import os
import datetime

#Variables globales que contienen las sentencias xpath 
HOME_URL = 'https://www.larepublica.co/'

XPATH_lINK_TO_ARTICLE = '//text-fill/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode("utf-8")
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


#Funcion que obtendra los links de las noticias
def parse_home():
    #Verificamos que no nos marque error al intentar comunicarnos con la web
    try:
        response = requests.get(HOME_URL) #Variable que guarda la pagina en html
        if response.status_code == 200: #Verificamos el estado del html
            home = response.content.decode("utf-8") #Convertimos caracteres especiales
            parsed = html.fromstring(home) #Convertimos de html a un archivo que nos permite usar xpath
            links_to_notices = parsed.xpath(XPATH_lINK_TO_ARTICLE) #Guardamos en una lista los links
            print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == "__main__":
    run()
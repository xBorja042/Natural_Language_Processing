import requests
from bs4 import BeautifulSoup
import tqdm
import sys

try:
	section = sys.argv[1]
	back = int(sys.argv[2])
except:
	section, back = False, False

if section:
	print(f"Scaning section {section} and a total of {back} pages")
else: section = 'mercados'

if back:
	print(f"Scaning a total of {back} pages")
else: back  = 30



url_original = 'https://cincodias.elpais.com/seccion/' + section
r = requests.get(url_original)
soup = BeautifulSoup(r.content, 'html.parser')
sopa = soup.findAll('h2', attrs ={'class': 'articulo-titulo'})
prefix = 'https://cincodias.elpais.com/'
links = [prefix + link.a['href'][1:] for link in sopa]

out_filename = section + '_out.txt'

with open(out_filename, 'w') as out_file:
    for url in tqdm.tqdm(links):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        articulo = ''
        for element in soup.find(id='cuerpo_noticia').find_all('p'):
            articulo += element.getText()
        articulo = articulo.replace('\n', '')
        out_file.write(articulo.lower())
        out_file.write("| ")
		
		
print(" Scaning rest of the pages backwards")
r = requests.get(url_original)
soup = BeautifulSoup(r.content, 'html.parser')
s_limit = soup.findAll('li', attrs ={'class': 'paginacion-siguiente activo'})[0]
limit = int(s_limit.findAll('a')[0].get('href')[-4:])


limit_f = limit - back



for i in range(limit, limit_f, -1):
    new_url = 'https://cincodias.elpais.com/seccion/mercados/' + str(i)    
    r = requests.get(new_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    sopa = soup.findAll('h2', attrs ={'class': 'articulo-titulo'})
    prefix = 'https://cincodias.elpais.com/'
    links = [prefix + link.a['href'][1:] for link in sopa]
    print(f" New URL to parse {new_url} with {len(links)} newspaper articles")
    with open(out_filename, 'a+') as out_file:
        for url in tqdm.tqdm(links):
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            articulo = ''
            for element in soup.find(id='cuerpo_noticia').find_all('p'):
                articulo += element.getText()
            articulo = articulo.replace('\n', '')
            out_file.write(articulo.lower())
            out_file.write("\n")
import os
from urllib.parse import quote
import urllib.request
import requests

from bs4 import BeautifulSoup
from sanic import Sanic
from sanic import response

app = Sanic("Professors")
S = requests.Session()

google_base_link = 'https://www.google.com/search?q=%s+%s&ie=UTF-8'
scholar_base_link = 'https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=%s+%s'
university_logo_base_link = 'https://www.google.com/search?q=university+%s+logo+wikipedia&sclient=img&tbm=isch'

base_row = '''<tr>
    <td>%s &nbsp; &nbsp;</td>
    <td><a target="_blank" href="%s">auto</a>&nbsp; &nbsp;</td>
    <td><a target="_blank" href="%s">scholar</a>&nbsp; &nbsp;</td>
    <td><a target="_blank" href="%s">search</a></td>
</tr>'''


@app.route("/")
async def root(request):

    universities = [university.replace('.txt', '').strip() for university in os.listdir('lists/')]
    items = list()
    for university in universities:
        uni_logo_page = S.get(university_logo_base_link % university)
        soup = BeautifulSoup(uni_logo_page.text, 'html.parser')
        uni_logo = soup.find_all('img')[1].attrs['src']

        img_tag = '<img src=%s>' % uni_logo
        a_tag = '<a href="%s">%s</a><br>' % (quote(university), university)
        items.append(img_tag + '&nbsp;' + a_tag)

    # items = [ for university in universities]
    return response.html('<html><body><h3>Universities</h3>\n%s</body></html>' % '\n'.join(items))


@app.route("/favicon.ico")
async def favicon(request):
    return response.empty()


@app.route("/<university>")
async def list_professors(request, university):
    items = list()
    professors = set()
    with open('lists/%s.txt' % university, 'r') as f:
        for i, line in enumerate(f):
            name = line.strip()
            if not name:
                items.append('</table><hr><table>')
                continue
            if name in professors or name.startswith('#'):
                continue
            professors.add(name)
            name_quoted = quote(name)
            university_quoted = quote(university)
            auto = '%s/%s' % (university_quoted, name_quoted)
            row = base_row % (name, auto, scholar_base_link % (name_quoted, university_quoted), google_base_link % (name_quoted, university_quoted))
            items.append(row)
    return response.html('<html><body><h3>%s</h3>\n<table>%s</table></body></html>' % (university, '\n'.join(items)))


@app.route("/<university>/<name>")
async def redirect_to_prof_page(request, university, name):
    university_quoted, name_quoted = quote(university), quote(name)
    scholar = scholar_base_link % (name_quoted, university_quoted)
    # html_page = urllib.request.urlopen(scholar)
    html_page = S.get(scholar)
    soup = BeautifulSoup(html_page.text)
    links = soup.select('a.gs_ai_pho')
    if len(links) == 0:
        google = google_base_link % (name_quoted, university_quoted)
        return response.redirect(google)
    elif len(links) > 1:
        return response.redirect(scholar)
    else:
        return response.redirect('https://scholar.google.com%s&view_op=list_works&sortby=pubdate' % links[0].get('href'))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, auto_reload=True)


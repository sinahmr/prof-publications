import os
from time import sleep
from urllib.parse import quote
import urllib.request

from bs4 import BeautifulSoup
from sanic import Sanic
from sanic import response

app = Sanic("Professors")

google_base_link = 'https://www.google.com/search?q=%s+%s&ie=UTF-8'
scholar_base_link = 'https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=%s+%s'
base_row = '''<tr>
    <td>%s &nbsp; &nbsp;</td>
    <td><a target="_blank" href="%s">auto</a>&nbsp; &nbsp;</td>
    <td><a target="_blank" href="%s">scholar</a>&nbsp; &nbsp;</td>
    <td><a target="_blank" href="%s">search</a></td>
</tr>'''


@app.route("/")
async def root(request):
    universities = [university.replace('.txt', '').strip() for university in os.listdir('lists/')]
    items = ['<a href="%s">%s</a><br>' % (quote(university), university) for university in universities]
    return response.html('<html><body><h3>Universities</h3>\n%s</body></html>' % '\n'.join(items))


@app.route("/favicon.ico")
async def favicon(request):
    return response.empty()


@app.route("/<university>")
async def list_professors(request, university):
    generate_all = request.args.get('generateall', '').lower() == 'true'
    items = list()
    professors = set()
    with open('lists/%s.txt' % university, 'r') as f:
        for i, line in enumerate(f):
            name = line.strip()
            if not name:
                items.append('</table><hr><table>')
                continue
            elif name.startswith('#'):
                items.append('<b>%s</b>' % name[1:])
            if name in professors or name.startswith('#'):
                continue
            professors.add(name)
            name_quoted = quote(name)
            university_quoted = quote(university)
            if generate_all:
                auto = await find_auto_value(university, name)
                if i % 10 == 9:
                    sleep(5)
            else:
                auto = '%s/%s' % (university_quoted, name_quoted)
            row = base_row % (name, auto, scholar_base_link % (name_quoted, university_quoted), google_base_link % (name_quoted, university_quoted))
            items.append(row)
    return response.html('<html><body><h3>%s</h3>\n<table>%s</table></body></html>' % (university, '\n'.join(items)))


@app.route("/<university>/<name>")
async def redirect_to_prof_page(request, university, name):
    return response.redirect(await find_auto_value(university, name))


async def find_auto_value(university, name):
    university_quoted, name_quoted = quote(university), quote(name)
    scholar = scholar_base_link % (name_quoted, university_quoted)
    html_page = urllib.request.urlopen(scholar)
    soup = BeautifulSoup(html_page, 'html.parser')
    links = soup.select('a.gs_ai_pho')
    if len(links) == 0:
        redirect = google_base_link % (name_quoted, university_quoted)
    elif len(links) > 1:
        redirect = scholar
    else:
        redirect = 'https://scholar.google.com%s&view_op=list_works&sortby=pubdate' % links[0].get('href')
    return redirect


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, auto_reload=True)

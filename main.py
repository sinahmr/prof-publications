import os
from urllib.parse import quote
import urllib.request
import requests

from bs4 import BeautifulSoup
from sanic import Sanic
from sanic import response

import utils

app = Sanic("Professors")
app.static('/styles', './styles')

google_base_link = 'https://www.google.com/search?q=%s+%s&ie=UTF-8'
scholar_base_link = 'https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=%s+%s'
prof_auto_profile_pic = 'https://www.google.com/search?q=%s+university+%s+profile&sclient=img&tbm=isch'

Sess = requests.Session()

@app.route("/")
async def root(request):
    universities = [university.replace('.txt', '').strip() for university in os.listdir('lists/')]
    items = list()
    for university in universities:
        uni_logo = utils.get_university_logo(Sess, university)
        logo_tag = utils.make_img_tag(uni_logo, (100, 100), classes="w3-margin w3-padding-left w3-padding-right")
        href_tag = utils.make_link_tag(quote(university), utils.titlify(university))
        items.append({
            'logo': logo_tag,
            'href': href_tag
        })

    uni_list = utils.tabelify_universities(items)
    return response.html(utils.htmlify("Universities", "Universities", uni_list))

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
                items.append({'break':True}) # </table><hr><table>
                continue
            if name in professors or name.startswith('#'):
                continue
            professors.add(name)

            name = utils.titlify(name)
            professor_pic_page = Sess.get(prof_auto_profile_pic % (name, university))
            soup = BeautifulSoup(professor_pic_page.text, 'html.parser')
            professor_pic = soup.find_all('img')[1].attrs['src']
            img_tag = utils.make_img_tag(professor_pic, (100, 120), "w3-round")
            name_quoted = quote(name)
            university_quoted = quote(university)
            auto = "%s/%s" % (university_quoted, name_quoted)
            # row = base_row % (name, auto, img_tag, scholar_base_link % (name_quoted, university_quoted), google_base_link % (name_quoted, university_quoted))
            # items.append(row)

            # content = "<table>%s</table>" % '\n'.join(items)

            items.append({
                'break': False,
                'photo': img_tag,
                'name': name,
                'auto': auto,
                'scholar': scholar_base_link % (name_quoted, university_quoted),
                'search': google_base_link % (name_quoted, university_quoted)
            })

        content = utils.professors_info(items)

    uni_logo = utils.get_university_logo(Sess, university)
    logo_tag = utils.make_img_tag(uni_logo, (70, 70), classes="w3-margin-right w3-padding-right")
    heading = logo_tag + utils.titlify(university)
    heading = utils.make_link_tag(quote("/"), heading, "w3-text-red")
    header = utils.titlify(university)
    return response.html(utils.htmlify(header, heading, content))


@app.route("/<university>/<name>")
async def redirect_to_prof_page(request, university, name):
    university_quoted, name_quoted = quote(university), quote(name)
    scholar = scholar_base_link % (name_quoted, university_quoted)

    html_page = Sess.get(scholar)
    soup = BeautifulSoup(html_page.text, 'html.parser')
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

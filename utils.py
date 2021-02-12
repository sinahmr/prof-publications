from bs4 import BeautifulSoup

def titlify(title:str)->str():
    """Capitalize first letters of every word in title except conjunction letters
       E.g., titlify('welcome to the new world') ==> 'Welcome to the New World'
    Arguments:
        title: A string representing your desired title
    Returns:
        A string: The titlified version of the input string
    """
    prepositions = ["and", "or", "the", "a", "of", "in", "at", "is", "to"]
    return "".join(["%s "%word.lower()
            if word in prepositions
            else "%s "%word.capitalize()
            for word in str(title).lower().split()])[:-1]

styles = ['<link rel="stylesheet" href="styles/w3.css">',
          '<link rel="stylesheet" href="styles/style.css">',]

def htmlify(head_title:str, heading:str, content:str)->str():
    """
    """
    head_tag = f"<head><title>%s</title>{''.join(styles)}</head>" % head_title
    header = '<header class="w3-bar w3-card"><h2>%s</h2></header>' % heading
    html = f'''
        <!doctype html>
        <html>%s
        <body>%s
        <div class="content">%s</div></body>
        %s
        </html>''' % (head_tag, header, content, make_footer())

    return html

def make_footer()->str():
    """Creates a simple footer content"""
    return '''<footer class=" w3-footer">
        Professors\' Publications Finder,  2021
        <a class="w3-text-red w3-right" href="https://github.com/nrasadi/prof-publications">Github</a>
        </footer>'''

def make_img_tag(img:str, size:(int, int)=(50, 50), classes:str='img')->str():
    """
    """
    img_tag = f'''<img src=%s width="{size[0]}" height="{size[1]}" class={classes}>''' % img
    return img_tag.strip()

def make_link_tag(link:str, title:str, classes:str='link')->str():
    """
    """
    href = '<a href="%s" classes="%s">%s</a>\n' % (link, classes, title)
    return href

def get_university_logo(Sess, university_name:str)->str():
    university_logo_base_link = 'https://www.google.com/search?q=university+%s+logo+wikipedia&sclient=img&tbm=isch'
    uni_logo_page = Sess.get(university_logo_base_link % university_name)
    soup = BeautifulSoup(uni_logo_page.text, 'html.parser')
    return soup.find_all('img')[1].attrs['src']

def professors_info(professors:list)->str():
    begin_row = '<div class="w3-container w3-row-padding ">'
    card = '''<div class="w3-third w3-center w3-container w3-margin-top ">
            %s <br>%s <br>
            <a target="_blank" href="%s">Auto</a>&nbsp;
            <a target="_blank" href="%s">Scholar</a>&nbsp;
            <a target="_blank" href="%s">Search</a>&nbsp;
            </div>'''
    grid = begin_row
    idx = 1
    for i, prof in enumerate(professors):
        if prof['break']:
            grid += ' </div><hr><div class="w3-container w3-row-padding">'
            idx = 1
            continue

        grid += card % (prof['photo'], prof['name'], prof['auto'], prof['scholar'], prof['search'])

        if i == len(professors) - 1:
            grid += '</div>'
        elif idx % 3 == 0:
            grid += ' </div>%s' % begin_row

        idx += 1

    return BeautifulSoup(grid, 'html.parser')

def tabelify_universities(universities:list)->str():
    grid = '<table class="w3-table w3-bordered w3-large">'
    base_row = '<tr class=""><th>%s %s</th></tr>'
    for uni in universities:
        grid += base_row % (uni['logo'], uni['href'])
    return grid

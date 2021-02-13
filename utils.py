from bs4 import BeautifulSoup


def titlify(title: str) -> str():
    """Capitalize first letters of every word in title except conjunction letters
       E.g., titlify('welcome to the new world') ==> 'Welcome to the New World'
    Arguments:
        title: A string representing your desired title
    Returns:
        A string: The titlified version of the input string
    """
    prepositions = ["and", "or", "the", "a", "of", "in", "at", "is", "to"]
    return "".join(["%s " % word.lower()
                    if word in prepositions
                    else "%s " % word.capitalize()
                    for word in str(title).lower().split()])[:-1]


styles = ['<link rel="stylesheet" href="styles/w3.css">',
          '<link rel="stylesheet" href="styles/style.css">', ]


def htmlify(head_title: str, heading: str, content: str) -> str():
    """ Creates html, head, content, and footer tags.
    Arguments:
        head_title: used in <head> tag as the title of the page
        heading: heading title to be shown on the top navigation bar
        content: the content of the page
    Returns: an string representing a generated html page
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


def make_footer(title: str = None, year='2021', git_repo='https://github.com/sinahmr/prof-publications') -> str():
    """Creates a simple footer content
    Arguments:
        title: a title for the footer. (default: Professors\'s Publications Finder)
        year: the latest date (only year) that scripts in the repository are modified. (e.g., 2021)
        git_repo: a url link to the reference git repository
    Returns: an string containing the footer tag and its inner content.
    """
    title = "Professors\' Publications Finder" if not title else title
    git_repo = f'<a target="_blank" class="w3-text-red w3-right" href={git_repo}>Github</a>' if git_repo else ""
    return f'''<footer class=" w3-footer">
            {title}, {year}
            {git_repo}
            </footer>'''


def make_img_tag(img: str, size: (int, int) = (50, 50), classes: str = 'img') -> str():
    """ Creates img tag.
    Arguments:
        img: source url of the image
        size: a tuple corresponding to the image height and width. e.g., (50, 50)
        classes: css classes to be applied on the img tag
    Returns: an img tag string.
    """
    img_tag = f'''<img src=%s width="{size[0]}" height="{size[1]}" class={classes}>''' % img
    return img_tag.strip()


def make_link_tag(link: str, title: str, classes: str = 'link') -> str():
    """Creates a tag.
    Arguments:
        link: href url of the <a> tag
        title: the link title
        classes: css classes to be applied on the a tag
    Returns: an <a> tag string.
    """
    href = '<a href="%s" classes="%s">%s</a>\n' % (link, classes, title)
    return href


def get_university_logo(Sess, university_name: str) -> str():
    """ Taking a request session and a university name, it finds an image url representing the university logo.
    Arguments:
        Sess: an instance of requests.Session()
        university_name: an string containing the name of the desired school
    Returns: logo url string
    """

    university_logo_base_link = 'https://www.google.com/search?q=university+%s+logo+wikipedia&sclient=img&tbm=isch'
    uni_logo_page = Sess.get(university_logo_base_link % university_name)
    soup = BeautifulSoup(uni_logo_page.text, 'html.parser')
    return soup.find_all('img')[1].attrs['src']


def professors_info(professors: list) -> str():
    """Generates university professor's page content
    Arguments:
        professors: a list of professors. each element is a dictionary with the following keys:
            - 'photo': (str) professor's profile picture
            - 'name': (str) professor's name
            - 'auto': (str) the a tag link to be inserted in the Auto section
            - 'scholar': (str) the a tag link to be inserted in the Scholar section
            - 'search': (str) the a tag link to be inserted in the Search section
            - 'break': (boolean) determines whether to insert a horizontal rule (breaking the last row) or not.
    Returns: the page content string
    """
    begin_row = '<div class="w3-container w3-row-padding ">'
    card = '''<div class="w3-quarter w3-center w3-container w3-margin-top ">
            %s <br>%s <br>
            <a target="_blank" href="%s">Auto</a>&nbsp;|&nbsp;
            <a target="_blank" href="%s">Scholar</a>&nbsp;|&nbsp;
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
        elif idx % 4 == 0:
            grid += ' </div>%s' % begin_row

        idx += 1

    return BeautifulSoup(grid, 'html.parser')


def tablify_universities(universities: list) -> str():
    """Create a table list from universities
    Arguments:
        universities: a list of universities. Each element is a dictionary with the following keys:
            - 'logo': (str) an img tag string corresponding to the university's logo
            - 'href': (str) an a tag string corresponding referring to the university's professors page
    Returns: the tablified string
    """
    grid = '<table class="w3-table w3-bordered w3-large">'
    base_row = '<tr class=""><th>%s %s</th></tr>'
    for uni in universities:
        grid += base_row % (uni['logo'], uni['href'])
    return grid

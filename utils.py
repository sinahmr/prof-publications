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

styles = '<link rel="stylesheet" href="./styles/w3.css">'

def htmlify(header_title:str, content:str)->str():
    """
    """
    head_tag = f"<head><title>%s</title>{styles}</head>" % header_title
    heading = "<h2>%s</h2>" % header_title
    header = '<header class="w3-bar w3-blue">%s</header>' % heading
    html = f'''
        <!doctype html>
        <html>%s
        <body>%s
        %s</body>
        </html>''' % (head_tag, header, content)

    return html

def make_img_tag(img:str, size:(int, int)=(50, 50))->str():
    """
    """
    img_tag = '''
        <img src=%s
        width="50px" height="50px"
        style="vertical-align:middle;margin: 1em .5em 1em .5em">
    ''' % img
    return img_tag

def make_link_tag(link:str, title:str)->str():
    """
    """
    href = '<a href="%s">%s</a>\n' % (link, title)
    return href

from lxml import etree
import os

def handle_uploaded_file(f):  
    with open('log/upload/temp.xml', 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)
    tree = etree.parse('log/upload/temp.xml')
    root = tree.getroot()
    title = root[0][0].text

    os.rename('log/upload/temp.xml', 'log/upload/{}.xml'.format(title))
    return title
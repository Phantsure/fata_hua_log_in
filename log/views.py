from django.shortcuts import render
from django.http import request, HttpResponse
from lxml import etree
import xml.etree.ElementTree as xml

from .forms import BlogForm
from .functions import handle_uploaded_file
from .models import Blogs

# Create your views here.

def index(request):
    return HttpResponse("this is index page")

def blog(request):
    if request.method == 'POST':
        blog = BlogForm(request.POST, request.FILES)
        if blog.is_valid():
            if request.FILES:
                f = request.FILES['file']
                title = handle_uploaded_file(f)
            else:
                title = blog.cleaned_data['title']
                body = blog.cleaned_data['body']
                author = blog.cleaned_data['author']
                filename = "log/upload/{}.xml".format(title)
                root = xml.Element("Blogs")
                blogelement = xml.Element("blog")
                root.append(blogelement)

                title_element = xml.SubElement(blogelement, "title")
                title_element.text = str(title)

                body_element = xml.SubElement(blogelement, "body")
                body_element.text = str(body)

                author_element = xml.SubElement(blogelement, "author")
                author_element.text = str(author)

                tree = xml.ElementTree(root)
                # print(root[0][0].text)
                tree.write(filename)
            
            b = Blogs()
            b.blog_titles = title
            b.save()

            return HttpResponse("blog posted")
            # parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
            # tree = etree.parse('log/upload/{}.xml'.format(title), parser=parser)
            # # extraction of information
            # root = tree.getroot()
            
            # return HttpResponse("{}<br>{}<br>{}".format(root[0][0].text, root[0][1].text, root[0][2].text))
    else:
        blog = BlogForm()
        return render(request, 'log/login.html', {'form':blog})

def saved_blog(request, given_title):
    for blog in Blogs.objects.all():
        if blog.blog_titles == given_title:
            parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
            tree = etree.parse('log/upload/{}.xml'.format(given_title), parser=parser)
            # extraction of information
            root = tree.getroot()
            return HttpResponse("{}<br>{}<br>{}".format(root[0][0].text, root[0][1].text, root[0][2].text))
    return HttpResponse("will show saved blogs of title:{}".format(given_title))
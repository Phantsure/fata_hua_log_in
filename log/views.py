from django.shortcuts import render, redirect
from django.http import request, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from lxml import etree
import xml.etree.ElementTree as xml
import os

from .forms import BlogForm
from .functions import handle_uploaded_file
from .models import Blogs

# Create your views here.

def index(request):
    return HttpResponse("this is index page. go to log/blog for blog or go to log/cat to see cats")

def cat(request):
    if request.method == 'POST':
        title = request.POST['title']
        # print(title)
        delete_saved_blog(request, given_title=title)
        return redirect('https://www.google.com/search?q=cats')
    return render(request, 'log/cat.html')

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
            print(request.GET.get('deleteButton'))
            if(request.GET.get('deleteButton')):
                return HttpResponseRedirect(reverse('log:delete_saved_blog', args=(given_title,)))
            else:
                parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
                tree = etree.parse('log/upload/{}.xml'.format(given_title), parser=parser)
                # extraction of information
                root = tree.getroot()
                return render(request,'log/saved_blog.html', {'blog_title':root[0][0].text, 'blog_content':root[0][1].text, 'blog_author':root[0][2].text})
    return HttpResponse("will show saved blogs of title:{}".format(given_title))

# solve delete problem

def delete_saved_blog(request, given_title):
    for blog in Blogs.objects.all():
        if blog.blog_titles == given_title:
            blog.delete()
            os.remove('log/upload/{}.xml'.format(given_title))
            return render(request, 'log/deleted_blog.html', {'given_title':given_title})
    return render(request, 'log/deleted_blog.html', {'given_title':given_title})
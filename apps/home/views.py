from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render
from .models import *
import qrcode
from django.core.files import File
import os
from .forms import *
from django.http import FileResponse


@login_required(login_url="/login/")
def index(request):

    context = {
        
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:

        load_template = request.path.split('/')[-1]
        print(request.path.split('/')[-1])

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def generator(request):
    context = {
        'url': None,
        'segment': 'generate'
    }
    return render(request, 'home/generator_qr.html', context)


def file_input_view(request):
    if request.method == 'POST':
        form = CreatePdfForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            try:
                docs = DocsObjects.objects.filter(id=form.cleaned_data['url']).first()
                if docs:
                    docs.file = uploaded_file
                    docs.code = form.cleaned_data['code']
                    docs.save()
            except:
                pass
        form = CreatePdfForm()
    else:
        form = CreatePdfForm()

    return render(request, 'home/add_file.html', {'form': form, 'segment': 'add_file'})


def generate_qr_code(request):
    if request.method == "POST":
        docs = DocsObjects.objects.create()
        docs.save()
        url = f'http://127.0.0.1:8000/file/{docs.id}'
        q = qrcode.make(url)
        q.save('qrcode.png')
        with open('qrcode.png', 'rb') as img_file:
            docs.qrcode.save(os.path.basename('qrcode.png'), File(img_file))
            docs.save()
        context = {
            'url': docs.id,
            'segment': 'generate',
            'docs': docs
        }
        return render(request, 'home/generator_qr.html', context)
    else:
        context = {
            'url': None,
            'segment': 'generate'
        }
        return render(request, 'home/generator_qr.html', context)


def get_file_guid(request, id):
    if request.method == 'POST':
        form = GetPinForm(request.POST)
        if form.is_valid():
            try:
                docs = DocsObjects.objects.filter(id=id).first()
                if docs and docs.code == form.cleaned_data['code']:
                    file_field = docs.file
                    if file_field:
                        file_name = file_field.name.split('/')[-1]
                        response = FileResponse(file_field, filename=file_name)
                        return response
            except:
                pass
        form = GetPinForm()
    else:
        form = GetPinForm()

    return render(request, 'home/get_file.html', {'form': form})

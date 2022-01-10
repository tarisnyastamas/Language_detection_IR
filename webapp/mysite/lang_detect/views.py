# Create your views here.
from django.shortcuts import render
import json
from django.contrib.auth.models import User #####
from django.http import JsonResponse , HttpResponse ####

import requests
from bs4 import BeautifulSoup


def index(request):
    return HttpResponse("Hello, world. You're at the language detection index.")



def strip(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text)
    text = soup.get_text()
    filtered_text = text.replace("\t", "").replace("\r", "").replace("\n", "")

    return filtered_text



# https://pypi.org/project/wikipedia/#description
def get_lang(request):
    
    url = request.GET.get('topic', None)

    print('topic:', url)

    data = {
        #'summary': wikipedia.summary(topic, sentences=1),
        'lang': "This site is in " + strip(url)
    }

    print('json-data to be sent: ', data)

    return JsonResponse(data)
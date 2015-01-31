# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic import View
from django.http import Http404, HttpResponse
import json
import os
import os.path
from os import walk
from django.views.decorators.csrf import csrf_exempt
from jsonpath_rw import jsonpath, parse
import re
import time
from . import DATA_IP, DATA_USER
from lightcontrol.utils import LightControl

# Create your views here.
# https://pypi.python.org/pypi/jsonpath-rw

class PageView(TemplateView):
    template_name = 'content/base.html'

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)

    

        return context


@csrf_exempt
def notify(request):
    if request.method == 'POST':
        rulesPath = os.path.join(os.getcwd(),"rules")

        requestRule = request.body
        bFinRule = False
        matchRule = ''


        for (dirpath, dirnames, filenames) in walk(rulesPath):
            for filename in filenames:
                if filename.endswith(".rle"):
                    filePath = os.path.join(rulesPath, filename)
                    f = open(filePath,'r')
                    fdata = ""
                    while 1:
                        line = f.readline()
                        if not line:break
                        fdata += line
                    f.close()

                    # compare simple strings
                    if requestRule.replace(' ', '') == fdata.replace(' ', ''):
                        bFinRule = True
                        matchRule = filename  

                        break

                    else: # compare complex rule
                        try:
                            complexRule = parse(fdata) 
                            js = json.loads(requestRule)
                            m = [match.value for match in complexRule.find(js)]
                            if not len(m) == 0:
                                bFinRule = True
                                matchRule = filename  

                                break
                        except Exception, e:
                            pass
                        else:
                            pass
                        finally:
                            pass

            break

        response_data = {  }
        if bFinRule:
            colorRules(filename)
            response_data['result'] = 'ok'
            response_data['matchRule'] = matchRule
        else:
            response_data['result'] = 'failed'
            if matchRule == '':
                response_data['matchRule'] = 'No matching rule'
        

        return HttpResponse(json.dumps(response_data), content_type="application/json")    
    else:
        response_data = {  }
        response_data['result'] = 'failed'
        response_data['message'] = 'Use POST method'

        return HttpResponse(json.dumps(response_data), content_type="application/json")    


# read color rules
def colorRules(fileName):
    colorPath = os.path.join(os.getcwd(),"rules", fileName.replace('.rle', '.clr'))
    p = re.compile('^[0-9]+$')

    f = open(colorPath, 'r')
    fdata = ""
    
    cIn = 0
    cOut = 0
    cnt = 0
    sleep = 0
    context = None
    while 1:
        line = f.readline()
        if not line:break

        if line.strip() == '':
            continue

        if p.match(line):
            sleep = int(line) / 1000
            fdata = ''
            cIn = 0
            cOut = 0

            time.sleep(sleep)
            sleep = 0
            continue

        cIn = cIn + line.count('{')
        cOut = cOut + line.count('}')
        cnt = cIn - cOut

        fdata += line

        
        if cnt == 0:
            if not fdata.strip() == '':
                context = executeColor(fdata, context)

            fdata = ''
            cIn = 0
            cOut = 0

    f.close()


def executeColor(colorString, _context = None):
    context = {}
    if not _context == None:
        context = _context
    
    if 'data' in colorString:
        jdata = json.loads(colorString)

        context['DATA_IP'] = jdata['data']['ip']
        context['DATA_USER']=jdata['data']['user']

    if 'light' in colorString:
        jdata = json.loads(colorString) 

        for lightId in jdata['lights']:
            lightData = json.dumps(jdata['light'])
            print 'Light id:{0}, ip:{1}  user: {2} || {3}'.format(lightId, context['DATA_IP'], context['DATA_USER'], lightData)

            LightControl(context['DATA_IP'], context['DATA_USER'], lightId, lightData)            

    return context
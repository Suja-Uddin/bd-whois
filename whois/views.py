from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponse,HttpResponseRedirect
from django.db import connection
from collections import namedtuple
from django.shortcuts import render_to_response 
from django.template import RequestContext
from django.contrib import auth
import urllib.request
import re
from bs4 import BeautifulSoup

def index(request,error=0):
	tmpl=loader.get_template("index.html")
	
	extension=['com','co','edu','gov','info','net','org','ac','mil','tv','ws']
	if error==1:
		context=RequestContext(request, {'extension':extension,'error':error})
	else:
		context=RequestContext(request, {'extension':extension,})

	return HttpResponse(tmpl.render(context))

def show_result(request):
	tmpl=loader.get_template("result.html")
	domain_name=request.POST.get('domain_name',"")
	extension=""
	found=0
	for i in range(0,len(domain_name)):
		if found==1:
			extension+=str(domain_name[i])
		if domain_name[i]=='.':
			found=1
	print(extension)
	extension_list=['com','co','edu','gov','info','net','org','ac','mil','tv','ws']
	found=0
	for ii in extension_list:
		if extension==ii:
			found=1
	if found==0:
		return index(request,1)
	url = "http://domainreg.btcl.com.bd/domain/show/%s.bd"%(domain_name,)
	request1 = urllib.request.Request(url)
	response = urllib.request.urlopen(request1)
	data=response.read().decode('utf-8')
	print("done loading page")

	#print(data)
	print("After ...")

	soup=BeautifulSoup(data,"html.parser")
	domain_info=soup.findAll('dd')
	info=[]

	for item in domain_info:
	    print(item.contents[0])
	    info.append(item.contents[0])
	print(info)    
	
	
	if len(info)==0:
		available='true'
		context=RequestContext(request,{'info':info,'available':available,'extension':extension_list})
		return HttpResponse(tmpl.render(context))

	context=RequestContext(request,{'info':info,'extension':extension_list})
	return HttpResponse(tmpl.render(context))
# Create your views here.

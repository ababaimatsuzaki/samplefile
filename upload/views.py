from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from upload.models import Document
from upload.forms import DocumentForm

import os
import glob
import shutil
import re
import codecs

import csv
import pprint
import pickle

def index(request):
    documents = Document.objects.all()
    return render(request, 'index.html', { 'documents': documents })

def basic_upload(request):
#    if request.method == 'POST' and request.FILES['testfile']:
    if request.method == 'POST':
        myfile = request.FILES['testfile']
        filepass = request.POST['pass']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
# 同じファイル名で保存

        file_name = "./media/" + filename
#        dirs = "/ando/files/theme/ababai/images/abs"
        dirs = filepass
        outfile_name = "./media/output/" + filename + ".csv"
        csvlink = "/media/output/" + filename + ".csv"
        with codecs.open(file_name, 'r', 'euc_jp', 'ignore') as f:
            data_lines = f.read()
# csv処理
        data_lines = data_lines.replace("<>", "\t")# <>をタブに変換
# wysiwyg処理
        data_lines = data_lines.replace("&lt;", "<")# <をタブに変換
        data_lines = data_lines.replace("&gt;", ">")# >をタブに変換
        data_lines = data_lines.replace("&amp;", "＆")# 全角アンド
        data_lines = data_lines.replace("&quot;", "”")# 全角ダブルクォーテーション
        data_lines = data_lines.replace("&apos;", "’")# 全角シングルクォーテーション
        data_lines = data_lines.replace("&nbsp;", "　")# 全角スペース
        data_lines = data_lines.replace("&hearts;", "♥")# 全角スペース
        data_lines = data_lines.replace("&hellip;", "…")# 全角スペース
        data_lines = data_lines.replace("alt=\"\"", "")# 全角スペース
        data_lines = data_lines.replace("src=\"/uploads/", "src=\"" + dirs + "/uploads/")# 全角スペース


        with codecs.open( outfile_name, 'w', 'euc_jp', 'ignore') as f:
             f.write(data_lines)


        return render(request, 'basic_upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'csvlink': csvlink

        })


    return render(request, 'basic_upload.html')


# 単一画像ファイル

def images_upload(request):
#    if request.method == 'POST' and request.FILES['testfile']:
    if request.method == 'POST':
        myfile = request.FILES['testfile']
        filepass = request.POST['pass']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        file_name = "./media/" + filename
        outfile_name = "./media/output/" + filename
        csvlink = "/media/output/" + filename
        data_lines = []

        with open(file_name, 'r') as f:
            data = f.read().splitlines()

        s = 0
        abaluckimg = [] #配列に格納
        for i in data:
            abaluckimg.append("{\"file\":\"" + filepass + data[s] + "\"}")
            s += 1

        with open(outfile_name, 'w') as f:
            for d in abaluckimg:
                f.write("%s\n" % d)

        return render(request, 'images_upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'csvlink': csvlink

        })


    return render(request, 'images_upload.html')

# ギャラリー

def gallery_upload(request):
#    if request.method == 'POST' and request.FILES['testfile']:
    if request.method == 'POST':
        myfile = request.FILES['testfile']
        filepass = request.POST['pass']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        file_name = "./media/" + filename
        outfile_name = "./media/output/" + filename
        csvlink = "/media/output/" + filename

        with open(file_name) as f:
            reader = csv.reader(f, delimiter='\t')
            l = [row for row in reader]

#print(l)
        sqllist = []
        sqlno = 0
        imgno = 0

        for i in l:
            imagestext = l[imgno] #配列に格納
            abaluckimg = [] #配列に格納
            text = "[" #配列に格納
            s = 0
            ano = 0

            for i in range(int(imagestext[0])):
                s += 1
                abaluckimg.append("{\"filename\":\"" + filepass + imagestext[s] + "\",\"title\":\"")
#                s += 1
#キャプション処理
                abaluckimg[ano] = abaluckimg[ano] + "\"},"
#       abaluckimg[ano] = abaluckimg[ano] + imagestext[s] + "\"},"
                text = text + abaluckimg[ano]


                ano += 1

            text = text.rstrip(",")
            text = text + "]"

            sqllist.append(text)
#   print(sqllist[sqlno])
            sqlno += 1
            imgno += 1

        with open(outfile_name, 'w') as f:
            for d in sqllist:
                f.write("%s\n" % d)

        return render(request, 'gallery_upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'csvlink': csvlink

        })


    return render(request, 'gallery_upload.html')

def gallerycap_upload(request):
#    if request.method == 'POST' and request.FILES['testfile']:
    if request.method == 'POST':
        myfile = request.FILES['testfile']
        filepass = request.POST['pass']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        file_name = "./media/" + filename
        outfile_name = "./media/output/" + filename
        csvlink = "/media/output/" + filename

        with open(file_name) as f:
            reader = csv.reader(f, delimiter='\t')
            l = [row for row in reader]

#print(l)
        sqllist = []
        sqlno = 0
        imgno = 0

        for i in l:
            imagestext = l[imgno] #配列に格納
            abaluckimg = [] #配列に格納
            text = "[" #配列に格納
            s = 0
            ano = 0

            for i in range(int(imagestext[0])):
                s += 1
                abaluckimg.append("{\"filename\":\"" + filepass + imagestext[s] + "\",\"title\":\"")
                s += 1
#キャプション処理
#                abaluckimg[ano] = abaluckimg[ano] + "\"},"
                abaluckimg[ano] = abaluckimg[ano] + imagestext[s] + "\"},"
                text = text + abaluckimg[ano]


                ano += 1

            text = text.rstrip(",")
            text = text + "]"

            sqllist.append(text)
#   print(sqllist[sqlno])
            sqlno += 1
            imgno += 1

        with open(outfile_name, 'w') as f:
            for d in sqllist:
                f.write("%s\n" % d)

        return render(request, 'gallerycap_upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'csvlink': csvlink

        })


    return render(request, 'gallerycap_upload.html')


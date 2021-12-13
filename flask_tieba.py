from flask import Flask , request 
from flask import  make_response
from flask_restful import Resource, Api
import time
import urllib.parse

import re
import requests
from lxml import etree

BDUSS=BUDSS
TIEBANAME=贴吧名
NETNAME=网站地址
 

TIEBANAME_url=urllib.parse.quote(TIEBANAME,encoding='utf-8') 

def httpget(url):
        
    cookies = { 
        'BDUSS': BDUSS
    }

    headers = {
        'Proxy-Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.41',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Referer': 'https://tieba.baidu.com/f?ie=utf-8&kw='+TIEBANAME_url+'&ie=utf-8'
    }


    params = (
        ('word', TIEBANAME),
        ('ie', 'utf-8')
    )

    response = requests.get(url, headers=headers, params=params, cookies=cookies, verify=False)
    res=response.text
    res=res.replace('<img src="/','<img src="https://tieba.baidu.com/')  
    res=res.replace('<img', '<img referrerpolicy="no-referrer"' )
    res=re.sub('<div class="user_info">(.*)</div><nav class="nav">','<div class="user_info"><p class="info_mesaage">'+TIEBANAME+'务后台公开</p></div><nav class="nav">',res)
     
    return res 
class _index(Resource):
    def post(self ):
        return self.get( )
    def get(self ): 
         
        res=httpget('http://tieba.baidu.com/bawu2/platform/index')
        
        return make_response(res)

class _listPostLog(Resource):
    def post(self ):
        return self.get( )
    def get(self ): 
         
        res=httpget(request.url.replace(NETNAME,'http://tieba.baidu.com'))
        res=res.replace('<li><a target="_blank" href="','<li><a target="_blank" referrerpolicy="no-referrer" href="')
        res=res.replace('<a target="_blank" href="/','<a target="_blank" referrerpolicy="no-referrer" href="https://tieba.baidu.com/')
        res=res.replace('<img referrerpolicy="no-referrer" src="http://tb1.bdstatic.com/tb/static-frs/img/blank.gif?v=1" original=','<img referrerpolicy="no-referrer" src=')
        res=res.replace('mImg.getAttribute(\'original\')','mImg.getAttribute(\'src\')')
        table=re.search('<table class="data_table">(.*)</table>',res)
        if table is not None:
            table=table.group()
            res=re.sub('<table class="data_table">(.*)</table>','AAAAAAAAAAAAAAAAAAAAAaa',res)
            html=etree.HTML(table)
            x=html.xpath('//table[@class="data_table"]/tbody/tr/td[2]/span')
            for i in range(len(x)):
                if html.xpath('//table[@class="data_table"]/tbody/tr/td[2]/span')[i].text=='屏蔽':
                    html.xpath('//table[@class="data_table"]/tbody/tr/td[1]/article/div[2]/h1/a')[i].set('href','https://tieba.baidu.com/')
                    html.xpath('//table[@class="data_table"]/tbody/tr/td[1]/article/div[1]/div[2]/a')[i].set('href','https://tieba.baidu.com')
                    html.xpath('//table[@class="data_table"]/tbody/tr/td[1]/article/div[1]/div[1]/a')[i].set('href','https://tieba.baidu.com')
                    
            table=str(etree.tostring(html),encoding='utf-8')
            res=re.sub('AAAAAAAAAAAAAAAAAAAAAaa',table,res)
        return make_response(res)
class _listUserLog(Resource):
    def post(self ):
        return self.get( )
    def get(self ): 
         
        res=httpget(request.url.replace(NETNAME,'http://tieba.baidu.com'))
        res=res.replace('<a class="avatar_link" target="_blank" href="/','<a class="avatar_link" target="_blank" href="https://tieba.baidu.com/')
        return make_response(res)
class _data(Resource):
    def post(self ):
        return self.get( )
    def get(self ): 
         
        res=httpget(request.url.replace(NETNAME,'http://tieba.baidu.com'))
        return make_response(res)
class _dataExcel(Resource):
    def post(self ):
        return self.get( )
    def get(self ): 
         
        res=httpget(request.url.replace(NETNAME,'http://tieba.baidu.com'))
        res=make_response(res)
        res.headers['Content-Disposition']='attachment; filename="bawudata_'+ time.strftime("%Y%m%d", time.localtime())+'.xls'
        return res 
class _listBawuLog(Resource):
    def post(self ):
        return self.get( )
    def get(self ): 
         
        res=httpget(request.url.replace(NETNAME,'http://tieba.baidu.com'))
        return make_response(res)
 
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)

api.add_resource(_index, '/') 
api.add_resource(_listPostLog, '/bawu2/platform/listPostLog') 
api.add_resource(_listUserLog, '/bawu2/platform/listUserLog')
api.add_resource(_data, '/bawu2/platform/data')
api.add_resource(_dataExcel, '/bawu2/platform/dataExcel')
api.add_resource(_listBawuLog, '/bawu2/platform/listBawuLog')   


if __name__ == '__main__':
     
    app.run(debug=True, host='127.0.0.1',port=8010,threaded=2)

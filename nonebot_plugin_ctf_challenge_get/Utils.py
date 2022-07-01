from cProfile import run
import requests,json,time
from bs4 import BeautifulSoup

def get_ctfhub(id=0):
    url = "https://api.ctfhub.com/User_API/Event/getUpcoming"
    param = {"offset":0,"limit":5}
    r = requests.post(url,json=param)
    x = json.loads(r.text)
    if id:
        url = "https://api.ctfhub.com/User_API/Event/getInfo"
        param = {"event_id": x['data']['items'][id-1]['id']}
        r = requests.post(url,json=param)
        detail = json.loads(r.text)['data']
        
        res='''[{}]
比赛形式: {}
比赛官网: {}
比赛时间: {}~{}
'''.format(detail['title'],detail['form'],detail['official_url'],time.strftime('%Y-%m-%d %H:%M',time.localtime(detail['start_time'])),time.strftime('%Y-%m-%d %H:%M',time.localtime(detail['end_time'])))
        return res
    else:
        res = "最近的5场比赛:\n"
        k=1
        for i in x['data']['items']:
            Timestampi = i['start_time']
            Timestampnow = time.time()
            if Timestampi<Timestampnow:
                t = '正在进行'
            else:
                t = time.localtime(Timestampi)
                t = time.strftime('%Y-%m-%d',t)
            res+= "{}. [{}] {}\n".format(k,t,i["title"])
            # res+= str(k) + ". " + "[" + time.strftime('%Y-%m-%d',t)+"] "  + i["title"] + "\n"
            k+=1
        res+="\n回复 序号 查看详情"
        return res

def get_adworld() -> str:
    url = "https://adworld.xctf.org.cn/api/evts/list"
    param = {"limit":4,"offset":0,"search":""}
    r = requests.get(url,params=param)
    x = json.loads(r.text)
    k=1
    res=""
    nores=""
    for i in x['rows']:
        if i["process"]!=0:
            continue
        res+="{}. [{}] {}\n".format(k,i['start_time'],i['name_zh'])
        k+=1
    if k==1:
        nores = "近期没有比赛哦~\n上一场比赛是{}\n回复 review+(比赛名称) 查看比赛详情".format(x['rows'][0]['name_zh'])
    else:
        res+="\n回复 序号 查看详情"
    return nores,res

def review_adworld(name) -> str:
    url = "https://adworld.xctf.org.cn/api/evts/list"
    param = {"limit":1,"offset":0,"search":name}
    r = requests.get(url,params=param)
    x = json.loads(r.text)
    res=""
    i = x['rows'][0]
        # res+=str(k) + ". " + "[" + i["start_time"][:10] + "] " + i["name_zh"]+"\n"
    res+='''[{}]
比赛介绍: {}
比赛官网: https://adworld.xctf.org.cn/match/guide?event={}&hash={}
比赛时间: {}~{}'''.format(i['name_zh'],i['description_zh'],i['id'],i['hash'],i['start_time'],i['end_time'])
    return res

def get_BUUCTF(id=0) -> str:
    url="https://buuoj.cn/match/matches"
    params = {"public":1,"is_start":3}
    r = requests.get(url,params=params)

    # print(r.text)
    soup = BeautifulSoup(r.text,'lxml')

    competition = {'running':[],'upComing':[],'stop':[]}

    for i in soup.findAll('div',class_='mb-3'):
        card = {}
        card['title'] = i.find('h5',class_='mb-1').text
        card['link'] = url + '/' + i.get('onclick').split("'")[1].split("/")[-1]
    
        card['start_time'] = i.findAll('script')[0].string.split('"')[1].partition('+')[0].replace('T',' ')
        start_time = time.mktime(time.strptime(card['start_time'],"%Y-%m-%d %H:%M:%S"))
        card['end_time'] = i.findAll('script')[1].string.split('"')[1].partition('+')[0].replace('T',' ')
        end_time = start_time = time.mktime(time.strptime(card['end_time'],"%Y-%m-%d %H:%M:%S"))
        card['category'] = i.findAll('span')[1].text

        now_time = time.time()
        if(start_time>now_time):
            card['status'] = 0 #比赛还未开始
            competition['upComing'].append(card)
        elif (end_time<now_time):
            card['status'] = 1 #比赛已经结束
            competition['stop'].append(card)
        else:
            card['status'] = 2 #比赛正在进行
            competition['running'].append(card)
    res=""
    if id:
        i = competition['stop'][id-1]
        res+='''[{}]
比赛类别: {}
比赛官网: {}
比赛时间: {}~{}'''.format(i['title'],i['category'],i['link'],i['start_time'],i['end_time'])
    else:
        k = 1
        if not competition['upComing'] or not competition['running']:
            return res
        else:
            for i in competition['upComing']:
                res+='{}. [{}] {}\n'.format(k,i['start_time'],i['title'])
                k+=1
            res+='\n回复 序号 查看详情'

    return res
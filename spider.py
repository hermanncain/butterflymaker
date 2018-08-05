import urllib.request,socket,re,sys,os,http,time,codecs,random
import agents

# use http 1.0 rather than default 1.1 to handle chunk reading incompletement
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

# settings for request
MAX_TRY = 10
MAX_WAIT = 3
socket.setdefaulttimeout(2000)

# butterfly list page and image page
baseURL='http://flutter-butterfly-sanctuary.wikia.com/wiki/'
bimgurl = 'http://flutter-butterfly-sanctuary.wikia.com/wiki/File:'
postfix = '%C2%A7Headericon.png'

# butterflies in this game are divided into sets: core sets & event sets
# core set is included by both event sets with display=none
pages=['Event_Sets','Event_Sets_2']

targetPath = "./img/"
butterflyLabels = []

def waitSecs():
    time.sleep(MAX_WAIT*random.random())

def getPage(Weburl):
    print('reading '+Weburl+' ...')
    Webheader= {'Upgrade-Insecure-Requests':'1',
                'User-Agent':random.sample(agents,1)[0]}
    req = urllib.request.Request(url = Weburl,headers=Webheader)
    respose = urllib.request.urlopen(req)
    
    for i in range(MAX_TRY):
        try:
            _page = respose.read()
            print('succeeded')
            respose.close()
            return str(_page)
        except:
            respose.close()
            if i<MAX_TRY:
                waitSecs()
                continue
            else:
                print('failed: time out')
                
def getLabels(content):
    names = []
    labels = []
    # get indices, names, rarities, sizes
    comp = re.compile(r'</sup>(\d{1,4}).{5,100}title="(.{1,50})">.{5,100}title="(.{3,10})".{5,100}title="(.{3,10})"')
    butterflyList = comp.findall(content)
    for butterfly in butterflyList:
        no = butterfly[0]
        name = butterfly[1].replace(' ','_')
        rarity = butterfly[2]
        size = butterfly[3]
        label = '#'+no+','+name+','+rarity+','+size
        labels.append(label)
        names.append(name)
        print('#'+no+' '+name)
    return labels

def dldImg(label):
    keys = label.split(',')
    index = keys[0]
    name = keys[1]
    rarity = keys[2]
    size = keys[3]
    filename = index+','+rarity+','+size+'.png'

    # skip the exsistings
    if os.path.exists('img/'+filename):
        return
    # turn name to web format
    name = name.replace('\\\'','%27')

    # get imgurl
    pageROI = getPage(bimgurl+name+postfix)
    pageROI = pageROI[pageROI.find('fullImageLink'):pageROI.find('fullMedia')]
    urlPattern = re.compile(r'<a href="(.{50,200})">')
    rurl = urlPattern.findall(pageROI)

    # if len(rurl)==0, pageROI got nothing from getPage()
    # then rurl[0] will raise exception caught by downloadButterflies() leading to re-downloading
    imgurl = rurl[0][:rurl[0].find('.png')+4]
    print('from '+imgurl+' downloading '+index+name+'...')
    waitSecs()
    opener=urllib.request.build_opener()
    head = random.sample(agents,1)[0]
    opener.addheaders=[('User-Agent',head)]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(imgurl,targetPath+filename)

def getButterflies():
    print('======Getting butterflies======')
    for p in pages:
        pageROI = getPage(baseURL+p)
        pageROI = pageROI[pageROI.find('mw-content-text'):pageROI.find('printfooter')]
        bLabels = getLabels(pageROI)
        butterflyLabels += bLabels
        waitSecs()
    # remove redundancy
    butterflyLabels = list(set(butterflyLabels))
    with open("butterflies.txt",'w','utf-8') as f:
        f.writelines([label+'\n' for label in butterflyLabels])

# TODO    
def updateButterflies():
    pass

def loadButterflies():
    print('======Loading butterflies======')
    butterflyLabels = []
    with open('butterflies.txt','r') as f:
        for line in f.readlines():
            butterflyLabels.append(line.strip('\n'))

def downloadButterflies():
    print('======Start downloading======')
    while True:
        try:
            for label in butterflyLabels:
                dldImg(label)
                waitSecs()
            break
        except:
            continue

def main():
    if(os.path.exists('butterflies.txt')):
        loadButterflies()
    else:
        getButterflies()
    downloadButterflies()

if __name__ == '__main__':
    main()

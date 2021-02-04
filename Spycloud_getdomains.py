import requests
import ConfigParser
import string
import sys
import json

def getLastDate():
    response = requests.get("https://api.spycloud.io/enterprise-v2/watchlist/identifiers/?watchlist_type=&verified=yes",headers={'X-Api-Key': apikey})
    output = response.json()
    l=[]
    for each in output['results']:
        l.append(each['last_discovered'])
    l.sort(reverse=True)
    return l[0][0:10]
def iterateSpyCloud(cursor):
    response = requests.get("https://api.spycloud.io/enterprise-v2/breach/data/watchlist/?type=&since="+lastDATE,headers={'X-Api-Key': apikey, 'cursor': cursor})
    results = response.json()#['results']
    for each in results['results']:
        print json.dumps(each)
        #print each['email'],",",each['domain'],",",each['spycloud_publish_date'][0:10],",",each['severity']
    try:  ## Continue ti iterate to get the next page
        cursor = response.json()['cursor']
        if len(cursor) > 0:
            iterateSpyCloud(cursor)
    except BaseException as e:
        print e.message
        print("NOK")

#please update <apikey> 
apikey='<apikey>'
cfgfile='/opt/splunk/bin/scripts/spycloud.ini'
Config = ConfigParser.SafeConfigParser()
Config.read(cfgfile)
lastDATE = Config.get('spycloud','DATE')
newLastDate=getLastDate()

if (lastDATE != newLastDate):
    iterateSpyCloud("")
    Config.set('spycloud','DATE',newLastDate)
    cfgfilew=open(cfgfile,'w')
    Config.write(cfgfilew)
    cfgfilew.close()

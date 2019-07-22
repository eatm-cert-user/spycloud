import requests
import ConfigParser
import string
import sys
import json

def getLastDate():
    response = requests.get("https://api.spycloud.io/enterprise-v1/watchlist/identifiers/?watchlist_type=domain&verified=yes",headers={'X-Api-Key': apikey})
    output = response.json()
    #print output
    l=[]
    for each in output['results']:
        #print each['last_discovered']
        l.append(each['last_discovered'])
    l.sort(reverse=True)
    #print "lastdate:",l[0][0:10]
    return l[0][0:10]
def iterateSpyCloud(cursor):
    response = requests.get("https://api.spycloud.io/enterprise-v1/breach/data/watchlist/?type=corporate&since="+lastDATE,headers={'X-Api-Key': apikey, 'cursor': cursor})
    #print response
    #print "Dedug: lastdate:",lastDATE
    results = response.json()#['results']
    #print(results)  ## Prints results froms Spycloud API
    #print "email,domain,spycloud_publish_date"
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
#print Config.sections()
lastDATE = Config.get('spycloud','DATE')
newLastDate=getLastDate()

if (lastDATE != newLastDate):
    iterateSpyCloud("")
    Config.set('spycloud','DATE',newLastDate)
    cfgfilew=open(cfgfile,'w')
    Config.write(cfgfilew)
    cfgfilew.close()
#print "lastdate:",lastDATE
#print "newlastdate:",newLastDate

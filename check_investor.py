import requests
import os
import csv
import re
import time
headers = {'accept': 'text/html,application/xhtml+xml,application/xml','user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

domains = []
with open('import.csv','r') as csv_file:
    reader = csv.DictReader(csv_file, delimiter=",")
    i=1
    for row in reader:
        domains.append({'index':f'Serial_{i}','root_address':row['links']})
        i+=1

def testURL(url):
    try:
        resp = requests.get(url,timeout=3,headers=headers)
        resp.connection.close()
        if resp.status_code!=200:
            return False
        else:
            return resp
    except:
        return False

def Investor_pattern(root):
    pattern = {
        'p0' : f"http://{root}//investor",
        'p1' : f"http://investor.{root}",
        'p2' : f"http://investors.{root}",
        'p3' : f"http://{root}/investor-relation",
        'p4' : f"http://{root}/investor-relations",
        'p5' : f"http://ir.{root}",
        'p6' : f"http://{root}/investors",
        'p7' : f"http://corp.{root}",
        'p8' : f"http://{root}//investor-relations",
        'p9' : f"http://{root}//investors",
        'p10' : f"http://{root}//shareholders",
        'p11' : f"http://{root}//partners",
        'p12' : f"http://{root}/investor"
        }
    return pattern

def Investot_relation():
    result=[]
    for domain in domains:
        pattern = Investor_pattern(domain['root_address'])
        print(f'\t{domain}')
        request_url = pattern['p4']
        try:
            test = requests.get(request_url,timeout=3,headers=headers)
            if test.status_code==200:
                info = {
                    'index':domain['index'],
                    'domain':domain['root_address'],
                    'request_url':request_url,
                    'response_url':test.url,
                    'status':test
                    }
                result.append(info)
                print(info)
            else:
                pass
        except:
            pass
    return result


def Press_pattern(root):
    regex = r'^http:\/\/www\.|^https:\/\/www\.|^https:\/\/|^http:\/\/|^www\.|\/$'
    url = re.sub(regex,'',root)
    pattern = {
        '0' : f"http://{url}//press-releases",
        '1' : f"http://{url}//news-releases",
        '2' : f"http://{url}//news",
        '3' : f"http://{url}//news-and-events",
        '4' : f"http://{url}//financial-releases",
        }
    return pattern


def press_release_with_switchCase():
    matched_result = []
    unmatched_result = []
    for domain in domains:
        url = Press_pattern(domain['root_address'])
        i=0
        while True:
            if i==5:
                unmatched_result.append({'index':domain['index'],'remaining urls':domain['root_address']})
                print(f"'index':{domain['index']} - did not match any pattern for {domain['root_address']}")
                break
            r = testURL(url[str(i)])
            if r == False:
                pass
            elif r != False:
                info = {
                    'index':domain['index'],
                    'domain':domain['root_address'],
                    'request_url':url[str(i)],
                    'response_url':r.url,
                    'status':r
                    }
                matched_result.append(info)
                print(info)
                break
            i+=1
    return matched_result, unmatched_result


#result = Investot_relation()

matched_result, unmatched_result = press_release_with_switchCase()

with open(f'export of matched result at {time.ctime()}.csv', 'w') as csvfile:
    fields = ['index','domain','request_url','response_url','status']
    writer = csv.DictWriter(csvfile, fieldnames = fields)
    writer.writeheader()
    writer.writerows(matched_result)
    csvfile.close()

with open(f'export of UNmatched result at {time.ctime()}.csv', 'w') as csvfile:
    fields = ['index','remaining urls']
    writer = csv.DictWriter(csvfile, fieldnames = fields)
    writer.writeheader()
    writer.writerows(unmatched_result)
    csvfile.close()

import requests
import math
import time

headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}


def main():
    pre_domain, keywords=[], []
    try:
        with open('results.txt', 'rb') as indomain: pre_domain = [ind.replace('\n', '').decode('utf-8') for ind in indomain]
    except:
        pass
    
    with open('keywords.txt', 'rb') as infile: keywords = [kw.replace("\n", "").replace("\t", '').replace("\r", '') for kw in infile]
    
    for kw in keywords:
        postHead = {'Accept': 'application/json, text/javascript, */*; q=0.01', 'Referer': 'https://domainpunch.com/tlds/daily.php', 'X-Requested-With': 'XMLHttpRequest',}
        params = (
            ('domains', ''), ('draw', '4'), ('columns[0][data]', '0'), ('columns[0][name]', ''), ('columns[0][searchable]', 'false'),
            ('columns[0][orderable]', 'false'), ('columns[0][search][value]', ''), ('columns[0][search][regex]', 'false'), ('columns[1][data]', '1'),
            ('columns[1][name]', ''), ('columns[1][searchable]', 'true'), ('columns[1][orderable]', 'true'), ('columns[1][search][value]', ''),
            ('columns[1][search][regex]', 'false'), ('columns[2][data]', '2'), ('columns[2][name]', ''), ('columns[2][searchable]', 'true'),
            ('columns[2][orderable]', 'true'), ('columns[2][search][value]', ''), ('columns[2][search][regex]', 'false'), ('columns[3][data]', '3'),
            ('columns[3][name]', ''), ('columns[3][searchable]', 'true'), ('columns[3][orderable]', 'true'), ('columns[3][search][value]', ''),
            ('columns[3][search][regex]', 'false'), ('columns[4][data]', '4'), ('columns[4][name]', ''), ('columns[4][searchable]', 'false'),
            ('columns[4][orderable]', 'false'), ('columns[4][search][value]', ''), ('columns[4][search][regex]', 'false'), ('order[0][column]', '2'),
            ('order[0][dir]', 'asc'), ('start', '0'), ('length', '250'), ('search[value]', str(kw)), ('search[regex]', 'false'), ('zid', '1'),
        )
        resp = s.get('https://domainpunch.com/tlds/daily.php', headers=postHead, params=params).json()
        
        total_pages = int(math.ceil(float(resp['recordsFiltered'])/250))
        current_list = list(set([dt['1'] for dt in resp['data']])-set(pre_domain))
        
        for tp in range(1, total_pages):
            old_param = map(list, params)
            
            for new in old_param:
                if new[0] == 'start': new[1] = str(tp*250)
            new_param = tuple(tuple(i) for i in old_param)
            
            resp = s.get('https://domainpunch.com/tlds/daily.php', headers=postHead, params=new_param).json()
            current_list.extend(list(set([dt['1'] for dt in resp['data']])-set(pre_domain)))
        
        with open('results.txt', 'ab') as outfile:
            for dmn in current_list:
                outfile.write(dmn.encode('utf-8')+'\n')
        
        print("{0} new-domains found for \"{1}\".".format(len(current_list), kw))


if __name__ == '__main__':
    predefined_interval=300 #value in seconds.
    
    print("Creating sesion\nStarting the loop\n")
    s = requests.session()
    
    s.headers.update(headers)
    s.get('https://domainpunch.com/tlds/daily.php')
    
    while True:
        main()
        
        print("\nSleeping for {0} second(s).\n".format(predefined_interval))
        time.sleep(predefined_interval)

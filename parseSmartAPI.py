import requests

def pull():
    response = requests.get("https://smart-api.info/api/query?limit=1000&q=TRAPI")
    kps = response.json()['hits']
    with open('status.txt','w') as outf:
        outf.write('infores\tcomponent\tteam\tx-maturity\turl\tpass\n')
        for kp in kps:
            try:
                team = kp['info']['x-translator']['team']
            except:
                continue
            component = kp['info']['x-translator']['component']
            infores = kp['info']['x-translator']['infores']
            for server in kp['servers']:
                url = server['url']
                maturity = server.get('x-maturity','???')
                if maturity == 'development':
                    passes = True
                elif maturity == 'production':
                    passes = (url.endswith('.translator.io') and not url.endswith('.ci.translator.io') and not url.endswith('.test.translator.io'))
                elif maturity == 'staging':
                    passes = (url.endswith('.ci.translator.io'))
                elif maturity == 'test':
                    passes = (url.endswith('.test.translator.io'))
                else:
                    passes = False
                outf.write(f'{infores}\t{component}\t{team}\t{url}\t{maturity}\t{passes}\n')

if __name__ == '__main__':
    pull()

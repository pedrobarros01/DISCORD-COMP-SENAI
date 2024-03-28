import requests
headers={
    'Host': 'senaiweb.fieb.org.br',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
    }
req = requests.get(f'https://senaiweb.fieb.org.br/MinhaAula/api/aulas?ra=019.705313', headers=headers)
data = req.json()
print(data)
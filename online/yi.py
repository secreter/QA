import requests
url='http://music.163.com/#/song?id=450048216'
params = {
'parserSelect':'English',
'parse':'Parse'
}  #python object
headers = {
}
req = requests.post(url, data=params, headers=headers)
print(req.text)
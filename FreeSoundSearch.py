import pycurl, json
from io import BytesIO

apikey = open('FreeSoundApiKey.txt', 'r').readline()


def GetResultForTag(target_tag):
    url = 'https://www.freesound.org/apiv2/search/text/?query={0}&token={1}'.format(target_tag, apikey)
    print(url)

    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    decoded_body = body.decode('iso-8859-1')
    return json.loads(decoded_body, encoding='iso-8859-1')





result = GetResultForTag('dog')



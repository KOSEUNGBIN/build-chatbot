
import logging
import json
import base64
import requests

log = logging.getLogger()
log.setLevel(logging.INFO)


def log(params):
    response = {
        "response_type": "in_channel",
        "text": "NOTHING"
    }

    if params['text']:
        config = json.loads(open("./config/jenkins-config.json").read())

        url = config['HOST'] + ':' + config['PORT'] + '/job/'+ params['text'] +'/lastBuild/consoleText'
        print(url)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic " + base64.urlsafe_b64encode((config['USER'] + ':' + config['PASSWD']))
        }

        jenkins_response = requests.get(url, headers=headers)

        if jenkins_response.status_code in [200, 201]:

            response['text'] = jenkins_response.text

        elif jenkins_response.status_code == 403:
            response['text'] = params['text']
            response['text'] += ' NOT EXIST'
        else:
            response['text'] = 'ERROR Request Jenkins'

    else:
        response['text'] = "/build_log <JOB>"
        response['text'] = "/build_log <JOB>"

    return response


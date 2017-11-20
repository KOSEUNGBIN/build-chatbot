
import logging
import json
import base64
import requests

log = logging.getLogger()
log.setLevel(logging.INFO)


def build(params):
    response = {
        "response_type": "in_channel",
        "text": "NOTHING"
    }

    if params['text']:
        config = json.loads(open("./config/jenkins-config.json").read())

        url = config['HOST'] + ':' + config['PORT'] + '/job/' + params['text'] + '/build'

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + base64.urlsafe_b64encode((config['USER'] + ':' + config['PASSWD']))
        }

        param = {
            "token": config['TOKEN']
        }

        print(url)
        jenkins_response = requests.get(url, headers=headers, params=param)
        print(jenkins_response)

        if jenkins_response.status_code in [200, 201]:

            response['text'] = "BUILD SUCCESS"

        elif jenkins_response.status_code == 403:
            response['text'] = params['text']
            response['text'] += ' NOT EXIST'
        else:
            response['text'] = 'ERROR Request Jenkins'

    else:
        response['text'] = "/build_list <JOB>"

    return response



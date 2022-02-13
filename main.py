import requests
import json as JSON
import time
import os.path
import discordtoken
import globals

CONFIG_FILE='config.json'

# load config
if not os.path.isfile(CONFIG_FILE):
    open(CONFIG_FILE, 'w')

config={}
with open(CONFIG_FILE, 'r') as _file:
    config=JSON.loads(_file.read())

globals.log.LOG_FILE=config['LOG_FILE']
globals.log.CONSOLE_LOGGING=config['CONSOLE_LOGGING']

globals.log.logger('config loaded')
globals.log.logger(config)

# load tokens
if not os.path.isfile(config['TOKENS_FILE']):
    open(config['TOKENS_FILE'], 'w')
    globals.log.logger('no tokens file existed so one was created')

tokens=[]
with open(config['TOKENS_FILE'], 'r') as _file:
    tokens = [token.rstrip() for token in _file]
    globals.log.logger(f'{len(tokens)} tokens were loaded')

globals.log.logger('everything loaded')

HEADERS={
    'Authorization': None,
    'Content-Type': 'application/json'
}

def send_message(content, channel_id, discord_token):

    user_id=discordtoken.get_token_id(discord_token)
    api=config['API_URL']
    url=f'{api}/channels/{channel_id}/messages'

    data={ 'content': content }
    data=JSON.dumps(data)

    headers=HEADERS
    headers['Authorization'] = discord_token
    
    r=requests.post(url, data=data, headers=headers)

    if r.status_code!=200:
        if r.status_code==429:

            retry_after=r.json()['retry_after']
            globals.log.logger(f'{user_id}(user id) was rate limited for {retry_after}s')

            time.sleep(retry_after)
            globals.log.logger(f'{retry_after}s rate limit has been lifted')

            return send_message(content, config.channel_id, discord_token)

        globals.log.logger(f'bad status code: '+str(r.status_code))
        return None

    return r.json()

globals.log.logger('methods defined')

if len(tokens)==0:
    tokensFile=config['TOKENS_FILE']
    globals.log.logger(f'{tokensFile} is empty!', error=True)

tokens=discordtoken.check_tokens(tokens)

globals.log.logger('tokens checked')

while True:

    for token in tokens:

        user_id=discordtoken.get_token_id(token)
        json=send_message(config['MESSAGE_CONTENT'], config['CHANNEL_ID'], token)
        if json==None:
            globals.log.logger(f'could not send message with user: '+user_id)
            continue
        
        content=json['content']
        username=json['author']['username']

        globals.log.logger(f'sent "{content}" as "{username}"')
    
    # time.sleep(.2)

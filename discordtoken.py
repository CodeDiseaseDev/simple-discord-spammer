import base64
import globals

log=globals.log

def get_token_id(discord_token):

    broken_token=discord_token.split('.')
    b64_id=broken_token[0]

    b64_id_b=b64_id.encode('ascii')
    id_b=base64.b64decode(b64_id_b)

    return id_b.decode('ascii')

def check_tokens(tokens:list):
    log.logger('checking token IDs')
    new_tokens=[]
    for token in tokens:
        try:
            id = get_token_id(token)
            log.logger(f'{id}(user id) has a valid token')
            new_tokens.append(token)
        except Exception:
            log.logger(f'{token}(token) is most likely fake')
            continue
    return new_tokens

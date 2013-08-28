from twython import Twython

APP_KEY = 'CVP4Tgh3FZahPl6wVSf6NQ'
APP_SECRET = 'aYbYRnYjbtDzJjTWsqjp10vKbxzSrB46CnuQtwZMI'
OAUTH_TOKEN = '76013996-9XJdUtMi78dQ3OiFIBuXqziNDVwBK6B1noh4eUu5w'
OAUTH_TOKEN_SECRET = 'BoihAhEBpydRZJGB5RsUPTPrKTxTzW3Fejr88MFl0'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

r= twitter.get_user_timeline(screen_name='ESPN')

print '\n---------\n'.join([x.get('text').encode('utf-8') for x in r]) 


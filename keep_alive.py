from flask import Flask
from threading import Thread
import random


app = Flask('')

@app.route('/')
def home():
	return '''
  <!DOCTYPE html>
<html>
<head>
<!-- HTML Codes by Quackit.com -->
<title>
Matt Bot</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="TFT Discord Bot">
<style>
body {background-color:#ffffff;background-image:url(https://d1lss44hh2trtw.cloudfront.net/assets/article/2019/05/13/discord-has-amassed-over-250-million-users-in-four-years_feature.jpg);background-repeat:no-repeat;background-position:top left;background-attachment:fixed;}
h1{font-family:Impact, sans-serif;font-variant:small-caps;color:#000000;background-color:#ffffff;}
p {font-family:Georgia, serif;font-size:14px;font-style:normal;font-weight:normal;color:#000000;background-color:#ffffff;}
</style>
</head>
<body>
<h1>DISCORD BOT</h1>
<p>This discord bot was made for the TFT Good discord server. Contact 7Teen#8897 for more info!</p>
</body>
</html>
'''

def run():
  app.run(
		host='0.0.0.0',
		port=random.randint(2000,9000)
	)

def keep_alive():
	'''
	Creates and starts new thread that runs the function run.
	'''
	t = Thread(target=run)
	t.start()
import requests
import json
import re
from flask import Flask, Response
from feedgen.feed import FeedGenerator
from markdown import markdown

app = Flask(__name__)

@app.route('/atom.xml')

def rss_feed():
    response = requests.get('https://home-backend-production.up.railway.app/posts')
    posts = json.loads(response.text)

    feed_gen = FeedGenerator()
    feed_gen.id('https://home-backend-production.up.railway.app')
    feed_gen.title('khh.log')
    feed_gen.author({'name':'kuohuanhuan', 'email':'hi@nekohuan.cyou'})
    feed_gen.link(href='https://home-backend-production.up.railway.app/atom.xml', rel='self')
    feed_gen.description('$ cat ./khh.log')
    feed_gen.language('zh-Hant-TW')

    for post in posts:
        feed_ent = feed_gen.add_entry()
        feed_ent.id(post['FileName'])
        feed_ent.title(post['Title'])
        feed_ent.content(re.sub(r'\s+', ' ', markdown(post['Content'], output_format='html')))
        feed_ent.description(re.sub(r'\s+', ' ', markdown(post['Content'][:80] + '...')))
        feed_ent.link(href='https://nekohuan.cyou/post/'+ post['FileName'])

    rss_feed = feed_gen.rss_str()
    return Response(rss_feed, mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)

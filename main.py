import os
import requests
import json
import re
from flask import Flask, Response
from feedgen.feed import FeedGenerator
from markdown import markdown

app = Flask(__name__)

@app.route('/atom.xml')

def rss_feed():
    response = requests.get(
        'https://nekohuan.cyou/api/posts/yes',
        headers = {
            "Authorization": f"token {os.environ['GH_PAT']}",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; vivo 1919) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 Mobile Safari/537.36 Vivaldi/5.3.2683.49"
        }
    )
    posts = json.loads(response.text)

    feed_gen = FeedGenerator()
    feed_gen.id('https://nekohuan.cyou')
    feed_gen.title('khh.log')
    feed_gen.author({'name': 'kuohuanhuan', 'email': 'hi@nekohuan.cyou'})
    feed_gen.link(href='https://nekohuan.cyou', rel='self')
    feed_gen.description('$ cat ./khh.log')
    feed_gen.language('zh-Hant-TW')
    feed_gen.ttl(60)

    for post in posts:
        feed_ent = feed_gen.add_entry()
        feed_ent.id(post['slug'])
        feed_ent.title(post['title'])
        feed_ent.content(re.sub(r'\s+', ' ', markdown(post['content'], output_format='html')))
        feed_ent.description(post['description'])
        feed_ent.link(href='https://nekohuan.cyou/post/'+ post['slug'])
        feed_ent.pubDate(post['datetime'] + '+0800')

    rss_feed = feed_gen.rss_str(pretty=True)
    return Response(rss_feed, headers={'Content-Type': 'application/rss+xml, application/xml'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)

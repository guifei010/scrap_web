import requests
import json
import re
from urllib.parse import urlencode


def get_query_arg(word, start_pos=0):
    """

    Args:
        word: 需要查询的关键词
        start_pos: 翻页的位置.

    Returns:

    """
    return urlencode({
        'q': word,
        '1': start_pos,
        'imgfile': '',
        'js': 1,
        'ie': 'utf8',
    })


def query_taobao_page(word, pos):
    url = 'https://s.taobao.com/search?'
    req = requests.get(url + get_query_arg(word, pos))
    match_regex = re.compile(r"^\s*g_page_config.+?(?P<js_data>\{.+\})[^\}]*$")
    for line in req.text.split('\n'):
        # 使用正则表达式提取结果。
        m = match_regex.match(line)
        if m:
            return json.loads(m.groupdict().get('js_data'))


def get_taobao(word):
    pos = 1
    while True:
        result = query_taobao_page(word, pos)
        items = result.get('mods', {}).get('itemlist', {}).get('data', {}).get('auctions', [])
        for item in items:
            yield item

"""
if __name__ == '__main__':
    for i, item in enumerate(get_taobao("笔记本")):
        if i > 20:
            break
        print(item)
        print("-"*20+item.get('title')+'-'*20)
        for k in ['pic_url', 'view_price', 'item_loc', 'nick', 'view_sales']:
            print(k, ":", item.get(k))
"""

if __name__ == '__main__':
    for i, item in enumerate(get_taobao("笔记本")):
        if i > 20:
            break
        print('******************')
        # print(item)
        title = item.get('title')
        # 把名字中的<span class=H>和</span>换成空
        title = title.replace('<span class=H>', "").replace('</span>', "")
        view_price = item.get('view_price')
        comment_count = item.get('comment_count')
        view_sales = item.get('view_sales')
        nick = item.get('nick')
        shopLink = item.get('shopLink')
        print('名称：%s\n价格：%s\n评论数：%s\n购买人数：%s\n店铺名称：%s\n店铺链接：%s\n' % (title, view_price, comment_count, view_sales, nick, shopLink))
        # print("名称:"+item.get('title'))
        # for k in ['pic_url', 'view_price',  'comment_count', 'item_loc', 'nick', 'view_sales']:
        #     print(k, ":", item.get(k))


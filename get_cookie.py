import redis, requests, json, time
from gl import headers
from do_login import login_info
from requests.exceptions import SSLError as rsle
from requests.packages.urllib3.exceptions import SSLError as rpuese
from ssl import SSLEOFError as sse


def store_cookie():
    cookie_dict = login_info.get_session()['cookie']
    r = redis.Redis(host='localhost', port=6379, db=0)
    cookiestr = json.dumps(cookie_dict)
    r.set('userinfo_cookie', cookiestr)


def get_cookie():
    r = redis.Redis(host='localhost', port=6379, db=0)
    return json.loads(r.get('userinfo_cookie').decode('utf-8'))


def get_session(q):
    while True:
        try:
            session = login_info.get_session()['session']
        except (sse, rsle, rpuese):
            # 预防因为网络问题导致的登陆不成功
            print('本次登陆出现问题')
            time.sleep(60)
            session = login_info.get_session()['session']
        finally:
            q.put(session)
            # session24小时过期
            time.sleep(23*60*60)


if __name__ == '__main__':
    store_cookie()
    cookie = get_cookie()
    content = requests.get('http://weibo.com/p/1005051921017243/info?mod=pedit_more', cookies=cookie, headers=headers).text
    print(content)

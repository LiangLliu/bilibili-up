import requests
import time
import json
import random

url = "https://api.bilibili.com/x/click-interface/click/web/h5"
get_bvid_url = "https://api.bilibili.com/x/space/arc/search"

sleep_time_seconds = 3
sleep_time_seconds_random = 7
exception_sleep_time_seconds = 100
count = 0

# page
pn = 1
ps = 50

user_id = ""


def init_config():
    with open("user-config.json") as json_file:
        config = json.load(json_file)
    print(config["userId"])
    global user_id
    user_id = config["userId"]


def get_bvids_with_mid(mid):
    response = requests.get(get_bvid_url, params={
        'mid': mid, "pn": pn, "ps": ps})

    ss = json.loads(response.text)
    print("\nRequest Code: %s, message %s" % (ss["code"], ss["message"]))
    print("---------video list---------------")
    video_bvids = []
    vlist = ss["data"]["list"]["vlist"]
    for item in vlist:
        print(item["bvid"])
        video_bvids.append(item["bvid"])
    return video_bvids


def get_request_data(bvid):
    response = requests.get(
        "https://api.bilibili.com/x/web-interface/view", params={'bvid': bvid})

    ss = json.loads(response.text)
    print("\nRequest Code: %s, message %s" % (ss["code"], ss["message"]))
    stime = str(int(time.time()))

    # 请求 https://api.bilibili.com/x/web-interface/view?bvid=bvid 获取

    request_data = {
        'aid': (ss["data"]["aid"]),
        'cid': (ss["data"]["cid"]),
        "bvid": bvid,
        'part': '1',
        'mid': (ss["data"]["owner"]["mid"]),
        'lv': '5',
        "stime": stime,
        'jsonp': 'jsonp',
        'type': '3',
        'sub_type': '0',
    }
    return request_data


def get_video_view_number(bvid):
    response = requests.get(
        "https://api.bilibili.com/x/web-interface/view", params={'bvid': bvid})
    resp = json.loads(response.text)
    view_number = resp["data"]["stat"]["view"]
    return view_number


def build_request_headers(bvid):
    # 首先先定义它的headers，在我们点击视频的时候，查看它的xhr，然后我们就可以找到它的对应cookie了，因为怎么获取播放量和cookie有关
    request_headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'origin': 'https://www.bilibili.com',
        'Connection': 'keep-alive',
        'referer': 'https://www.bilibili.com/video/' + bvid,
        "cookie": "_uuid=3FE3CF83-B9E8-4146-0B1A-715E4448B57157957infoc; buvid3=643B48AA-19CF-4768-AFAC-E4C72BAE9512148806infoc; CURRENT_BLACKGAP=1; CURRENT_FNVAL=80; CURRENT_QUALITY=0; sid=iir8gxre; rpdid=|(J~J|R~JlRl0J'uYJlYuRRYk"
    }
    return request_headers


def request_video_with_bvid(bvid):
    request_data = get_request_data(bvid)
    request_headers = build_request_headers(bvid)
    requests.post(url, data=request_data, headers=request_headers)


def request_videos(video_bvids):
    index = 0
    for bvid in video_bvids:
        try:
            old_view = get_video_view_number(bvid)
            request_video_with_bvid(bvid)
            sleep_time = sleep_time_seconds + random.randint(0, sleep_time_seconds_random)
            time.sleep(sleep_time)
            current_view = get_video_view_number(bvid)
            print("bvid: %s , old view: %d ,sleep_time: %ds ,current view: %d . " %
                  (bvid, old_view, sleep_time, current_view), end='')
            if current_view > old_view:
                print("The view of current video increases by 1\n")
                index += 1
            else:
                print("The current video view failed")

        except Exception as e:
            print(e)
            time.sleep(exception_sleep_time_seconds)
            print('exception : over')
    print("\n--------The current request successful count : %d " % index)
    global count
    count += index
    print("--------Total Success: %d\n" % count)


if __name__ == '__main__':
    init_config()
    video_bvids = get_bvids_with_mid(user_id)
    for i in range(20):
        request_videos(video_bvids)
        time.sleep(exception_sleep_time_seconds)

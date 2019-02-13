import re
import json
from urllib import parse

import BiliUtil_old

if __name__ == '__main__':
    # 填写需要批量下载的频道的URL
    download_url = 'https://space.bilibili.com/4282930/channel/detail?cid=48758'
    input_info = parse.urlparse(download_url)
    uid = re.match('/([0-9]+)/channel/detail', input_info.path).group(1)
    cid = parse.parse_qs(input_info.query)['cid'][0]

    video_list, channel_info = BiliUtil_old.get_up_channel_video_list(uid, cid)
    print(json.dumps(video_list))
    print(json.dumps(channel_info))





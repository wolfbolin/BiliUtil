import json
import BiliUtil_old

if __name__ == '__main__':
    video_list = BiliUtil_old.get_up_all_video_list(4282930, BiliUtil_old.ORDER_LATEST)
    print(json.dumps(video_list))

    video_list, channel_info = BiliUtil_old.get_up_channel_video_list(4282930, 48758)
    print(json.dumps(video_list))
    print(json.dumps(channel_info))
    album_info = BiliUtil_old.get_album_info(28539522)
    print(json.dumps(album_info))

    cookies = 'LIVE_BUVID=AUTO7615456282276008; sid=4uhet93r; stardustvideo=1; CURRENT_FNVAL=16; buvid3=77229FB7-A6AF-4642-8E75-68861B31239185388infoc; rpdid=oqxiqwmllidospsmplmxw; im_notify_type_72835041=0; DedeUserID=72835041; DedeUserID__ckMd5=6a465e397aed100e; SESSDATA=868c68fd%2C1551761144%2C38d97521; bili_jct=03dace7dc83d3c0fcc4e6db9c37d419a; finger=17c9e5f5; bp_t_offset_72835041=219166301309039445; CURRENT_QUALITY=80; _dfcaptcha=a6ea81909e83b34a6c628c93fc970f99'

    video_info = BiliUtil_old.get_video_info(28539522, 49392241, cookies)
    print(json.dumps(video_info))

    BiliUtil_old.download_video(video_info)




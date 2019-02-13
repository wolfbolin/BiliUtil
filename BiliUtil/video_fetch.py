import os
import re
import subprocess

import BiliUtil_old.static_func as f
import BiliUtil_old.static_value as v


def download_video(video_info):
    if not os.path.exists(v.file_cache_path):
        os.makedirs(v.file_cache_path)

    if not os.path.exists(v.file_output_path):
        os.makedirs(v.file_output_path)

    # 完善下载信息
    referer = 'https://www.bilibili.com/video/av' + str(video_info['aid']['v'])

    # 使用两个进程分别下载视频和音频
    f.print_1('正在下载视频和配套音--av号：{}'.format(video_info['aid']['v']))
    audio_shell = "powershell aria2c -c -s 2 -o'{}/{}.aac' --referer={} '{}'"
    audio_process = subprocess.Popen(audio_shell.format(v.file_cache_path,
                                                        video_info['cid']['v'],
                                                        referer,
                                                        video_info['audio']['v']))

    video_shell = "powershell aria2c -c -s 2 -o'{}/{}.flv' --referer={} '{}'"
    video_process = subprocess.Popen(video_shell.format(v.file_cache_path,
                                                        video_info['cid']['v'],
                                                        referer,
                                                        video_info['video']['v']))

    audio_process.wait()
    video_process.wait()

    audio_cache_path = '{}/{}.aac'.format(v.file_cache_path, video_info['cid']['v'])
    video_cache_path = '{}/{}.flv'.format(v.file_cache_path, video_info['cid']['v'])
    if os.path.exists(audio_cache_path) and os.path.exists(video_cache_path):
        f.print_g('[OK]视频与配套音频下载成功--av号：{}'.format(video_info['aid']['v']))
    else:
        f.print_r('[ERR]视频或配套音频下载失败--av号：{}'.format(video_info['aid']['v']))
        raise BaseException('av{}下载失败'.format(video_info['aid']['v']))

    # # 转录合成完整视频
    # f.print_1('正在合成视频和配套音--av号：{}'.format(video_info['aid']['v']))
    # encode_shell = "ffmpeg -i {} -i {} {}/{}.mp4"
    # encode_process = subprocess.Popen(encode_shell.format(audio_cache_path,
    #                                                       video_cache_path,
    #                                                       v.file_output_path,
    #                                                       video_info['cid']['v']),
    #                                   stdout=subprocess.PIPE)
    #
    # for line in iter(encode_process.stdout.readline, b''):
    #     print(str(line, 'utf-8'))
    #
    # encode_process.wait()
    #
    # if os.path.exists('{}/{}.mp4'):
    #     f.print_g('[OK]目标视频合成成功--av号：{}'.format(video_info['aid']['v']))
    # else:
    #     f.print_r('[ERR]目标视频合成失败--av号：{}'.format(video_info['aid']['v']))
    # f.print_g('[OK]视频与配套音频下载完成--av号：{}'.format(video_info['aid']['v']))

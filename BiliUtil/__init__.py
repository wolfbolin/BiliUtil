# coding=utf-8
import os
import re
import warnings

from BiliUtil.bilibili_user import User
from BiliUtil.bilibili_album import Album
from BiliUtil.bilibili_channel import Channel
from BiliUtil.static_component import Quality
from BiliUtil.static_component import AutoLoad

_aria2c_result = os.popen('aria2c -v').read()
_aria2c_result = re.match(r'(\S+)', _aria2c_result)
_ffmpeg_result = os.popen('ffmpeg -version').read()
_ffmpeg_result = re.match(r'(\S+)', _ffmpeg_result)
if _aria2c_result is not None and _aria2c_result.group(1) == 'aria2':
    if _ffmpeg_result is not None and _ffmpeg_result.group(1) == 'ffmpeg':
        from BiliUtil.static_component import Downloader
    else:
        warnings.warn("(=・ω・=)您未配置ffmpeg渲染环境，Download类不可用")
else:
    warnings.warn("(=・ω・=)您未配置aria2c下载环境，Download类不可用")

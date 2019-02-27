import os
import re
_aria2c_result = os.popen('aria2c -v').read()
_aria2c_result = re.match(r'(\S+)', _aria2c_result)
if _aria2c_result is not None and _aria2c_result.group(1) == 'aria2':
    print('\033[0;32;0m{}\033[0m'.format(str('(=・ω・=)aria2c环境检查通过(=・ω・=)')))
    from .bili_album import Album
    from .bili_channel import Channel
    from .bili_user import User
else:
    print('\033[0;31;0m{}\033[0m'.format(str('(=・ω・=)您未配置aria2c下载环境(=・ω・=)')))

_ffmpeg_result = os.popen('ffmpeg -v').read()
_ffmpeg_result = re.match(r'(\S+)', _ffmpeg_result)
if _ffmpeg_result is not None and _ffmpeg_result.group(1) == 'ffmpeg':
    print('\033[0;32;0m{}\033[0m'.format(str('(=・ω・=)ffmpeg环境检查通过(=・ω・=)')))
    from .static_func import merge_video_file
else:
    print('\033[0;31;0m{}\033[0m'.format(str('(=・ω・=)您未配置ffmpeg渲染环境(=・ω・=)')))

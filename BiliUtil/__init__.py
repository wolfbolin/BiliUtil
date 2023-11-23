# coding=utf-8
from __future__ import annotations

import os
import re

from . import Util, Space
from .Space import User
from .Util import Config
from .Video import Album, Task

# 检查ffmpeg是否安装
ffmpeg_result = os.popen('ffmpeg -version').read()
if re.match(r'(\S+)', ffmpeg_result).group(1) != 'ffmpeg':
    raise RuntimeError('未安装ffmpeg')
# 检查aria2c是否安装
aria2c_result = os.popen('aria2c -v').read()
if re.match(r'(\S+)', aria2c_result).group(1) != 'aria2':
    raise RuntimeError('未安装aria2c')

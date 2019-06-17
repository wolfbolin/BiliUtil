import os
import subprocess
from urllib import parse
import BiliUtil.static_value as v
from fake_useragent import UserAgent


def print_0(message, end='\n'):
    print('\033[0;30;0m{}\033[0m'.format(str(message)), end=end)


def print_1(message, end='\n'):
    print('\033[0;37;0m{}\033[0m'.format(str(message)), end=end)


def print_r(message, end='\n'):
    print('\033[0;31;0m{}\033[0m'.format(str(message)), end=end)


def print_g(message, end='\n'):
    print('\033[0;32;0m{}\033[0m'.format(str(message)), end=end)


def print_y(message, end='\n'):
    print('\033[0;33;0m{}\033[0m'.format(str(message)), end=end)


def print_b(message, end='\n'):
    print('\033[0;34;0m{}\033[0m'.format(str(message)), end=end)


def print_cyan(message, end='\n'):
    # 青色
    print('\033[0;36;0m{}\033[0m'.format(str(message)), end=end)


def print_gray(message, end='\n'):
    # 灰色
    print('\033[0;37;0m{}\033[0m'.format(str(message)), end=end)


def new_http_header(url, ref='https://www.bilibili.com'):
    header = v.HTTP_HEADER.copy()
    header['Host'] = parse.urlparse(url).netloc
    header['User-Agent'] = UserAgent().random
    header['Referer'] = ref
    return header


def merge_video_file(path, delete=False):
    # 完成目录下flv视频文件与aac音频文件的合并
    if os.path.exists(path) and os.path.isdir(path):
        path = os.path.abspath(path)  # 将路径替换为绝对路径
        file_list = os.listdir(path)  # 获取路径下文件列表
        for file in file_list:
            file_path = path + '\\' + file
            file_name = os.path.splitext(file)[0]
            prefix, suffix = os.path.splitext(file_path)
            if suffix == '.flv':
                if os.path.exists(prefix + '.aac'):
                    print_b('已找到未合并文件{}，正在合并'.format(file_name))
                    shell = 'ffmpeg -i "{}.flv" -i "{}.aac" -c copy -f mp4 -y "{}.mp4"'
                    process = subprocess.Popen(shell.format(prefix, prefix, prefix),
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE,
                                               shell=True)
                    process.communicate()
                    if os.path.exists(prefix + '.mp4'):
                        print_1('视频', end='')
                        print_cyan(file_name, end='')
                        print_1('已经', end='')
                        print_g('完成合并', end='')
                        if delete:
                            os.remove(prefix + '.flv')
                            os.remove(prefix + '.aac')
                            print_1('，原始音视频', end='')
                            print_r('已删除')
                        else:
                            print_1('，原始音视频', end='')
                            print_y('未删除')
                    else:
                        raise BaseException('视频与音频合并失败，不知道发生了什么')
                else:
                    raise BaseException('未找到与视频匹配的音频!!!')
            elif suffix == '.mp4':
                print_1('视频', end='')
                print_cyan(file_name, end='')
                print_1('已找到，跳过该文件')
    else:
        raise BaseException('输入的文件夹路径不存在')

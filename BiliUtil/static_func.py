from urllib import parse
import BiliUtil_old.static_value as v
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


def new_http_header(url):
    header = v.HTTP_HEADER.copy()
    header['Host'] = parse.urlparse(url).netloc
    header['User-Agent'] = UserAgent().random
    return header

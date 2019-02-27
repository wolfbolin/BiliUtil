import os
import BiliUtil


def open_dir(path):
    path = os.path.abspath(path)
    # 扫描当前文件夹
    BiliUtil.merge_video_file(path, True)
    # 递归搜索文件夹
    file_list = os.listdir(path)
    for file in file_list:
        file_path = path + '\\' + file
        if os.path.isdir(file_path):
            open_dir(file_path)


if __name__ == '__main__':
    print('即将扫描下载目录并合并分离的音视频')
    base_path = './Download'
    open_dir(base_path)

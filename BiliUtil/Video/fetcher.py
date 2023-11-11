# coding=utf-8
from __future__ import annotations
import os
from typing import Optional, List, Union, Tuple, Dict, Any
from .. import Util
from ..Space.channel import Channel
from ..Space.user import User
from ..Video import Video, Album, Task


def get_album(info: Dict[str, Tuple[str, Union[User, Channel, Album, Video]]]) -> Album:
    return info['album'][1]


class Fetcher:
    def __init__(self, obj: Union[User, Channel]):
        self.obj = obj
        self.info_list: Optional[List[Dict[str, Tuple[str, Union[User, Channel, Album, Video]]]]] = None
        self.task_list: Optional[List[Task]] = None
        self.exist_list: Optional[List[str]] = None

    async def fetch_av_list(self, name_pattern: int = Util.Config.SET_AS_CODE,
                            quality: Optional[int] = None, count: int = Util.FetchConfig.ALL) -> List[str]:
        av_list = []
        self.info_list = []

        if isinstance(self.obj, User):
            obj_code = self.obj.uid
        elif isinstance(self.obj, Channel):
            obj_code = self.obj.cid
        else:
            raise Util.ParameterError('该类型对象无法自动加载')

        if name_pattern == Util.Config.SET_AS_CODE:
            obj_name = obj_code
        elif name_pattern in [Util.Config.SET_AS_NAME, Util.Config.SET_AS_PAGE]:
            await self.obj.sync()
            obj_name = Util.legalize_name(self.obj.name)
        else:
            obj_name = "unknown"

        album_list = await self.obj.get_album_list(count=count)
        for album in album_list:
            await album.sync()
            if album.is_upower_exclusive is True:  # 充电专属稿件跳过
                continue
            album_name = album.album_name(name_pattern)
            video_list = await album.get_video_list()
            for video in video_list:
                await video.sync(quality)
                video_name = video.video_name(name_pattern)

                self.info_list.append({
                    'obj': (obj_name, self.obj),
                    'album': (album_name, album),
                    'video': (video_name, video)
                })
                av_list.append(album.aid)
        av_list = list(set(av_list))
        return av_list

    def load_task(self, output: str, exclude: Optional[List[str]] = None,
                  v_filter: Optional[Any] = None) -> List[str]:
        task_list = []
        self.task_list = []
        base_path = os.path.abspath(output)
        exclude = [str(item) for item in exclude or []]

        for info in self.info_list:
            if get_album(info).aid in exclude:
                continue
            elif v_filter is not None and v_filter.check_video(info['video'][1]):
                continue

            full_path = os.path.join(base_path, info['obj'][0], info['album'][0])
            self.task_list.append(Task(info['video'][1], full_path, info['video'][0], info['album'][1].cover))
            task_list.append(get_album(info).aid)

        task_list = list(set(task_list))
        return task_list

    def load_exist(self, output: str) -> Tuple[List[str], List[str]]:
        all_video_list = []
        positive_list = []
        negative_list = []
        base_path = os.path.abspath(output)

        for info in self.info_list:
            all_video_list.append(get_album(info).aid)
            video_path = os.path.join(base_path, info['obj'][0], info['album'][0], '{}.mp4'.format(info['video'][0]))
            if os.path.exists(video_path):
                positive_list.append(get_album(info).aid)
            else:
                negative_list.append(get_album(info).aid)

        all_video_list = set(all_video_list)
        positive_list = list(set(positive_list))
        negative_list = list(all_video_list - set(negative_list))

        return positive_list, negative_list

    def pull_all(self, show_process: bool = True, no_repeat: bool = True):
        av_list = []
        for task in self.task_list:
            av_list.append(task.start(show_process, no_repeat))

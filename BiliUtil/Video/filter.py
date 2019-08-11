# coding=utf-8
import BiliUtil.Util as Util


class Filter:
    def __init__(self, quality=None, length=None, height=None, width=None, page=None, ratio=None):
        self.quality = quality
        self.length = length
        self.height = height
        self.width = width
        self.page = page
        self.ratio = ratio

    def set_quality(self, quality):
        if ~isinstance(quality, list):
            raise Util.ParameterError('参数类型异常')
        self.quality = quality

    def set_length(self, length):
        if ~isinstance(length, list):
            raise Util.ParameterError('参数类型异常')
        self.length = length

    def set_height(self, height):
        if ~isinstance(height, list):
            raise Util.ParameterError('参数类型异常')
        self.height = height

    def set_width(self, width):
        if ~isinstance(width, list):
            raise Util.ParameterError('参数类型异常')
        self.width = width

    def set_page(self, page):
        if ~isinstance(page, list):
            raise Util.ParameterError('参数类型异常')
        self.page = page

    def set_ratio(self, ratio):
        if ~isinstance(ratio, list):
            raise Util.ParameterError('参数类型异常')
        self.ratio = ratio

    def check_video(self, video):
        """
        当响应值为True时，说明该视频超出接受范围，视频需要被过滤
        :param video: 被监测视频
        :return: 检测响应
        """
        if self.quality and video.quality not in self.quality:
            return True
        if self.length and (video.length / 1000 < self.length[0] or self.length[1] < video.length / 1000):
            return True
        if video.level == 'new_version':
            if self.height and (video.height < self.height[0] or self.height[1] < video.height):
                return True
            if self.width and (video.width < self.width[0] or self.width[1] < video.width):
                return True
            ratio = video.width / video.height
            if self.ratio and (ratio < self.ratio[0] or self.ratio[1] < ratio):
                return True
        if self.page and video.page not in self.page:
            return True
        return False

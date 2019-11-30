# BiliUtil

![Windows](https://img.shields.io/badge/Windows-support-green.svg)
![Linux](https://img.shields.io/badge/Linux-testing-orange.svg)
![License](https://img.shields.io/badge/License-MPL_2.0-orange.svg)
![Python](https://img.shields.io/badge/Python-3.7-blue.svg)
![Version](https://img.shields.io/badge/Version-2.x-blueviolet.svg)

Bilibili.com（B站）数据下载工具包。若您在使用过程中发现BUG或有可以改进之处，欢迎提交[Issue](https://github.com/wolfbolin/BiliUtil/issues)或邮件（mailto@wolfbolin.com）与我联系。如果觉得还不错，欢迎Star和Fork支持一下（一百个Star冲鸭）。



> 特性
>
> * 用户与频道内视频批量下载
> * 支持匿名至大会员画质下载
> * 开放灵活详细的API编程接口
>* 视频分块多链接下载与自动合成



常见问题请参考[Q&A](#qa)  | BUG修复请参考[更新日志](#update)



###### TOC

一、[安装方式](#install)

二、[使用样式](#example)

三、[接口文档](#document)

四、[Q&A](#qa)

五、[关于BiliUtil](#about)

六、[更新日志](#update)





## 一、安装方式<span id="install"/>

本工具包采用pip方式发布，并需要调用本地aria2c与ffmpeg插件，工具包启动前将根据环境变量检查环境是否可用，当环境中缺少相关插件时，部分类将不会导入。

*Step 1*: 使用pip安装

```shell
pip install BiliUtil
```

*Step 2*: 安装Aria2c插件

插件官网：<https://aria2.github.io/>

*Step 3:* 安装FFmpeg插件

插件官网：<https://ffmpeg.org/>

## 二、使用样例<span id="example"/>

获取视频信息并下载视频

```python
import BiliUtil
if __name__ == '__main__':
    album = BiliUtil.Album(3947271)
    # album.set_album(3947271)
    # album.set_by_url("https://www.bilibili.com/video/av3947271")
    album_info = album.sync()
    print(album_info)
    video_list = album.get_video_list()
    for video in video_list:
        video.sync(cookie="SESSDATA=abcd68fd...")
        task = BiliUtil.Task(video, 'D:/BiliUtil', album.aid)
        task.start()
```

获取用户信息并下载所有视频

```python
import BiliUtil
if __name__ == '__main__':
    cookie = "SESSDATA=abcd68fd..."
    cache = "D:/BiliUtil"

    user = BiliUtil.User(20165629)
    # user.set_user(user)
    # user.set_by_url("https://space.bilibili.com/20165629")
    user_info = user.sync()
    print(user_info)

    fetcher = BiliUtil.Fetcher(user)
    av_list = fetcher.fetch_all(cookie, BiliUtil.Config.SET_AS_NAME)
    print(av_list)

    positive_list, negative_list = fetcher.load_exist(cache)
    print(positive_list)
    print(negative_list)

    task_id = fetcher.load_task(cache, positive_list, cache)
    download_list = fetcher.pull_all()
    print('完成{}个视频下载：{}'.format(len(download_list), download_list))

```



高配版示例程序请见[example3.py](https://github.com/wolfbolin/BiliUtil/blob/master/example3.py)和[example4.py](https://github.com/wolfbolin/BiliUtil/blob/master/example3.py)，其中example4.py是我个人自测自用程序，涉及大多数使用场景，可靠性与适用性MAX



## 三、接口文档<span id="document"/>

在第四章[Q&A](#四QA)中将讲解常见问题与逻辑结构，如有需要请移步第四章，那里可能有你想问的。本章仅讲解工具包的使用方法，简单粗暴便于理解。

### 0、常量与含义<span id="config"/>

常量中包含了文件命名方式的定义，画质信息的定义，全局代理设置的定义等内容。

| 常量             | 值                               | 含义            |
| ---------------- | -------------------------------- | --------------- |
| 命名方式         |                                  |                 |
| SET_AS_NAME      | 1                                | 以视频名称命名  |
| SET_AS_CODE      | 2                                | 以对象编号命名  |
| SET_AS_PAGE      | 3                                | 以分P文件命名   |
| 网络代理         |                                  |                 |
| HTTP_PROXY       | 例http://user:pass@1.2.3.4:5678  | HTTP代理设置    |
| HTTPS_PROXY      | 例https://user:pass@1.2.3.4:5678 | HTTPS代理设置   |
| 视频画质         |                                  |                 |
| Quality.V360P    | ('16', '流畅 360P')              | 360P            |
| Quality.V480P    | ('32', '清晰 480P')              | 480P            |
| Quality.V720P    | ('64', '高清 720P')              | 720P（登录）    |
| Quality.V720P60  | ('74', '高清 720P60')            | 720P60（会员）  |
| Quality.V1080P   | ('80', '高清 1080P')             | 1080P（登录）   |
| Quality.V1080Px  | ('112', '高清 1080P+')           | 1080P+（会员）  |
| Quality.V1080P60 | ('116', '高清 1080P60')          | 1080P60（会员） |
|                  |                                  |                 |



### 1、用户类（BiliUtil.User）<span id="userclass"/>

#### 1.1、`__init__(uid=None)`

你可以为每一个用户声明一个对象实例，在声明时你可以指定用户uid或在同步数据前设定用户uid。

``` python
user = BiliUtil.User('20165629')
```

每个实例中将包含以下成员变量，你可以在[`sync()`](#user-sync)操作后读取这些信息。

| 成员变   | 变量含义            |
| -------- | ------------------- |
| uid      | 用户uid             |
| name     | 用户昵称            |
| birthday | 用户生日            |
| title    | 用户身份            |
| face     | 用户头像            |
| time     | 创号时间（可能为0） |
| level    | 用户级别            |
| sex      | 用户性别            |
| sign     | 用户签名            |
| vip      | 大会员              |
|          |                     |

#### 1.2、`set_user(uid)`

你可以使用该函数设定用户uid或重新指定用户uid。该操作不会重置成员变量。

```python
user.set_user('20165629')
```

#### 1.3、`set_by_url(url)`

你可以通过该函数以url解析的方式指定对象的用户uid。该操作不会重置成员变量。

```python
user.set_by_url('https://space.bilibili.com/20165629?from=search')
```

#### 1.4、`sync(cookie=None)`<span id="user-sync"/>

你可用通过该操作更新对象的成员变量，如果你感觉信息不够丰满，请与开发者联系。

```python
user_info = user.sync(cookie='SESSDATA=abcd68fd...')
```

#### 1.5、`get_channel_list(cookie=None)`

你可以通过该操作获取用户公开的全部频道，返回值中将储存本工具包中[频道类](#channelclass)的对象。

```python
channel_list = user.get_channel_list(cookie='SESSDATA=abcd68fd...')
```

#### 1.6、`get_album_list(cookie=None)`

你可以通过该操作获取用户公开的全部视频，返回值中将储存本工具包中[专辑类](#albumclass)的对象。

```python
get_album_list(cookie='SESSDATA=abcd68fd...')
```



### 2、频道类（BiliUtil.Channel）<span id="channelclass"/>

#### 2.1、`__init__(uid=None, cid=None)`

你可以为每一个用户声明一个对象实例，在声明时你可以指定用户uid、频道cid或在同步数据前设定用户uid、频道cid。

```python
channel = BiliUtil.Channel(uid='20165629', cid='9108')
```

每个实例中将包含以下成员变量，你可以在[`get_album_list()`](#channel-get_album_list)操作后读取这些信息。


| 成员变量   | 变量含义           | 默认值 |
| ---------- | ------------------ | ------ |
| uid        | 用户uid            | None   |
| cid        | 频道cid            | None   |
| name       | 频道名称           | None   |
| cover      | 频道封面           | None   |
| count      | 频道内专辑数量     | None   |
|            |                    |        |

#### 2.2、`set_channel(uid, cid)`

你可以使用该函数设定频道cid或重新指定频道cid，同时必须指定频道对应用户uid。该操作不会重置成员变量。

```python
channel.set_channel('20165629', '9108')
```

#### 2.3、`set_by_url(url)`

你可以通过该函数以url解析的方式指定对象的用户uid和频道cid。该操作不会重置成员变量。

```python
channel.set_by_url('https://space.bilibili.com/20165629/channel/detail?cid=9108')
```

#### 2.4、`get_album_list(cookie=None)`<span id="channel-get_album_list"/>

你可用通过该操作获取该频道中的全部专辑对象，返回值中将储存本工具包中[专辑类](#albumclass)的对象。

```python
channel_info = channel.get_album_list(cookie='SESSDATA=abcd68fd...')
```



### 3、专辑类（BiliUtil.Album）<span id="alnbumclass"/>

#### 3.1、`__init__(aid=None)`

你可以为每一个专辑声明一个对象实例，在声明时你可以指定专辑aid（av号），或者同步数据前设定专辑aid（av号）。关于专辑与视频的区别请参考[Q&A](#qa)加强对名词的理解。

```python
album = BiliUtil.Album('3947271')
```

每个实例中将包含以下成员变量，你可以在[`sync()`](#album-sync)操作后读取这些信息。

| 成员变量 | 变量含义        | 默认值 |
| -------- | --------------- | ------ |
| aid      | 专辑aid（av号） | None   |
| num      | 包含视频数量    | None   |
| type     | 分区名称        | None   |
| cover    | 封面链接        | None   |
| name     | 视频名称        | None   |
| time     | 发布时间        | None   |
| desc     | 专辑描述        | None   |
| view     | 观看人数        | None   |
| danmu    | 弹幕数量        | None   |
| reply    | 回复数量        | None   |
| favorite | 收藏数量        | None   |
| coin     | 硬币数量        | None   |
| share    | 分享数量        | None   |
| like     | 点赞数量        | None   |
| cid_list | 视频cid编号列表 | None   |
|          |                 |        |

#### 3.2、`set_album(aid)`

你可以使用该函数设定专辑aid或重新指定专辑aid，该操作不会重置成员变量。

```python
album.set_user('3947271')
```

#### 3.3、`set_by_url(url)`

你可以通过该函数以url解析的方式指定对象的专辑aid，该操作不会重置成员变量。

```python
album.set_by_url('https://www.bilibili.com/video/av3947271')
```

#### 3.4、`album_name(name_pattern=Util.Config.SET_AS_CODE)`

你可以通过该操作获取标准化的专辑名称，同时你可以通过参数的方式生成不同命名方式的名称

```python
album_name = album.album_name()
```

#### 3.5、`sync(cookie=None)`<span id="album-sync"/>

你可用通过该操作更新对象的成员变量，如果你感觉信息不够丰满，请与开发者联系。

```python
album_info = album.sync(cookie='SESSDATA=abcd68fd...')
```

#### 3.6、`get_video_list(cookie=None)`<span id="album-get_video_list"/>

你可以通过该操作获取每个专辑中的视频对象，返回值中将储存本工具包中视频类的对象。

```python
get_video_list(cookie='SESSDATA=abcd68fd...')
```

### 4、视频类（BiliUtil.Video）<span id="videoclass"/>

#### 4.1、`__init__(aid=None, cid=None)`

不建议使用者自行创建视频对象，请使用专辑类的[`get_video_list()`](#album-get_video_list)操作获取视频类对象实例列表。

每个实例中将包含以下成员变量，你可以在[`sync()`](#video-sync)操作后读取这些信息。

| 成员变量 | 变量含义            | 默认值 |
| -------- | ------------------- | ------ |
| album      | 专辑对象     | None   |
| cid      | 视频cid             | None   |
| name     | 视频名称（分P名称） | None   |
| page     | 视频编号（分P序号） | None   |
| quality  | 视频画质            | None   |
| length   | 视频长度            | None   |
| format   | 视频格式            | None   |
| height   | 视频高度            | None   |
| width    | 视频宽度            | None   |
| level    | 视频版本            | None   |
| video    | 视频链接            | list() |
| audio    | 视频链接            | list() |
|          |                     |        |

#### 4.2、`video_name(name_pattern=Util.Config.SET_AS_CODE)`

你可以通过该操作获取标准化的视频名称，同时你可以通过参数的方式生成不同命名方式的名称

```
video_name = video.video_name(Util.Config.SET_AS_PAGE)
```

#### 4.3、`sync(cookie=None， quality=None)`<span id="video-sync"/>

你可用通过该操作更新对象的成员变量，如果你感觉信息不够丰满，请与开发者联系。

你可以在同步视频信息时选择需要获取的视频画质，如果不指定，将默认按照可获取到的最高画质获取信息。

最高画质的获取与传入的Cookie信息有密切联系，有关Cookie与画质的关系请查阅[Q&A](#qa)

```python
video_info = video.sync(
    cookie='SESSDATA=abcd68fd...', 
    quailty=BiliUtil.Config.Quality.V1080P
)
```

## 5、抓取器（BiliUtil.Fetcher）<span id="fetcherclass"/>

该类的设计是针对有批量下载视频需求而设计，避免使用者自行完成所有下载流程的编写。请关注该类的使用流程与使用示例，奇怪的使用方式可能会触发不知道什么情况的BUG。

#### 5.1、`__init__(obj)`

你可以使用用户类或频道类来初始化一个抓取器对象实例，不建议开发者操作实例中的对象数据。

#### 5.2、`fetch_all(cookie=None, name_pattern=SET_AS_CODE, quality=None)`

请在初始化之后使用该函数获取对象名下所有的视频列表，并储存在对象内部变量中，为后续操作提供数据。

当初始化对象为用户类时，将自动获取用户名下的所有视频。当初始化对象为频道类时，将自动获取该频道中的所有视频。当文件命名[命名方式](#config)为以名字命名时(`SET_AS_NAME`)，程序将自动调用视频对象的`sync()`函数获取该视频的名称。你还可以传入视频质量的枚举以调整视频的最高质量，若无该参数则按照最高视频质量下载。

#### 5.3、`load_exist(ouput)`

你可以使用该函数加载输出目录中已经存在的视频列表，返回值分为乐观策略和悲观策略。在乐观策略状态下专辑实例有存在视频即认为存在， 在悲观策略状态下专辑实例所有视频都存在才认为存在。

该函数的设计是为了避免在视频下载时程序重复下载视频浪费流量与时间，也避免过多请求被官方风控。

#### 5.4、`load_task(output, exclude=None, v_filter=None)`

该函数可以帮助你在抓取器对象中生成一个任务列表，在任务列表中主要包含了任务类对象实例。

该函数提供了两个可选参数

* exclude：排除列表，当视频av号命中该列表中av号时，将自动跳过不创建下载任务。
* v_filter：过滤器，当专辑中的视频命中了过滤器的过滤条件时，将不创建下载任务。

#### 5.5、`pull_all(show_process=True, no_repeat=True)`

在一切都准备好之后，你可以调用该函数完成视频的批量下载，程序将自动调用每一个任务实例中的[`start()`函数](#taskstart)开始，函数的两个参数也将透传给任务对象。



### 6、任务类（BiliUtil.Task）<span id="tasklass"/>

#### 6.1、`__init__(video, output, name, cover=None)`

在初始化任务类时，需要传入一个视频对象，输出文件夹路径，封面链接与视频命名。如果你觉得非常麻烦，请使用抓取器自动生成单个视频的下载任务。

#### 6.2、`start(show_process=True, no_repeat=True)`<span id="taskstart"/>

该函数将启动任务的下载流程，程序将按照实例化对象时的参数调用Aria2c完成视频与封面的下载。

关于在视频下载流程中会发生什么，请参考[Q&A](#qa)中关于视频下载的相关解释。

函数提供两个可选参数

* show_process：是否显示下载进度，通过该参数可以控制是否显示Aria2c和FFmpeg工作流程的信息。
* no_repeat：是否重复下载，通过该参数可以控制遇到已存在视频是否跳过下载流程。



### 7、过滤器（BiliUtil.Filter）

#### 7.1、`__init__(quality=None, length=None, height=None, width=None, page=None, ratio=None)`

你可以初始化一个过滤器对象用于过滤批量下载过程中不符合条件的视频（部分参数仅针对新类型的视频有效）

该函数提供了多个可选参数

* quality：视频画质，请传入一个包含预制[画质](#config)类型的数组。（例：[BiliUtil.Config.Quality.V1080P,
                 BiliUtil.Config.Quality.V1080Px]）
* length：视频时长，请传入一个闭区间作为视频时长的判断标准（秒为单位）。（例：[40, 600]）
* height：视频高度，请传入一个闭区间作为视频高度的判断标准（px为单位）。（例：[720, 1080]）
* weight：视频宽度，请传入一个闭区间作为视频宽度的判断标准（px为单位）。（例：[720, 1080]）
* page：视频分P，请传入一个由数组组成的数组作为分P的判读依据（下标1开始）。（例：[1,  2]）
* ratio：视频比例，请传入一个闭区间作为视频比例的判断标准（比例->宽/高）。（例：[1, 2]）

#### 7.2、set_xxx()

你也可以使用set加对应参数名修改对象实例中的参数信息。



## 四、Q&A<span id="qa"/>

### 开发进度与缺陷

目前已完成开发的模块

* 用户信息获取与视频列表拉取
* 频道信息获取与视频列表拉取
* 专辑信息获取与视频列表拉取
* 视频信息获取
* 任务列表生成器
* 视频列表过滤器
* 已存视频检查器
* 新版多P视频下载与合成
* 旧版单视频下载与转换

目前尚存在缺陷的功能

* 旧版分段视频下载与合成

期望或将要开发的功能

* 视频弹幕获取与保存
* 视频评论获取与保存
* 远程视频缓存server

### 下载流程简单说明

使用者在下载的过程中一般遵循一下步骤：初始化对象-->获取视频对象-->创建任务-->开始下载

在创建任务的过程中，程序将处理视频的储存位置与下载后视频名称的问题，并将不同层级的对象统一转化为任务，将任务作为下载的最小单元，方便编程与管理。

在下载过程中，程序将主要处理文件夹的建立，封面的下载、音画下载与音画合并。其中在核心的下载过程中，程序将根据情况自动采用多线程多连接的下载方式，并且减少分片大小，相比于v1.x的速度有大幅提高，不再会产生挂机一晚也下载不到视频的情况。

### 暂不支持的功能整理

* [Issue#16](https://github.com/wolfbolin/BiliUtil/issues/16)：列举分区下所有视频
* [Issue#17](https://github.com/wolfbolin/BiliUtil/issues/17)：番剧的下载（版权与权限限制

### Cookie信息的获取与使用

- cookie信息不影响除视频画质外其他信息的获取。
- 通过cookie信息，你可以在下载视频的时候获取到更高清的视频数据，也可以手动指定视频清晰度。

- 设定cookie信息时，类似于`_uuid=B45CF1AB-xxx; LIVE_BUVID=AUTO76154xxx; SESSDATA=abcd68fd%2C1123761144%2C38d97xyz`的cookie信息也是可以被识别的。也可以传入字典类型的cookie信息，但是cookie信息中必须包含`SESSDATA`字段，该字段是提升视频质量的关键点。
- 不同的身份信息视频质量上限表：
  - 未登录--->480P
  - 已登录--->1080P
  - 大会员--->1080P60FPS / 1080P+
  
  - 关键的cookie存在与发往`*.bilibili.com`域下，发往其他域的请求中不包含该信息。至于如何在浏览器中获取Cookie，请移步：[如何在浏览器中获取Cookie](http://baidux.tinoy.cn/?q=%E5%A6%82%E4%BD%95%E5%9C%A8%E6%B5%8F%E8%A7%88%E5%99%A8%E4%B8%AD%E8%8E%B7%E5%8F%96Cookie)

### 什么是专辑Album和视频Video有什么区别？

首先说明这个专辑不是平时常说的唱片专辑，这个专辑是指包含了多个视频的一个集合，代表了用户的一次发布。

众所周知许多Up会上传多P，多P就对应了多个视频，因此一个av号可能会对应多个视频。所以在文档中我们不能再使用“视频”这个词汇来表达一个av号所对应的资源，因此便采用了“专辑”这个词汇来表达。

### 什么是uid、cid、aid？

我们需要为每一个资源做一个标记，官方也是这么做的。如果你真的经常使用B站，那么你一定知道UID为2的 **碧诗**和av号，本工具包沿用了B站的编号体系，不仅仅是用户与专辑，每一个频道与视频都是有他们自己的编号的。

### set_by_url有什么要求？

当我们打开了用户或视频时，URL中就已经包含了我们生成对象所需要的信息。在声明对象实例时，我们可以利用这些信息，由于不是使用正则进行匹配的，因此你可以随心所欲的拷贝URL，包括带有参数的URL都是可以接受的。但是，请确保传入的URL是与对象类型相匹配的，否则可能会导致程序运行异常。

### 为什么要用到FFmpeg？

在B站更新了数据下发形式后，你所观看的每一个视频都由纯视频和纯音频的形式下发，因此我们在下载之后需要使用工具将这些数据封装在一起。工具的使用方法我已经封装在代码中，默认会在视频下载结束后完成合并渲染。

### 新旧视频版本

目前视频的版本主要分为两种，由程序内部自动判断。对于旧版视频，因为在下载前无法获取视频的具体参数，因此不可使用过滤器中的部分功能，而且旧版视频音画是在同一个视频容器中，因此无需合并数据，但同时旧版视频仅支持单链接下载，没有多服务器下发的能力。视频的下载速度可能会受到影响。

### 画质分级与最高画质

根据B站的限制，拥有不同身份的用户能够看到的视频数据有所不同，因此在下载视频时应尽量使用有大会员的用户身份进行下载。否则，即使你咋程序中指定的是v1080Px也无法获取到该画质的视频。毕竟这个工具包不是搞大会员破解的。



**其他未尽适宜请提[Issue](https://github.com/wolfbolin/BiliUtil/issues)**



## 五、关于BiliUtil<span id="about"/>

这个包中还有很多未完成的细节，还有一些想实现的功能未完成。
欢迎有兴趣的小伙伴一次参与，反馈BUG，更新代码，提供方案，我们共同完善它。

你可以联系我：mailto@wolfbolin.com

**声明：该博客内容仅供学习参考，请勿用于商业目的**



## 六、更新日志<span id="update"/>

### v0.2.2

修复

* [Issue #24](https://github.com/wolfbolin/BiliUtil/issues/24) [PR #25](https://github.com/wolfbolin/BiliUtil/pull/25)缓存视频允许以分P名称命名视频
* [driverCzn](https://github.com/driverCzn) 提出的BUG，解决旧版视频下载一半后无法自动断点续传的检测策略问题

优化

* 代码结构与语法优化

缺陷

* [driverCzn](https://github.com/driverCzn) 提出但尚未解决的“旧版长视频分段下载”问题

### v0.2.1

修复

* [Issue #14](https://github.com/wolfbolin/BiliUtil/issues/14) API调整导致视频链接获取错误的BUG
* [Commit 351b07](https://github.com/wolfbolin/BiliUtil/commit/351b072100998e0b845da336a10b854710e10847) 修复视频画质设置中，先有鸡还是先有蛋的问题
* 删除部分开发无关的文件

### v0.2.0

新版发布

- 简化代码结构与文档长度，简化使用方式
- cookie直接透传至，管理cookie更方面
- 多连接小分片并行下载，提高下载成功率与速度
- 支持根据视频属性、视频分P过滤无需下载的视频
- 支持设定下载代理地址，让流量走一些神奇的通道

### v0.1.10

修复

- 修复了上一个版本在Linux平台上还是不能下载的Bug
- 修正了实例中的一些BUG
- 修正了文档锚定的错误写法

### v0.1.9

修复

- 修复了在Linux平台上相对路径错误导致的无法下载问题
- 添加了批量下载Up主的代码实例，在examples文件夹中。

### v0.1.8

修复

- 修复了严重的翻页BUG（之前版本get_all_video_info获取用户视频最多30个，程序出现了一些偏差）

### v0.1.7

修复

- get_xxx_info函数中vars函数运行异常
- 修改数据拷贝方式，防止数据被篡改
- 修改对象初始化方式，防止二次创建对象时异常
- 修正若干数据获取逻辑BUG

### v0.1.6

修复

- 修复exclude_list列表使用BUG

新增

- 为频道与用户对象添加获取已下载视频的AV号列表。
- 为专辑对象添加判断视频是否已下载的访问接口

### v0.1.5

新增

- 为频道与用户对象添加获取AV号列表函数。
- 允许在批量下载视频时，通过添加排除列表，过滤部分视频的下载。
- 为多个函数添加合适的响应值。

### v0.1.4

解决ffmpeg合成阶段程序卡死。由于pipe size的大小限制，导致程序在收到超过64kb的输出时，程序会卡死不动。修改process.wait()为process.communicate()以解决该问题。

### v0.1.3

操作失误导致pip中v0.1.2版本被删除，将以v0.1.3版本发布。建议更新至最新版本后再使用。

### v0.1.2

修改：

- 修复了`ffmpeg`环境检测不通过的BUG，因为使用了错误的语法。
- 移除了对powershell的支持，未来将在linux环境中测试。
- 修复了使用`aria2c`时的错误语法，解决自定义输出路径报错。
- 修改路径获取方案，相对路径传入后，将以绝对路径进行计算。

### v0.1.1

新增：

- 音视频合并函数
- 音视频批量合并代码示例

修改：

- 删除部分无意义的`(=・ω・=)`输出
- 调整aria2与ffmpeg环境检测机制

### v0.0.1

BiliUtil已经过基础测试，正式发布第一个版本，若要直接使用，请使用pip进行安装。

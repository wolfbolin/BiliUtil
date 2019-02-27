

# BiliUtil

![Windows](https://img.shields.io/badge/Windows-support-green.svg)![Linux](https://img.shields.io/badge/Linux-test-orange.svg)![Python](https://img.shields.io/badge/Python-3.6-blue.svg)![License](https://img.shields.io/badge/License-MPL_2.0-orange.svg)

Bilibili.com（B站）视频下载工具包

**声明：该内容仅供学习参考，请勿用于商业目的**

*帮助信息请看到[第三章](#help)，更新日志请看到[第四章](#changelog)*

## 一、安装方式

1. 请使用pip安装该包：`pip install BiliUtil`
2. 若使用视频下载功能，请自行安装配置`aria2`。
3. 若使用视频合并功能，请自行安装配置`ffmpeg`。

*工具包将自动检查**aria2**和**ffmpeg**环境，若任一环境不存在，所涉及的类与函数将不会被引入*



## 二、使用方式

包中封装了始终对象，“UP主”（User）、“频道”（Channel）、“专辑”（Album）和“视频”（User），前三个对象是可以声明的，但是“视频”对象（Video）不可独立声明。

### 1、用户类（User）

该类表示了一个UP主，当需要获取某位UP主信息或UP的视频时，可以选择创建该类的实例。



#### 1.1、成员变量

| 成员变量     | 变量含义            | 默认值 |
| ------------ | ------------------- | ------ |
| cookie       | 设置的cookie信息    | None   |
| uid          | 用户uid             | None   |
| name         | 用户昵称            | None   |
| birthday     | 用户生日            | None   |
| coin         | 用户硬币量          | None   |
| face         | 用户头像            | None   |
| time         | 创号时间（可能为0） | None   |
| level        | 用户级别            | None   |
| sex          | 用户昵称            | None   |
| sign         | 用户签名            | None   |
| album_list   | 用户视频对象列表    | list() |
| channel_list | 用户频道对象列表    | list() |
|              |                     |        |



#### 1.2、声明实例

你可以引入包并创建一个空的用户实例，空的用户实例不设置用户uid。

```python
import BiliUtil
if __name__ == '__main__':
	ua = BiliUtil.User()
```



#### 1.3、设定用户uid

你可以通过多种方式设定用户uid，详见下方案例。

```python
import BiliUtil
if __name__ == '__main__':
	# 方案一
	ua = BiliUtil.User(uid='4093899')
	# 方案二
	ua = BiliUtil.User()
	ua.set_user(uid='4093899')
	# 方案三
	ua = BiliUtil.User()
	ua.set_by_url(url='https://space.bilibili.com/4093899')
```

三种函数声明方式如下：

```python
def __init__(self, uid=None)
def set_user(self, uid)
def set_by_url(self, url)
```

**注**：使用URL设定用户时，类似于`https://space.bilibili.com/4093899/channel/index`的URL也可以被识别。



#### 1.4、设定Cookie

设定的cookie信息会影响到该实例及其包含的所有自动创建的对象。

```python
ua.set_cookie('SESSDATA=abcd68fd%2C1551761144%2C38d97xyz')
```

**注**：cookie设置的方式与意义详见第三章的解释。



#### 1.5、获取用户信息

在设定用户uid信息后，即可通过该函数获取用户的基础信息。

```python
import BiliUtil
if __name__ == '__main__':
	ua = BiliUtil.User(uid='4093899')
	ua.get_user_info()
```



#### 1.6、获取所有视频列表

你可以仅获取视频列表而不下载视频，该操作将自动帮你完成用户信息的获取。

```python
import BiliUtil
if __name__ == '__main__':
	ua = BiliUtil.User(uid='4093899')
	ua.get_all_video_info()
```



#### 1.7、获取所有视频数据

你可以直接下载UP主的全部视频，该操作将自动帮你完成**用户信息**的获取与**视频列表**的获取。该操作支持**设定路径、命名方式、视频时长**，当设置了适合的cookie时，下载的画质将会自动提升。

```python
import BiliUtil
if __name__ == '__main__':
	ua = BiliUtil.User(uid='4093899')
	ua.get_all_video_data(base_path='Download', name_path=True, max_length=None)
```

**注**：参数设置的方式与意义详见第三章的解释。



#### 1.8、获取频道列表

你可以仅获取频道列表而不下载视频，该操作将自动帮你完成用户信息的获取。

```python
import BiliUtil
if __name__ == '__main__':
	ua = BiliUtil.User(uid='4093899')
	ua.get_channel_video_info()
```



#### 1.9、获取频道视频数据

你可以直接下载UP主的全部视频，该操作将自动帮你完成**用户信息**的获取与**频道列表**的获取。该操作支持**设定路径、命名方式、视频时长**，当设置了适合的cookie时，下载的画质将会自动提升。

```python
import BiliUtil
if __name__ == '__main__':
	ua = BiliUtil.User(uid='4093899')
	ua.get_channel_video_data(base_path='Download', name_path=True, max_length=None)
```

**注**：参数设置的方式与意义详见第三章的解释。



#### 1.10、获取对象信息字典

你可以将当前对象中保存的所有信息转换为字典格式保存，修改该字典时并不会影响实例。

```python
import BiliUtil
if __name__ == '__main__':
	ua = BiliUtil.User(uid='4093899')
	ua.get_user_info()  # 修改对象
	print(ua.get_dict_info())  # 输出对象内部信息
	ua.get_all_video_info() # 修改对象
	print(ua.get_dict_info())  # 输出对象内部信息
	ua.get_channel_video_info() # 修改对象
	print(ua.get_dict_info())  # 输出对象内部信息
```



#### 1.11、下载高清视频样例

```python
import BiliUtil

if __name__ == '__main__':
    cookie = input('请提供登录后的cookie信息，以升级下载画质:')
    ua = BiliUtil.User()
    ua.set_by_url('https://space.bilibili.com/6799052/')
    ua.set_cookie(cookie)
    ua.get_all_video_data(base_path='Download', name_path=True)
```



### 2、频道类（Channel）

该类表示了一个用户所属的频道，当需要获取频道内所有视频信息时，可以选择创建该类的实例。

#### 2.1、成员变量

| 成员变量   | 变量含义           | 默认值 |
| ---------- | ------------------ | ------ |
| cookie     | 设置的cookie信息   | None   |
| uid        | 用户uid            | None   |
| cid        | 频道cid            | None   |
| name       | 频道名称           | None   |
| cover      | 频道封面           | None   |
| count      | 频道内专辑数量     | None   |
| album_list | 频道内专辑对象列表 | list() |
|            |                    |        |



#### 2.2、声明实例

你可以引入包并创建一个空的频道实例，空的频道实例不设置用户uid和频道cid。

```python
import BiliUtil
if __name__ == '__main__':
	ch = BiliUtil.Channel()
```



#### 2.3、设定频道cid

你可以通过多种方式设定用户uid与频道cid，详见下方案例。

```python
import BiliUtil
if __name__ == '__main__':
	# 方案一
	ch = BiliUtil.Channel(uid='4093899', cid='8020')
	# 方案二
	ch = BiliUtil.Channel()
	ch.set_user(uid='4093899', cid='8020')
	# 方案三
	ch = BiliUtil.Channel()
	ch.set_by_url(url='https://space.bilibili.com/4093899/channel/detail?cid=8020')
```

三种函数声明方式如下：

```python
def __init__(self, uid=None, cid=None)
def set_channel(self, uid, cid)
def set_by_url(self, url)
```

**注**：使用URL设定用户时，请使用准确的URL。



#### 2.4、设定Cookie

设定的cookie信息会影响到该实例及其包含的所有自动创建的对象。

```python
ch.set_cookie('SESSDATA=abcd68fd%2C1551761144%2C38d97xyz')
```

**注**：cookie设置的方式与意义详见第三章的解释。



#### 2.5、获取频道信息

你可以仅获取频道信息以及视频列表而不下载视频。

```python
import BiliUtil
if __name__ == '__main__':
	ch = BiliUtil.Channel(uid='4093899', cid='8020')
	ch.get_channel_info()
```



#### 2.6、获取频道视频数据

你可以直接获取频道内视频数据，该操作将自动帮你完成**频道信息**的获取。该操作支持**设定路径、命名方式、视频时长**，当设置了适合的cookie时，下载的画质将会自动提升。

```python
import BiliUtil
if __name__ == '__main__':
	ch = BiliUtil.Channel(uid='4093899', cid='8020')
	ch.get_channel_data(base_path='Download', name_path=True, max_length=None)
```

**注**：参数设置的方式与意义详见第三章的解释。



#### 2.7、获取对象信息字典

你可以将当前对象中保存的所有信息转换为字典格式保存，修改该字典时并不会影响实例。

```python
import BiliUtil
if __name__ == '__main__':
	ch = BiliUtil.Channel(uid='4093899', cid='8020')
	ch.get_channel_info()  # 修改对象
	print(ch.get_dict_info())  # 输出对象内部信息
```



#### 2.8、下载高清视频样例

```python
import BiliUtil
if __name__ == '__main__':
    cookie = input('请提供登录后的cookie信息，以升级下载画质:')
    ch = BiliUtil.Channel()
    ch.set_by_url('https://space.bilibili.com/4093899/channel/detail?cid=8020')
    ch.set_cookie(cookie)
    ch.get_all_video_data(base_path='Download', name_path=True)
```



### 3、专辑类（Album）

该类表示了一个专辑，即表示了一个av号对应的视频集合。当需要获取一个av号内所有视频时，可以选择创建该类的实例。

#### 3.1、成员变量

| 成员变量   | 变量含义               | 默认值 |
| ---------- | ---------------------- | ------ |
| cookie     | 设置的cookie信息       | None   |
| aid        | 专辑av号               | None   |
| name       | 专辑名称               | None   |
| time       | 发布时间               | None   |
| desc       | 专辑描述               | None   |
| zone       | 频道内视频对象列表None | None   |
| num        | 视频数量               | None   |
| cover      | 封面链接               | None   |
| like       | 点赞数量               | None   |
| coin       | 投币数量               | None   |
| favorite   | 收藏数量               | None   |
| share      | 分享数量               | None   |
| view       | 观看人次               | None   |
| danmu      | 弹幕数量               | None   |
| video_list | 专辑内视频对象列表     | list() |
|            |                        |        |



#### 3.2、声明实例

你可以引入包并创建一个空的频道实例，空的频道实例不设置用户uid和频道cid。

```python
import BiliUtil
if __name__ == '__main__':
	av = BiliUtil.Album()
```



#### 3.3、设定专辑aid

你可以通过多种方式设定av号，详见下方案例。

```python
import BiliUtil
if __name__ == '__main__':
	# 方案一
	av = BiliUtil.Album(aid='31483746')
	# 方案二
	av = BiliUtil.Album()
	av.set_user(aid='31483746')
	# 方案三
	av = BiliUtil.Album()
	av.set_by_url(url='https://www.bilibili.com/video/av31483746')
```

三种函数声明方式如下：

```python
def __init__(self, aid=None)
def set_album(self, aid=None)
def set_by_url(self, url)
```

**注**：使用URL设定用户时，请使用准确的URL。



#### 3.4、设定Cookie

设定的cookie信息会影响到该实例及其包含的所有自动创建的对象。

```python
av.set_cookie('SESSDATA=abcd68fd%2C1551761144%2C38d97xyz')
```

**注**：cookie设置的方式与意义详见第三章的解释。



#### 3.5、获取专辑信息

你可以仅获取专辑信息以及视频列表而不下载视频。

```python
import BiliUtil
if __name__ == '__main__':
	av = BiliUtil.Album(aid='31483746')
	av.get_album_info()
```



#### 3.6、获取频道视频数据

你可以直接获取专辑内视频数据，该操作将自动帮你完成**专辑信息**的获取。该操作支持**设定路径、命名方式、视频时长**，当设置了适合的cookie时，下载的画质将会自动提升。

```python
import BiliUtil
if __name__ == '__main__':
	av = BiliUtil.Album(aid='31483746')
	av.get_album_data(base_path='Download', name_path=True, max_length=None)
```

**注**：参数设置的方式与意义详见第三章的解释。



#### 3.7、获取对象信息字典

你可以将当前对象中保存的所有信息转换为字典格式保存，修改该字典时并不会影响实例。

```python
import BiliUtil
if __name__ == '__main__':
	av = BiliUtil.Album(uid='4093899', cid='8020')
	av.get_channel_info()  # 修改对象
	print(ch.get_dict_info())  # 输出对象内部信息
```



#### 3.8、下载高清视频样例

```python
import BiliUtil
if __name__ == '__main__':
    cookie = input('请提供登录后的cookie信息，以升级下载画质:')
    av = BiliUtil.Album()
    av.set_by_url('https://www.bilibili.com/video/av31483746')
    av.set_cookie(cookie)
    av.get_album_data(base_path='Download', name_path=True)
```



### 4、视频类（Video）

该类的实例不可手动创建，只能通过专辑类生成视频类的实例。

#### 4.1、成员变量

| 成员变量    | 变量含义         | 默认值 |
| ----------- | ---------------- | ------ |
| cookie      | 设置的cookie信息 | None   |
| aid         | 专辑av号         | None   |
| cid         | 视频cid          | None   |
| index       | 分P编号          | None   |
| name        | 分P名称          | None   |
| quality     | 视频质量         | None   |
| quality_des | 视频质量描述     | None   |
| length      | 视频时长         | None   |
| video       | 视频下载链接     | None   |
| audio       | 音频下载链接     | None   |
|             |                  |        |



#### 4.2、获取对象信息字典

你可以将当前对象中保存的所有信息转换为字典格式保存，修改该字典时并不会影响实例。

```python
import BiliUtil
if __name__ == '__main__':
	av = BiliUtil.Album(uid='4093899', cid='8020')
	av.get_channel_info()  # 获取数据并生成Video实例
	av.video_list[0].get_dict_info()  # 输出对象内部信息
```



### 5、静态函数

#### 5.1、视频合并函数

众所周知，视频由画面和声音组成。B站自从某个不知道的时间点以后将用户上传的视频分离为**独立的视频与音频**。因此，我们需要将下载好的视频与音频合并为一个文件，这样才方便观看。该函数将帮助你完成这一过程。

使用该函数需要您自行在计算机中配置**ffmpeg**渲染环境，若检查不到该环境存在，音视频合并函数将不会被引入。

> 函数声明：`merge_video_file(path, delete=False)`
>
> path：视频所在的文件夹
>
> delete：是否在视频合并后删除源文件

```python
import BiliUtil

if __name__ == '__main__':
    print('合并文件夹内视频')
    BiliUtil.merge_video_file('./Download', True)
```



## 三、<span id="help">帮助信息</span>

### 1、cookie信息

- cookie信息不影响除视频画质外其他信息的获取。
- 通过cookie信息，你可以在下载视频的时候获取到更高清的视频数据，程序会根据你的身份（未登录、已登录、大会员），自动尝试并下载画质最好的视频（手动设置画质的功能写了一半没写完）。
- 当对象设置了cookie信息后，程序会将该信息分发至该实例所包含的所有Album和Video对象中。声明新的对象以及对象的其他实例不受该操作的影响。

* 设定cookie信息时，类似于`_uuid=B45CF1AB-xxx; LIVE_BUVID=AUTO76154xxx; SESSDATA=abcd68fd%2C1551761144%2C38d97xyz`的cookie信息也是可以被识别的。也可以传入字典类型的cookie信息，但是cookie信息中必须包含`SESSDATA`字段，该字段是提升视频质量的关键点。
* 不同的身份信息可下载视频的映射表：
  * 未登录--->480P
  * 已登录--->1080P
  * 大会员--->1080P60FPS / 1080P+

### 2、下载参数

在下载视频时，你可以传入三个参数来调节下载的过程。base_path='Download', name_path=True, max_length=None

* base_path：**基础路径**，该路径为程序缓存视频的基础路径，程序将在该路径下创建分级的文件夹。
* name_path：**命名方式**，该参数为True时，将使用各级实例的名称作为生成文件夹的名称（非法字符将被替换为'_'）
* max_length：**下载长度**，该参数将限定视频下载的长度，单位为毫秒。当视频长度**大于**该值时，视频将不被下载。若您不需要该设置，请将该值设置为None。

### 3、视频下载流程

在生成了正确的对象后，我们就可以开始批量下载视频了。我需要向你解释一下下载的过程发生了什么。
1. 您需要传入三个参数"缓存路径"、"命名方式"、“限制长度”
2. 例将会自动获取实例的相关信息。
3. 程序将按照指定的命名方式生成文件夹。
4. 程序将按照"User>Channel>Album>Video"四级目录遍历，该操作将递归调用每个实例的`get_xxxxx_data`函数，并将三个参数传入，以此完成数据的遍历下载。
5. 数据将综合采用`aria2c`与`requests`进行下载，请确保您的环境中有`aria2c`与`requests`可供调用。
6. 对于下载完成的数据，程序将会做简单的验证（仅验证文件是否存在）
7. 下载结束后，程序将逐级将该对象下载时使用的数据，以json格式保存在同级目录中。
8. 当您重启了相同的下载过程时，aria2将帮助你完成断点续传，下载过的视频将不会重复下载。

*以下代码将演示如何下载频道视频*
```python
import BiliUtil
if __name__ == '__main__':
    cookie = input('请提供登录后的cookie信息，以升级下载画质:')
    # 创建频道对象
    ch = BiliUtil.Channel()
    # 设置频道参数
    ch.set_by_url('https://space.bilibili.com/4282930/channel/detail?cid=48758')
    # 传入cookie参数
    ch.set_cookie(cookie)
    # 开始批量下载视频
    ch.get_channel_data(base_path='Download', name_path=False, max_length=None)
```

### 4、使用效果

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190220225232678.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NzMxNjc3,size_16,color_FFFFFF,t_70)

### 5、关于BuilUtil

这个包中还有很多未完成的细节，还有一些想实现的功能未完成。
欢迎有兴趣的小伙伴一次参与，反馈BUG，更新代码，提供方案，我们共同完善它。

你可以联系我：mailto@wolfbolin.com

**声明：该博客内容仅供学习参考，请勿用于商业目的**



## 四、<span id="changelog">更新日志</span>

### v0.1.1

新增：

* 音视频合并函数
* 音视频批量合并代码示例

修改：

* 删除部分无意义的`(=・ω・=)`输出
* 调整aria2与ffmpeg环境检测机制

### v0.0.1

BiliUtil已经过基础测试，正式发布第一个版本，若要直接使用，请使用pip进行安装。
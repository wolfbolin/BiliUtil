# BiliUtil
Bilibili.com API工具包

**声明：该博客内容仅供学习参考，请勿用于商业目的**

## 一、引入代码
代码已上传至Github：https://github.com/wolfbolin/BiliUtil

将BiliUtil文件夹复制到你的文件夹中，运行`python setup.py install`安装依赖程序（或者安装必要的依赖即可）

## 二、使用说明
### 1、Channel类
该类表示了一个特定的频道，即某位UP创建的某一个频道。例如下图红框所示。
#### 1.1、创建Channel对象
在创建Channel对象时需要向实例提供uid和cid，uid代表用户的编号，cid代表频道的编号。
这两个值可以通过网页的url获得，例如：`https://space.bilibili.com/8366990/channel/detail?cid=11375`，该频道的主人uid为8366990，频道编号为11375。
通过这两个信息才能定位一个频道的信息，实例支持通过URL直接获得或者手动指定。
*以下代码将演示如何创建对象*
```
import BiliUtil
# 方法一：通过URL指定参数
ch = BiliUtil.Channel()
ch.set_by_url(url='https://space.bilibili.com/8366990/channel/detail?cid=11375')
# 方法二：直接设定参数
ch = BiliUtil.Channel(uid=8366990, cid=11375)
# or
ch.set_channel(uid=8366990, cid=11375)
```
#### 1.2、获取Channel信息
在创建了Channel对象后即可调用函数获取频道的相关信息，有效信息如下表所示：
| 成员变量 | 变量含义 |
|--|--|
| uid | UP主的uid |
| cid | 该频道的cid |
| name | 该频道名称 |
| cover | 该频道封面 |
| count | 该频道内视频数量 |
| cookie | 获取视频附加的cookie信息 |
| album_list | 频道内视频列表（Album类对象列表） |

* 调用`get_channel_info`成员函数即可获取该频道的相关信息。**请注意**`get_channel_info`函数仅获取频道的基本信息，并不会递归获取频道下每个视频的详细信息，并且获取信息的过程与cookie无关。
* 调用`get_dict_info`成员函数即可获取字典形式频道信息。**请注意**`get_dict_info`函数返回的字典仅可用于信息的输出，若修改字典内信息，并不能改变对象中相关变量的数据。
*以下代码将演示如何获取这些信息*
```
import json
import BiliUtil
# 设置频道参数
ch = BiliUtil.Channel(uid=8366990, cid=11375)
# 获取频道信息
ch.get_channel_info()
# 输出频道信息
ch_info = ch.get_dict_info()
print(json.dumps(ch_info))
```
#### 1.3、设置cookie信息
* cookie信息不影响除视频画质外其他信息的获取。
* 通过cookie信息，你可以在下载视频的时候获取到更高清的视频数据，程序会根据你的身份，自动尝试并下载画质最好的视频（手动设置画质的功能写了一半没写完）。
* 当对象设置了cookie信息后，程序会将该信息分发至该实例所包含的所有Album和Video对象中。声明新的对象以及对象的其他实例不受该操作的影响。
* **请注意**：与下载视频相关的cookie信息只有SESSDATA字段。你可以仅复制该字段，或者将发送至`www.bilibili.com`的所有cookie信息传入函数，程序会自行处理。若您需要传入一个字典，请确保字典中包含键为SESSDATA的键值对。

*以下代码将演示如何设置cookie信息*
```
import json
import BiliUtil
# 设置频道参数
ch = BiliUtil.Channel(uid=8366990, cid=11375)
# 设置cookie信息
ch.set_cookie('SESSDATA=abcd68fd%2C1551761144%2C38d97xyz')
# 输出频道信息
ch_info = ch.get_dict_info()
print(json.dumps(ch_info))
```

#### 1.4、下载单个视频
只需传入av号即可下载单个视频，如果传入cookie信息则可以下载更高清的视频。下载细节的讲解可参考1.5小节。

*以下代码将演示如何下载单个视频*
```
import BiliUtil

if __name__ == '__main__':
    cookie = input('请提供登录后的cookie信息，以升级下载画质:')
    av = BiliUtil.Album()
    av.set_by_url('https://www.bilibili.com/video/av42581472')
    av.set_cookie(cookie)
    av.get_album_data(base_path='Download', name_path=True)

```

#### 1.5、下载频道视频
在确认设置了uid和cid并且传入了合适的cookie信息后，我们就可以开始批量下载视频了。我需要向你解释一下下载的过程发生了什么。
1. 您需要传入两个参数"缓存路径"()、"命名方式"()（下文有解释）
2. Channel实例将会自动获取Channel的相关信息，即自动完成 1.2 所描述的过程。
3. 命名方式只支持用**id命名**或用**名称命名**，程序将按照命名方式，逐级创建文件夹
。当传入`True`时程序会在下载过程中使用每一级对象的`name`字段进行命名，例如：`Download\跳舞，干杯~\【欣小萌】书记魔性舞xxx\横屏版\`。当传入`False`时，程序会在下载过程中使用id进行命名，例如：`Download\11375\1841575\74191098\`。建议不使用名字作为路径名称，因为名字中常常包含大量的非法字符，可能会引起异常的程序终止。（异常字符已做处理，但是不完整）
4. 程序将按照"Channel>Album>Video"三级目录遍历，该操作将递归调用每个实例的`get_xxxxx_data`函数，并将两个参数传入，以此完成数据的遍历下载。
5. 数据将综合采用`aria2c`与`requests`进行下载，请确保您的环境中有`aria2c`与`requests`可供调用。
6. 对于下载完成的数据，程序将会做简单的验证（仅验证文件是否存在）
7. 下载结束后，程序将逐级将该对象下载时使用的数据，以json格式保存在同级目录中。

*以下代码将演示如何下载频道视频*
```
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
    ch.get_channel_data(base_path='Download', name_path=False)
```

#### 1.6、使用效果
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190220225232678.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM2NzMxNjc3,size_16,color_FFFFFF,t_70)

#### 1.7、关于BuilUtil
这个包中还有很多未完成的细节，还有一些想实现的功能未完成。
欢迎有兴趣的小伙伴一次参与，反馈BUG，更新代码，提供方案，我们共同完善它。

你可以联系我：mailto@wolfbolin.com

**声明：该博客内容仅供学习参考，请勿用于商业目的**

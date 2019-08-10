# BiliUtil

![Windows](https://img.shields.io/badge/Windows-support-green.svg)
![Linux](https://img.shields.io/badge/Linux-testing-orange.svg)
![License](https://img.shields.io/badge/License-MPL_2.0-orange.svg)
![Python](https://img.shields.io/badge/Python-3.7-blue.svg)
![Version](https://img.shields.io/badge/Version-2.x-blueviolet.svg)

Bilibili.com（B站）数据下载工具包。若您在使用过程中发现BUG或有可以改进之处，欢迎提交Issue或邮件（mailto@wolfbolin.com）与我联系。如果觉得还不错，欢迎Star和Fork支持一下。

> What's News?
>
> * 简化代码结构与文档长度，简化使用方式
> * cookie直接透传至，管理cookie更方面

## 一、安装方式

本工具包采用pip方式发布，并需要调用本地aria2c与ffmpeg插件，工具包启动前将根据环境变量检查环境是否可用，当环境中缺少相关插件时，部分类将不会导入。

*Step 1*: 使用pip安装

```shell
pip install BiliUtil
```

*Step 2*: 安装Aria2c插件

插件官网：<https://aria2.github.io/>

*Step 3:* 安装FFmpeg插件

插件官网：<https://ffmpeg.org/>

## 二、使用样例

获取视频信息并下载视频

```

```

获取用户信息并下载所有视频

```

```

获取用户频道并下载所有视频

```

```

## 三、接口文档

在第四章[特别说明](#四Q&A)中将讲解常见问题与逻辑结构，如有需要请移步第四章，那里可能有你想问的。本章仅讲解工具包的使用方法，简单粗暴便于理解。

### 1、用户类（BiliUtil.User）

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
| title    |                     |
| face     | 用户头像            |
| time     | 创号时间（可能为0） |
| level    | 用户级别            |
| sex      | 用户性别            |
| sign     | 用户签名            |
| vip      | 大会员              |

#### 1.2、`set_user(uid)`

你可以使用该函数设定用户uid或重新指定用户uid，该操作不会重置成员变量。

```python
user.set_user('20165629')
```

#### 1.3、`set_by_url(url)`

你可以通过该函数以url解析的方式指定对象的用户uid，该操作不会重置成员变量。

```python
user.set_by_url('https://space.bilibili.com/20165629?from=search')
```

#### 1.4、`sync(cookie=None)`<span id="user-sync"/>

你可用通过该操作更新对象的成员变量，如果你感觉信息不够丰满，请与开发者联系。

```python
user_info = user.sync(cookie='SESSDATA=abcd68fd...')
```

#### 1.5、`get_channel_list(cookie=None)`

你可以通过该操作获取用户公开的全部频道，返回值中将储存本工具包中频道类的对象。

```python
channel_list = user.get_channel_list(cookie='SESSDATA=abcd68fd...')
```

#### 1.6、`get_album_list(cookie=None)`

你可以通过该操作获取用户公开的全部视频，返回值中将储存本工具包中专辑类的对象。

```python
get_album_list(cookie='SESSDATA=abcd68fd...')
```

### 2、频道类（BiliUtil.Channel）

#### 2.1、`__init__(uid=None, cid=None)`

你可以为每一个用户声明一个对象实例，在声明时你可以指定用户uid、频道cid或在同步数据前设定用户uid、频道cid。

```python
channel = BiliUtil.Channel(uid='20165629', cid='9108')
```

每个实例中将包含以下成员变量，你可以在[`sync()`](#channel-sync)操作后读取这些信息。


| 成员变量   | 变量含义           | 默认值 |
| ---------- | ------------------ | ------ |
| uid        | 用户uid            | None   |
| cid        | 频道cid            | None   |
| name       | 频道名称           | None   |
| cover      | 频道封面           | None   |
| count      | 频道内专辑数量     | None   |
|            |                    |        |



## 四、Q&A

### 什么是uid？

### set_by_url有什么要求？

###  cookie的设置有什么要求？


# BiliUtil

![Windows](https://img.shields.io/badge/Windows-support-green.svg)
![Linux](https://img.shields.io/badge/Linux-testing-orange.svg)
![Python](https://img.shields.io/badge/Python-3.6-blue.svg)
![License](https://img.shields.io/badge/License-MPL_2.0-orange.svg)

Bilibili.com（B站）视频下载工具包，Github源码地址：[https://github.com/wolfbolin/BiliUtil](https://github.com/wolfbolin/BiliUtil)

若您在使用过程中发现BUG或有可以改进之处，欢迎提交Issue或邮件（mailto@wolfbolin.com）与我联系。如果觉得还不错，欢迎Star和Fork支持一下。

**声明：该内容仅供学习参考，请勿用于商业目的**

*帮助信息请看到[帮助信息](#三帮助信息)，更新日志请看到[更新日志](#四更新日志)*

[TOC]

# 近日即将更新，全新的结构，更快的下载，更少的异常

## 一、安装方式

1. 请使用pip安装该包：`pip install BiliUtil`
2. 若使用视频下载功能，请自行安装配置`aria2`。
3. 若使用视频合并功能，请自行安装配置`ffmpeg`。

*工具包将自动检查**aria2**和**ffmpeg**环境，若任一环境不存在，所涉及的类与函数将不会被引入*

## 二、坐等新版

## 三、坐等新版

## 四、更新日志

### v0.1.10

修复

* 修复了上一个版本在Linux平台上还是不能下载的Bug
* 修正了实例中的一些BUG
* 修正了文档锚定的错误写法

### v0.1.9

修复

* 修复了在Linux平台上相对路径错误导致的无法下载问题
* 添加了批量下载Up主的代码实例，在examples文件夹中。

### v0.1.8

修复

* 修复了严重的翻页BUG（之前版本get_all_video_info获取用户视频最多30个，程序出现了一些偏差）

### v0.1.7

修复

* get_xxx_info函数中vars函数运行异常
* 修改数据拷贝方式，防止数据被篡改
* 修改对象初始化方式，防止二次创建对象时异常
* 修正若干数据获取逻辑BUG

### v0.1.6

修复

* 修复exclude_list列表使用BUG

新增

* 为频道与用户对象添加获取已下载视频的AV号列表。
* 为专辑对象添加判断视频是否已下载的访问接口

### v0.1.5

新增

* 为频道与用户对象添加获取AV号列表函数。
* 允许在批量下载视频时，通过添加排除列表，过滤部分视频的下载。
* 为多个函数添加合适的响应值。

### v0.1.4

解决ffmpeg合成阶段程序卡死。由于pipe size的大小限制，导致程序在收到超过64kb的输出时，程序会卡死不动。修改process.wait()为process.communicate()以解决该问题。

### v0.1.3

操作失误导致pip中v0.1.2版本被删除，将以v0.1.3版本发布。建议更新至最新版本后再使用。

### v0.1.2

修改：

* 修复了`ffmpeg`环境检测不通过的BUG，因为使用了错误的语法。

* 移除了对powershell的支持，未来将在linux环境中测试。
* 修复了使用`aria2c`时的错误语法，解决自定义输出路径报错。
* 修改路径获取方案，相对路径传入后，将以绝对路径进行计算。


### v0.1.1

新增：

* 音视频合并函数
* 音视频批量合并代码示例

修改：

* 删除部分无意义的`(=・ω・=)`输出
* 调整aria2与ffmpeg环境检测机制

### v0.0.1

BiliUtil已经过基础测试，正式发布第一个版本，若要直接使用，请使用pip进行安装。

#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: mage
# Mail: mage@woodcol.com
# Created Time:  2018-1-23 19:17:34
#############################################


from setuptools import setup, find_packages

setup(
    name="BiliUtil",
    version="0.0.8",
    keywords=("pip", "bilibili"),
    description="The download tools for bilibili video",
    license="MIT Licence",

    url="https://github.com/wolfbolin/BiliUtil",
    author="wolfbolin",
    author_email="mailto@wolfbolin.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['requests', 'fake-useragent']
)

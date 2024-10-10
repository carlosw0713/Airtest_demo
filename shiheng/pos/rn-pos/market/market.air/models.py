#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/16 11:44
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
# @File    : models.py
# @IDE     : PyCharm
# @REMARKS : 备注

__author__ = "carlos"

import logging

# 批量设置 Airtest 默认的日志记录器并设置日志级别
tags=['airtest.core.android.adb',
      'airtest.utils.nbsp',
      'airtest.core.android.cap_methods.minicap',
      'airtest.core.android.rotation'
      'airtest.core.android.touch_methods.minitouch',
      ]
for i in tags:
    logger = logging.getLogger(i)
    logger.setLevel(logging.ERROR) # 日志级别ERROR才显示


from airtest.core.api import *
# auto_setup(__file__)
auto_setup(__file__, logdir=True, devices=["Android://"])

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
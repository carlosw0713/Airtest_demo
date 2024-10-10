#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/16 11:43
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
# @File    : LimitedtimeDiscount.py
# @IDE     : PyCharm
# @REMARKS : 备注

from models import *

class LimitedtimeDiscountPage():

    def Limitedtime_Discount(self):
        # 限时折扣
        poco(text="carlos商品活动").click()
        poco(text="carlos-限时折扣-多规格").click()
        poco(text="规格2e").click()
        poco(text="确定").click()
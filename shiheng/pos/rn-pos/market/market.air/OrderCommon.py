#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/16 11:55
# @Author  : carlos
# @Email   : carlos.w.0713@outlook.com
# @File    : OrderCommon.py
# @IDE     : PyCharm
# @REMARKS : 备注

from models import *

class OrderCommonPage:

    def Login_rnpos(self):

        poco("com.miui.home:id/workspace").offspring("门店通_Test").offspring("com.miui.home:id/icon_icon").click()

    def InitPage(self):

        # 初始化操作，清除会员登录、清除购物车

        if not poco(text="会员识别").exists():
            poco(text='').click() #退出

            msg = poco('android:id/message').get_text()
            assert_equal(msg, '确定登出该会员信息？')

            poco(text='确认', name='android:id/button1').click()

        poco(text="清空").click()

        msg = poco('android:id/message').get_text()
        assert_equal(msg, '确定清空购物车？')

        poco(text='确认', name='android:id/button1').click()

    def Member_Login(self):

        # 会员登录
        poco(text="会员识别").click()
        Member_Phone = 13142222222
        Member_Phonestr = str(Member_Phone)
        for i in range(len(Member_Phonestr)):
            # print(Member_Phonestr[i])
            poco(text=Member_Phonestr[i]).click()
        poco(text='确认').click()

    def SettleAccounts(self):
        # 结算
        poco(text="结算").click()
        poco(text="发起收款").click()
        poco(text='现金支付').click()
        poco(text="确认").click()

if __name__ == '__main__':
    OrderCommonPage().InitPage()
# -*- encoding=utf8 -*-
__author__ = "carlos"

from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["Android:///",])



from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


# script content
print("start...")


poco(text="会员识别").click()
poco("android.widget.EditText").set_text('13142222222')
poco(text='').click()
poco(text='确认',name='android:id/button1').click()

a=poco(text="商品活动",type="android.widget.TextView").sibling()
for i in a:
    print(i.get_text)

a=poco(text="优惠.",type="android.widget.TextView")
print(a.get_text)
    
poco(text='确认',name='android:id/button1').click()
msg=poco('android:id/message').get_text()
print(msg)

poco("android.widget.EditText").click()
text(1234567890)

a=poco('carlos-限时折扣-多规格').get_text()
print(a)
poco("android.widget.EditText").setattr('selected',True)
poco("android.widget.EditText").click()
poco("android.widget.EditText").set_text(13142392973)

a=poco(text='商品活动').sibling(text=contains_query('优惠'))
a=poco(textMatches=".*优惠.*").get_text()
a=poco(textMatches="优惠14").get_text()
print(a)

android.view.ViewGroup a=poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("android:id/content").child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup")[1].child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup")[1].child("android.view.ViewGroup")[1].child("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").offspring("android.widget.FrameLayout").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup")[1].child("android.widget.ScrollView")[0].child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.view.ViewGroup").child("android.widget.TextView").get_text()
print(a)

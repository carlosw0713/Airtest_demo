# -*- encoding=utf8 -*-
__author__ = "carlos"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from base64 import b64decode


if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["Android:///",])


from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


# script content
print("start...")


# generate html report
# from airtest.report.report import simple_report

# yaunpoco(text="存储空间").click()

# touch操作
touch(Template(r"tpl1719367256373.png", record_pos=(-0.128, 0.378), resolution=(1200, 1920)))

## poco 操作
print(len(poco('android:id/title'))) #21 个元素
print(len(poco(name='android:id/title'))) #21 个元素

### click点击操作
poco('android:id/title')[3].click() #暂时不行,得去掉【3】
poco(text="我的设备").click('center') #点击元素的中心点
poco('android:id/title',type = 'android.widget.TextView',text='WLAN').click([0.1, 0.2]) #聚焦点击
poco(desc='壁纸').focus([0.5, 0.5]).click() #聚焦点击头同上


### Swipe滑动
point_a = [0.14, 0.9]
center = [0.14, 0]
poco.swipe(point_a, center) # swipe from A to B

poco(text='授权管理').click()
point_b=[0.8,0.8]
direction = [-0.5, 0] #滑动的方法量 x,y
poco.swipe(point_b, direction=direction) # swipe from A by given direction 

### 输入（文字输入）问题反馈里
poco(text='问题反馈').click()
poco('com.miui.bugreport:id/et').set_text(f'手动输入哈哈哈啊\n换行666')
### 获取元素信息

point_c=poco(text='应用管理')
print(point_c.get_text())
print(point_c.get_name())

### 按键操作
keyevent("BACK")
keyevent("Home")

### 截屏 snapshot 
from base64 import b64decode
b64img, fmt = poco.snapshot(width=720)
open(f'carlos-截图.{fmt}', 'wb').write(b64decode(b64img))









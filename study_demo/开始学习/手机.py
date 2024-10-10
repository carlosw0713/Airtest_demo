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


# generate html report
# from airtest.report.report import simple_report
touch(Template(r"tpl1719197173373.png", record_pos=(-0.113, 0.01), resolution=(1080, 2400)))
sleep(1.0)

touch(Template(r"tpl1719197311798.png", record_pos=(-0.34, -0.47), resolution=(1080, 2400)))
sleep(1.0)

touch(Template(r"tpl1719197334340.png", record_pos=(-0.381, -0.502), resolution=(1080, 2400)))
sleep(1.0)

touch(Template(r"tpl1719197394467.png", record_pos=(0.061, 0.52), resolution=(1080, 2400)))
sleep(1.0)

touch(Template(r"tpl1719197424129.png", record_pos=(-0.015, 0.633), resolution=(1080, 2400)))














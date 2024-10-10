# -*- encoding=utf8 -*-
__author__ = "AirtestProject"
__desc__ = """
网易云音乐app-测试实操
1.录制运行视频、用例跑完后自动生成报告
2.进入网易云音乐首页
3.找到薛之谦的指定歌曲
4.获取抖音排行榜的所有歌名
"""

from airtest.core.api import *
from airtest.report.report import simple_report
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.core.android.recorder import *
from airtest.core.android.adb import *

# 脚本初始化
auto_setup(__file__,devices=["android://127.0.0.1:5037/PFT4PBLF75GQHYBM?cap_method=JAVACAP&&ori_method=JAVACAPORI&&touch_method=JAVATOUCH"],logdir=r"D:\test\pro01_log")

def enter_music():
    # 点击不同意
    poco("com.netease.cloudmusic:id/quit").click()
    sleep(1.0)
    assert_not_exists(Template(r"tpl1604644121931.png", record_pos=(-0.124, -0.479), resolution=(720, 1440)), "不同意并退出APP")


# 点击同意
    start_app("com.netease.cloudmusic")
    poco("com.netease.cloudmusic:id/agree").wait_for_appearance(timeout=60)
    poco("com.netease.cloudmusic:id/agree").click()

    wait(Template(r"tpl1604633187765.png", record_pos=(0.0, -0.05), resolution=(720, 1440)))
    sleep(2.0)
    poco("com.netease.cloudmusic:id/permissionGrant").click()
    sleep(1.0)

    poco("com.android.packageinstaller:id/permission_allow_button").wait_for_appearance()
    poco("com.android.packageinstaller:id/permission_allow_button").click()
    sleep(1.0)

    touch(Template(r"tpl1604633413603.png", record_pos=(0.215, 0.049), resolution=(720, 1440)))


    wait(Template(r"tpl1604632791326.png", record_pos=(-0.003, -0.487), resolution=(720, 1440)),timeout=120)

    poco("com.netease.cloudmusic:id/agreeCheckbox").wait_for_appearance()
    poco("com.netease.cloudmusic:id/agreeCheckbox").click()

    poco("com.netease.cloudmusic:id/trial").click()

    sleep(5.0)

    assert_exists(Template(r"tpl1604645199520.png", record_pos=(-0.033, -0.311), resolution=(720, 1440)), "进入网易云首页")
    
    
def find_music():
    poco("搜索").click()

    text("薛之谦")

    assert_exists(Template(r"tpl1604645789934.png", record_pos=(-0.237, -0.507), resolution=(720, 1440)), "找到薛之谦的歌单")

    poco(text="歌手：薛之谦").click()

    touch(Template(r"tpl1604654544126.png", record_pos=(-0.328, 0.011), resolution=(720, 1440)))

    while True:

        if not exists(Template(r"tpl1604893064017.png", threshold=0.85, record_pos=(-0.342, 0.818), resolution=(720, 1440))):
            poco.swipe([0.719, 0.907],[0.246, 0.908])
        else:
            print("已找到目标歌曲")
            sleep(1.0)
            poco("android.widget.ImageView").click()
            sleep(1.0)
            poco("com.netease.cloudmusic:id/likeBtn").click()
            break

    for i in range(4):
        keyevent("BACK")

    sleep(1.0)
    
def Crawling_music():
    poco("androidx.recyclerview.widget.RecyclerView").child("android.view.ViewGroup")[3].child("com.netease.cloudmusic:id/portalImage").click()


    while True:

        if not exists(Template(r"tpl1604894647838.png", record_pos=(-0.318, 0.122), resolution=(720, 1440))):
            poco.swipe([0.531, 0.733],[0.549, 0.225])
        else:
            print("已找到抖音排行榜")
            sleep(1.0)
            poco("com.netease.cloudmusic:id/pagerListview").child("android.widget.LinearLayout")[0].child("com.netease.cloudmusic:id/billboardLeft").child("com.netease.cloudmusic:id/billboardImg").click()
            break

    assert_exists(Template(r"tpl1604903382239.png", record_pos=(-0.031, -0.487), resolution=(720, 1440)), "进入抖音排行榜的歌单")

# 定义1个空数组用于存放排行榜的歌名
    titles = []
# 定义数组目前的长度和最终的长度
    current_count, last_count = len(titles), len(titles)

    while True:
        last_count = len(titles)
        for title in     poco("com.netease.cloudmusic:id/musicInfoList").child("com.netease.cloudmusic:id/musicListItemContainer"):
            a = title.offspring("com.netease.cloudmusic:id/songName")
            if not a.exists():
                continue
            name = a.get_text()
            if not name in titles:
                titles.append(name)
                print(name)
    
        current_count = len(titles)
        poco.swipe([0.5,0.7],[0.5,0.1],duration=2)
        sleep(1.0)
    
    # 当俩者数值相等，即current_count不再增加时，表明爬取完毕
        if current_count == last_count:
            log("总共爬取"+str(last_count)+"首歌曲的名称")
            print("总共爬取"+str(last_count)+"首歌曲的名称")
            break

            
try:
# 开启录屏
    adb = ADB(serialno="PFT4PBLF75GQHYBM")
    recorder = Recorder(adb)
    recorder.start_recording()

# 重启应用，保证初始化状态一致
    clear_app("com.netease.cloudmusic")
    start_app("com.netease.cloudmusic")

# 初始化poco
    sleep(5.0)
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

# 执行用例
    enter_music()
    find_music()
    Crawling_music()
    
# 结束录屏
    recorder.stop_recording(output=r"D:\test\pro01_log\cloudmusic.mp4")
finally:
    simple_report(__file__,logpath=r"D:\test\pro01_log",output=r"D:\test\pro01_log\log.html")
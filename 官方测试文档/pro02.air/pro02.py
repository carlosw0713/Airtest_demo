# -*- encoding=utf8 -*-
__author__ = "AirtestProject"
__desc__ = """
网易云音乐app-测试实操
1.录制运行视频、用例跑完后自动生成报告
2.进入网易云音乐首页
3.找到薛之谦的指定歌曲
4.获取网络热歌榜的所有歌名
"""

from airtest.core.api import *
poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("android:id/content").child("android.view.ViewGroup").click()
poco(text="减").click()
from airtest.report.report import simple_report
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.core.android.recorder import *
from airtest.core.android.adb import *

# 脚本初始化
auto_setup(__file__,devices=["android://127.0.0.1:5037/bmhy6lfaskiziffu?ori_method=ADBORI&touch_method=ADBTOUCH&"]")

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

    assert_exists(Template(r"tpl1623984154162.png", record_pos=(0.06, -0.324), resolution=(720, 1440)), "进入网易云首页")
    
    
def find_music():
    poco("com.netease.cloudmusic:id/searchBar").click()
    # poco("搜索").click()

    text("薛之谦")

    assert_exists(Template(r"tpl1623985622956.png", record_pos=(-0.196, -0.453), resolution=(720, 1440)), "找到薛之谦的歌单")

    poco(text="歌手：薛之谦 (Joker Xue)").click()
    # poco(text="歌手：薛之谦").click()

    touch(Template(r"tpl1623986184677.png", record_pos=(-0.2, 0.263), resolution=(720, 1440)))
    touch([260, 867])
    sleep(2.0)
    touch(Template(r"tpl1623986284971.png", record_pos=(-0.308, 0.394), resolution=(720, 1440)))


    while True:

        if not exists(Template(r"tpl1624274392590.png", threshold=0.8, record_pos=(-0.218, 0.797), resolution=(720, 1440))):
            poco.swipe([0.719, 0.907],[0.246, 0.908])
        else:
            print("已找到目标歌曲")
            sleep(1.0)
            poco("com.netease.cloudmusic:id/iv_smallAlbumCover").click()
            # poco("android.widget.ImageView").click()
            sleep(1.0)
            poco("com.netease.cloudmusic:id/likeBtn").click()
            break

    for i in range(4):
        keyevent("BACK")

    sleep(1.0)
    
def Crawling_music():
    # poco("androidx.recyclerview.widget.RecyclerView").child("android.view.ViewGroup")[3].child("com.netease.cloudmusic:id/portalImage").click()
    poco(text="排行榜").click()
    sleep(2.0)

    while True:

        if not exists(Template(r"tpl1623988230455.png", record_pos=(-0.314, -0.057), resolution=(720, 1440))):
            poco.swipe([0.531, 0.733],[0.549, 0.225])
        else:
            print("已找到网络热歌榜")
            sleep(1.0)
            poco(text="网络热歌榜").click()
            break

    assert_exists(Template(r"tpl1623988327748.png", record_pos=(-0.092, -0.603), resolution=(720, 1440)), "进入网络热歌榜的歌单")

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
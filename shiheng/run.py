# -*- encoding=utf-8 -*-
# Run Airtest in parallel on multi-device
import os
import traceback
import subprocess
import webbrowser
import time
import json
import shutil
from airtest.core.android.adb import ADB
from jinja2 import Environment, FileSystemLoader

def run(devices, airs):
    """"
        run_all
 18  19     """
    try:
        data_r=[]
        global time_s
        time_s = time.time()
        for air in airs:
            results = load_jdon_data(air)
            tasks = run_on_multi_device(devices, air, results)
            for task in tasks:
                status = task['process'].wait()
                results['tests'][task['dev']] = run_one_report(task['air'], task['dev'])
                results['tests'][task['dev']]['status'] = status
                name = air.split(".")[0]
                json.dump(results, open(get_path("result")+os.sep+name+'_data.json', "w"), indent=4)
            data_r.append(results)
        run_summary(data_r)
    except Exception as e:
        traceback.print_exc()


def run_on_multi_device(devices, air, results):
    """
        在多台设备上运行airtest脚本
        Run airtest on multi-device
    """
    tasks = []
    for dev in devices:
        log_dir = get_path("log",dev,air)
        #命令行执行：airtest run openOrder.air --device Android://127.0.0.1:5037/b7f0c036 --log F:irtest_code\good_store_project\log\openOrder
        cmd = [
            "airtest",
            "run",
            air,
            "--device",
            "Android:///" + dev,
            "--log",
            log_dir
        ]
        try:
            tasks.append({
                'process': subprocess.Popen(cmd, cwd=os.getcwd()),
                'dev': dev,
                'air': air
            })
        except Exception as e:
            traceback.print_exc()
    return tasks

#点击每个用例的详情页面
def run_one_report(air, dev):
    """"
        生成一个脚本的测试报告
        Build one test report for one air script
    """
    try:
        log_dir = get_path("log",dev, air)
        log = os.path.join(log_dir, 'log.txt')
        if os.path.isfile(log):
            #命令行执行：airtest report F:irtest_code\good_store_project\openOrder.air --log_root F:irtest_code\good_store_project\log\openOrder --outfile F:irtest_code\good_store_project\log\openOrder\openOrder.html --lang zh
            #如果是selenium，则最后要加上selenium插件
            #airtest report F:irtest_code\good_store_project\openOrder.air --log_root F:irtest_code\good_store_project\log\openOrder --outfile F:irtest_code\good_store_project\log\openOrder\openOrder.html --lang zh --plugins airtest_selenium.report
            cmd = [
                "airtest",
                "report",
                air,
                "--log_root",
                log_dir,
                "--outfile",
                os.path.join(log_dir, 'log.html'),
                "--lang",
                "zh"
            ]
            ret = subprocess.call(cmd, shell=True, cwd=os.getcwd())
            return {
                    'status': ret,
                    'path': os.path.join(log_dir, 'log.html')
                    }
        else:
            print("Report build Failed. File not found in dir %s" % log)
    except Exception as e:
        traceback.print_exc()
    return {'status': -1, 'device': dev, 'path': ''}


def run_summary(data):
    """"
        生成汇总的测试报告
        Build sumary test report
    """
    try:
        for i in data:
            c = get_json_value_by_key(i,"status")

        summary = {
            'time': "%.3f" % (time.time() - time_s),
            'success': c.count(0),
            'count': len(c)
        }
        summary['start_all'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                             time.localtime(time_s))
        summary["result"] = data
        print("summary++++++++++",summary)

        env = Environment(loader=FileSystemLoader(os.getcwd()),
                          trim_blocks=True)
        html = env.get_template('report_tpl.html').render(data=summary)
        with open("report.html", "w", encoding="utf-8") as f:
            f.write(html)
        webbrowser.open("report.html")
    except Exception as e:
        traceback.print_exc()


def load_jdon_data(air):
    """"
        加载进度
            返回一个空的进度数据
    """
    clear_log_dir(air)
    return {
        'start': time.time(),
        'script': air,
        'tests': {}

    }

def clear_log_dir(air):
    """"
        清理log文件夹 openCard.air/log
        Remove folder openCard.air/log
    """
    log = os.path.join(os.getcwd(), air, 'log')
    if os.path.exists(log):
        shutil.rmtree(log)

#获取key为status的值
def get_json_value_by_key(in_json, target_key, results=[]):
    for key,value in in_json.items(): # 循环获取key,value
        if key == target_key:
            results.append(value)
        if isinstance(value, dict):
            get_json_value_by_key(value,target_key)
    return results

#获取路径
def get_path(content,device=None,air="openCard.air"):
    root_path = os.getcwd()
    path = os.getcwd()
    if content=="result":
        #返回测试报告路径
        path = os.path.join(root_path,"result")
    elif content == "log":
        log_dir = os.path.join(root_path,air, 'log', device.replace(".", "_").replace(':', '_'))
        #如果没有日志路径则创建一个
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        #返回日志路径
        path = log_dir
    elif content == "cases":
        #返回测试用例路径
        path = os.path.join(root_path,air)
    else:
        #返回根目录
        path = root_path
    return path

#获取路径下所有air的测试用例文件
def get_cases(path):
    cases=[]
    for name in os.listdir(get_path(path)):  # 遍历当前路径下的文件夹和文件名称
        if name.endswith(".air"):
            cases.append(name)
    return cases

def sort_cases(cases,loginAir,outAir):
    #清除列表中的登录、退出登录，然后将其分别添加到列表的第一位和最后一位
    cases.remove(loginAir)
    cases.remove(outAir)
    cases.insert(0, loginAir)
    cases.insert(len(airs), outAir)
    return cases


if __name__ == '__main__':

    """
        初始化数据
        Init variables here
    """
    #获取所有已连接的设备列表
    devices = [tmp[0] for tmp in ADB().devices()]

    #设置指定设备执行测试用例
    devices = ["BTY4C16705003852","b7f0c036"]
    #获取所有测试用例
    airs = get_cases("root")
    #将登录用例排在最前面执行，退出用例排在最后面执行
    sort_airs = sort_cases(airs,"loginPro.air","loginOutPro.air")
    #获取指定用例,按顺序执行
    sort_airs = ["openCardPro.air","openOrderPro.air","quickMoneyPro.air"]
    """
        执行脚本
        excute scripts
    """
    # 运行所有脚本
    run(devices, sort_airs)

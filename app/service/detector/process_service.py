import json
from app.common.errorcode import *

# 数据预处理包括：参数异常检测，输入异常检测等
# return：两部分：1）用于检测的数据：包括指标名、时间戳、指标值
#               2）前期异常结果


def do_the_all_preprocess(data):
    # 用于检测的数据
    detect_data = []
    # 前期异常结果
    ano_results = []
    # json转为dict
    data = json.loads(data.decode("utf-8"), strict=False)
    print(type(data))
    print(data)
    # 检测key是否存在
    if ("cluster" in data) and ("time" in data) and ("ne_dat" in data) and ("host_dat" in data):
        cluster = data["cluster"]
        timestamp = data["time"]
        ne_dat = data["ne_dat"]
        host_dat = data["host_dat"]
        # 检测value是否存在
        if timestamp and cluster:
            if ne_dat or host_dat:
                # 检测时间戳和指标值是否存在
                for detect in ne_dat:  # 网元级指标
                    if detect["name"] is None or detect["value"] is None:
                        ano_results.append(Parm_ERR)
                    # 检测时间戳和指标值是否一一对应
                    elif len(detect["value"]) != len(timestamp):
                        ano_results.append(Time_ERR)
                    else:
                        par_s = detect["name"] + "_" + cluster
                        dt = {
                            "par_s": par_s,
                            "timestamp": timestamp,
                            "value": detect["value"]
                        }
                        detect_data.append(dt)
                for detect_value in host_dat:  # 主机级指标
                    if detect_value["host"] is None:  # 主机名
                        ano_results.append(Parm_ERR)
                    else:
                        if detect_value["dat"]:  # 主机级指标信息
                            for dat in detect_value["dat"]:
                                if dat["name"] is None or dat["value"] is None:
                                    ano_results.append(Parm_ERR)
                                elif len(dat["value"]) != len(timestamp):  # 检测时间戳和指标值是否一一对应
                                    ano_results.append(Time_ERR)
                                else:
                                    par_s = dat["name"] + "_" + cluster + "_" + detect_value["host"]
                                    dt = {
                                        "par_s": par_s,
                                        "timestamp": timestamp,
                                        "value": dat["value"]
                                    }
                                    detect_data.append(dt)
            else:
                ano_results.append(Parm_ERR)
        else:
            ano_results.append(Parm_ERR)
    else:
        ano_results.append(Key_ERR)
    return detect_data, ano_results

# 主机
on_production = 1  # 在产
stop_production = 0  # 停产
Delete = -1  # 逻辑删除

# 设备
on_line = 0  # 在线
stop_run = 1  # 停运
need_repair = 2  # 报修
maintenance = 3  # 维护

# 传感器与设备关系
working = 1  # 传感器在设备工作
not_working = -1  # 传感器不在设备上工作

# 连表
b = ["status", "equipment_code", "client_unit", "region"]

#  维护状态
stop_maintenance = 1  # 维护结束
not_stop_maintenance = 0  # 维护未结束


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]  # 拿到对应的字段列表
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# 主机
on_production = 1  # 在产
stop_production = -1  # 停产
Delete = 0  # 逻辑删除

# 设备
on_line = 0  # 在线
stop_run = 1  # 停运
need_repair = 2  # 报修
maintenance = 3  # 维护

# 传感器与设备关系
working = 1  # 传感器在设备工作
not_working = -1  # 传感器不在设备上工作

a = ["传感器类型", "传感器型号", "状态"]
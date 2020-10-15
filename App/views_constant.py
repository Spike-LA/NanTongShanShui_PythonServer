# 主机

on_production = 1  # 在产
stop_production = 0  # 停产
Delete = -1  # 逻辑删除

# 设备
on_line = 0  # 在线
stop_run = 1  # 停运
need_repair = 2  # 报修
maintenance = 3  # 维护
scraped = 4  # 报废

# 传感器与设备关系
working = 1  # 传感器在设备工作
not_working = -1  # 传感器不在设备上工作

#  维护状态
stop_maintenance = 1  # 维护结束
not_stop_maintenance = 0  # 维护未结束

# 维护结果
finish_maintenance = 1  # 维护完成
wait_maintenance = 0  # 等待维护
not_finish_maintenance = -1  # 维护未完成

# 维护原因
routine_maintenance = 0  # 例行维护
user_repair = 1  # 用户报修
operation_maintenance = 2  # 运维报修

# 账户状态
activated = 1  # 账户已激活
none_efficacy = 0  # 账户已失效

# 传感器状态
is_using = 1  # 可以使用
not_using = -1  # 停止使用

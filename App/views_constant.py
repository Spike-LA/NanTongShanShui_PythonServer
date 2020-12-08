# 主机

on_production = 1  # 在产
stop_production = 0  # 停产
Delete = -1  # 逻辑删除

# 设备状态
on_line = 0  # 在线(在用户厂里）
stop_run = 1  # 停运(在公司厂里）
scraped = 2  # 报废
need_repair = 3  # 报修
maintenance = 4  # 维护

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
is_using = 1  # 正在使用
sensor_scrap = 0  # 已报废
un_using = 2  # 未使用

# 水质提醒
wait_deal = 1  # 未处理
is_dealt = 0  # 已处理

# 用户状态
not_Delete = 1  # 未删除
Delete = -1  # 逻辑删除

# 用户登录状态
on = 1  # 已登录
out = -1  # 未登录

# 客户、联系人状态
on_using = 1  # 未删除
not_using = -1  # 逻辑删除

# 发送状态
success = 1  # 发送成功
fail = 0  # 发送失败

# 执行状态
do_success = 1  # 执行成功
do_fail = 0  # 执行失败

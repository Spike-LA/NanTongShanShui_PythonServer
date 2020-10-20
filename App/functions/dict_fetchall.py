# 自定义原生sql的fetchall方法（将获取的数据形式改为列表套字典）
def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]  # 拿到对应的字段列表
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()]

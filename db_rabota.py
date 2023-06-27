import pymysql

# данные от БД
HOST = ""
USER = ""
PASSWORD = ""
DB = ""


def get_review_for_rewriting() -> tuple:
    # устанавливаем соединение
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
    cursor = conn.cursor()

    # выполняем следующий запрос
    # cursor.execute(
    #     f"SELECT id, recall FROM u1380978_database.t_request WHERE status = 'Переписывание';"
    # )
    cursor.execute(
        f"""SELECT r.id, r.recall, r.status, c.address, c.fullname, r.sex, a.fullname FROM u1380978_database.t_request r 
            left join u1380978_database.t_client c on c.id = r.client_id
            left join u1380978_database.t_area a on a.id = r.area_id
            WHERE status = 'Переписывание'"""
    )
    # кладем результат в кортеж
    result_set = cursor.fetchall()

    # закрываем соединение
    conn.close()

    # возвращаем кортеж со случайным отзывом
    return result_set


print(get_review_for_rewriting())


def update_review_for_rewriting(id: int, recall: str) -> None:
    # устанавливаем соединение
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB)
    cursor = conn.cursor()

    # подготавливаем запрос
    sql = f"UPDATE u1380978_database.t_request SET recall = '{recall}' WHERE t_request.id = {id};"

    # выполняем запрос
    cursor.execute(sql)
    conn.commit()
    # подготавливаем запрос
    sql = f"UPDATE u1380978_database.t_request SET status = 'Исправлен' WHERE t_request.id = {id};"

    # выполняем запрос
    cursor.execute(sql)
    conn.commit()
    
    sql_2 = f"CALL u1380978_database.update_requests_rewrite();"
    # выполняем запрос
    cursor.execute(sql_2)
    conn.commit()

    # закрываем соединение
    conn.close()

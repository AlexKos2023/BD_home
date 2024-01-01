import psycopg2
import os

'''для создания базы данных необходимо:
    1. Установить библиотеку pip install psycopg2-binary.
    2. Создать базу данных createdb -U postgres homeworkbase (command).
    3. Установить соединение, введя пароль.
    4. Создать таблицы, передав название таблиц, после введя их параметры (указаны внизу).
    '''

PASSW = str(input("Введите пароль от базы данных "))



def open_create_BD(PASSW: str):
    try:
        connection = psycopg2.connect(user="postgres",
        password = PASSW,
        database="homework")
        print("Соединение с базой установлено")
    except:
        pass
    return connection

connection = open_create_BD(PASSW)
    
def create_table(connection,
                 name_table: str):
    if not os.path.isdir(r".\Netologia"):
        os.mkdir(r".\Netologia")
        new_file = open (r".\Netologia\names_list.txt", "w", encoding="utf-8")
        new_file.write(name_table)
    else:
        with open(r".\Netologia\names_list.txt", "r", encoding="utf-8") as f:
            x = (f.read()).split(', ')
            if name_table in x:
                print(f'Таблица {name_table} уже существует')
    with connection.cursor() as cur:
        meta = str(input("Введите параметры таблицы: "))
        cur.execute(f'CREATE TABLE IF NOT EXISTS {name_table}({meta});')
        connection.commit()
        with open(r".\Netologia\names_list.txt", "a", encoding="utf-8") as f:
            f.write(f'{name_table}, ')
        print(f'Создана таблица {name_table}')           
    return

'''Возможно получить список существующих папок без использования OS:
with connection.cursor() as cur:
    cur.execute("""SELECT table_name FROM information_schema.tables
           WHERE table_schema = 'public'""")
    for table in cur.fetchall():
        print(table)'''

def give_me_folders_name():
    if os.path.isfile(r".\Netologia\names_list.txt"):
        with open(r".\Netologia\names_list.txt", "r", encoding="utf-8") as f:
            x = (f.read()).split(', ')
            print("Список существующих папок: ")
            print(*x, sep = '\n')
    else:
        print('Файл не найден.')
    return

def delete_table(connection, folders_name: str):
    with open(r".\Netologia\names_list.txt", "r", encoding="utf-8") as f:
        exist_name = f.read().split(', ')
    for i in folders_name.split(', '):
        if i != "":
            with connection.cursor() as cur:
                cur.execute(f'DROP TABLE IF EXISTS {i} CASCADE')
                connection.commit()
                if i in exist_name:
                    exist_name.remove(i)
            to_write = str(exist_name)
            with open(r".\Netologia\names_list.txt", "w", encoding="utf-8") as f:
                f.write(to_write)
    connection.commit()
    return

def add_client(connection):
    name = input("Укажите имя нового клиента:")
    surname = input("Укажите фамилию нового клиента:")
    e_mail = input("Укажите e_mail нового клиента")
    nphone_list = []
    control = True
    while control:
        nphone = (input("Укажите номер телефона клиента:"))
        if nphone == "":
            control = False
        else:
            nphone_list.append(nphone)
    with connection.cursor() as cur:
        cur.execute(f"""
                    INSERT INTO personality(name, surname, e_mail)
                    VALUES ('{name}', '{surname}', '{e_mail}') RETURNING id;
                    """)
        num_id = cur.fetchone()[0]
        for i in nphone_list:
            cur.execute(f"""
                        INSERT INTO person_phone(number_phone, e_mail_id)
                        VALUES ('{i}', '{num_id}') RETURNING id;
                        """)
    connection.commit()
    return

def add_some_else_phones(connection):
    with connection.cursor() as cur:
        cur.execute("""SELECT * from personality;""")
        print(*cur.fetchall(), sep='\n')
    men_id = input("Укажите id из списка выше: ")
    nphone_list = []
    control = True
    while control:
        nphone = (input("Укажите номер телефона клиента:"))
        if nphone == "":
            control = False
        else:
            nphone_list.append(nphone)
    for i in nphone_list:
        with connection.cursor() as cur:
            cur.execute(f"""
                            INSERT INTO person_phone(number_phone, e_mail_id)
                            VALUES ('{i}', '{men_id}') RETURNING id;
                            """)
    connection.commit()
    return

def change_personality(connection):
    print('id', 'e_mail', 'name', 'surname', sep='|')
    with connection.cursor() as cur:
        cur.execute("""SELECT * from personality;""")
        print(*cur.fetchall(), sep='\n')
    men_id = input("Укажите id из списка выше: ")
    canged = input("Укажите название изменяемого поля, кроме ключа: ")
    new_set = input("Укажите новое значение: ")
    with connection.cursor() as cur:
            cur.execute(f"""UPDATE personality SET {canged} = '{new_set}' WHERE id = {men_id}
                            """)
    connection.commit()
    return

def find_client(connection):
    print('id','name', 'surname', 'e_mail' 'number_phone', sep='|')
    with connection.cursor() as cur:
        cur.execute("""select e_mail_id, name, surname, e_mail, number_phone from person_phone pp 
                        join personality p on pp.e_mail_id = p.id;""")
        exist = cur.fetchall()
        print(*exist, sep='\n')
        param = input("Укажите искомое значение: ")
        print('id','name', 'surname', 'e_mail' 'number_phone', sep='|')
        for i in exist:
            if param in i:
                print(i)
    return

def delete_number(connection):
    find_client(connection)
    deleted_number = input("Укажите номер для удаления: ")
    with connection.cursor() as cur:
        cur.execute(f"""DELETE FROM person_phone WHERE number_phone='{deleted_number}';
        """)
    connection.commit()
    return

def delete_personality(connection):
    find_client(connection)
    deleted_number = input("Укажите e_mail для удаления клиента: ")
    with connection.cursor() as cur:
        cur.execute(f"""DELETE FROM personality WHERE e_mail='{deleted_number}';
        """)
    connection.commit()
    return



if __name__ == '__main__':
    pass
    

#give_me_folders_name()
#delete_table(connection, input("Укажите имена папок для удаления через запятую с пробелом: "))
#create_table(connection, 'personality')
#create_table(connection, 'person_phone')
#add_client(connection)
#add_some_else_phones(connection)
#change_personality(connection)
#find_client(connection)
#delete_number(connection)

connection.close()

'''
ДАННЫЕ ДЛЯ СОЗДАНИЯ ТАБЛИЦ
id SERIAL PRIMARY KEY, e_mail VARCHAR (60) NOT NULL, name VARCHAR (60) NOT NULL, surname VARCHAR (60) NOT NULL
id SERIAL PRIMARY KEY,e_mail_id INTEGER references personality(id), number_phone VARCHAR(10) ON DELETE CASCADE
'''

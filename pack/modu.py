"""
這個模組提供了管理資料庫存儲用戶帳戶和書籍記錄的功能。
它包括將CSV和JSON文件轉換為字典的功能，創建資料庫及用戶和書籍表的功能，
將數據從'user.csv'和'books.json'插入到相應表中，執行表的CRUD操作的功能，以及允許用戶安全登錄的功能。

函數：

1. csv_to_dict(file_path: str) -> dict:
   將CSV文件轉換為字典列表，其中每個字典表示CSV文件中的一行。

2. json_to_dict(file_path: str) -> dict:
   將JSON文件轉換為包含JSON數據的字典。

3. creat_data_sheet(db_name: str) -> None:
   創建資料庫和用戶以及書籍的表，並將'user.csv'和'books.json'中的數據插入相應的表中。

4. check_and_create_db(db_name: str) -> None:
   檢查資料庫是否存在，如果不存在則創建資料庫。

5. compare_user_accounts(db_name: str, account: str, password: str) -> bool:
   檢查帳戶是否存在於資料庫的用戶表中，並驗證提供的密碼。

6. log_in(db_name: str) -> bool:
   實現安全登錄功能，允許用戶使用其帳戶憑據登錄。

7. print_menu() -> None:
   打印一個用於管理資料表的CRUD操作的菜單。

8. add_records(db_name: str, title: str, author: str, publisher: str,
               year: int) -> None:
   將一條新的記錄添加到資料庫中的書籍表中。

9. del_records(db_name: str, title: str) -> None:
   根據提供的標題從資料庫的書籍表中刪除記錄。

10. revision_records(db_name: str, title: str, new_title: str, author: str,
                     publisher: str, year: int) -> None:
    根據提供的標題修改資料庫中的書籍表中的記錄。

11. query_records(db_name: str, keyword: str) -> None:
    根據提供的關鍵字（標題或作者）查詢資料庫中的書籍表中的記錄。

12. data_list(db_name: str) -> None:
    打印存儲在資料庫中的書籍記錄的列表。
"""
# 使用ChatGPT生成此模組的docstring

import csv
import os
import sqlite3
import json


# 參考ChatGPT
def csv_to_dict(file_path: str) -> dict:
    '''
    將CSV檔案轉換為字典列表。

    參數:
        file_path (str): CSV檔案的路徑。

    返回值:
        list of dict: 包含字典的列表，每個字典代表CSV檔案中的一行。
    '''
    csv_dict = []
    with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # 讀取第一行作為標頭
        for row in reader:
            user_dict = {}  # 創建一個新的空字典
            for i, value in enumerate(row):
                user_dict[headers[i]] = value  # 將每個標頭和對應的值添加到字典中
            csv_dict.append(user_dict)  # 將該字典添加到列表中
    return csv_dict


def json_to_dict(file_path: str) -> dict:
    '''
    將JSON檔案轉換為字典。

    參數:
        file_path (str): JSON檔案的路徑。

    返回值:
        dict: 包含JSON資料的字典。
    '''
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def creat_data_sheet(db_name: str) -> None:
    """
    建立資料庫並建立用戶和書籍資料表。

    參數:
    - db_name (str): 資料庫名稱。

    返回值:
    - None

    函數內容:
    - 創建新的資料庫。
    - 創建名為 'users' 和 'books' 的資料表。
    - 將 'user.csv' 中的數據插入 'users' 表格。
    - 將 'books.json' 中的數據插入 'books' 表格。
    """
    users_dict = csv_to_dict('user.csv')
    books_dict = json_to_dict('books.json')
    # 如果資料庫不存在，則建立一個新的數據庫
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # 建立users資料表

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
    ''')

    # 建立books資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publisher TEXT NOT NULL,
            year INTEGER NOT NULL
        );
    ''')

    # insert users_data
    for user in users_dict:
        try:
            cursor.execute(
                "INSERT INTO users(username, password) VALUES (?, ?);",
                (
                    user['username'],
                    user['password']
                )
            )
            conn.commit()
        except sqlite3.Error as error:
            print(f"執行 INSERT 操作時發生錯誤：{error}")

    # insert books_data
    for book in books_dict:
        try:
            cursor.execute(
                """INSERT INTO books(title, author, publisher, year)
                VALUES (?, ?, ?, ?);""",
                (
                    book['title'],
                    book['author'],
                    book['publisher'],
                    book['year']
                )
            )
            conn.commit()
        except sqlite3.Error as error:
            print(f"執行 INSERT 操作時發生錯誤：{error}")

    conn.close()


def check_and_create_db(db_name: str) -> None:
    '''
    確認資料庫是否存在，若不存在則建立資料庫。

    參數:
        db_name (str): 資料庫名稱。

    返回值:
        None
    '''
    if not os.path.exists(db_name):
        creat_data_sheet(db_name)


def compare_user_accounts(db_name: str, account: str, password: str) -> bool:
    '''
    判斷帳戶是否存在於資料庫中的使用者資料表，並檢查提供的密碼是否與帳戶的密碼匹配。

    參數:
        db_name (str): 資料庫名稱。
        account (str): 要比較的帳戶名稱。
        password (str): 要比較的密碼。

    返回值:
        bool: 如果帳戶存在且密碼匹配，則返回True；否則返回False。
    '''
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    result_all = cursor.fetchall()
    for row in result_all:
        if row[1] == account and row[2] == password:
            return True
    return False


def log_in(db_name: str) -> bool:
    """
    登入功能，檢查帳號及密碼並進行登入操作。

    參數:
        db_name (str): 資料庫名稱。

    返回值:
        bool: 登入成功則返回True，否則返回False。

    Raises:
        ValueError: 帳號或密碼為空時引發。
        AssertionError: 登入次數超過三次時引發。
    """

    count = 0
    while count < 3:
        account = input('請輸入帳號：')
        password = input('請輸入密碼：')
        if account == '' or password == '':
            raise ValueError('帳號或密碼不可為空')

        if compare_user_accounts(db_name, account, password):
            break
        count += 1
    assert count < 3, "登入次數超過三次"
    return True


def print_menu() -> None:
    """
    輸出功能選單。

    返回值:
        None
    """
    print(f"\n{'-' * 19}\n{'資料表 CRUD':^16}\n{'-' * 19}")

    print('{:^16}\n{:^16}\n{:^16}\n{:^16}\n{:^16}\n{}'
          .format("1. 增加記錄",
                  "2. 刪除記錄",
                  "3. 修改記錄",
                  "4. 查詢記錄",
                  "5. 資料清單",
                  "-" * 19))


def add_records(db_name: str, title: str, author: str, publisher: str,
                year: int) -> None:
    """
    向書籍資料表中新增一條記錄。

    參數:
        db_name (str): 資料庫名稱。
        title (str): 書籍標題。
        author (str): 書籍作者。
        publisher (str): 書籍出版商。
        year (int): 書籍出版年份。

    返回值:
        None

    Raises:
        ValueError: 如果提供的標題、作者、出版商或年份為空字符串，則引發。
        ValueError: 如果年份無法轉換為整數，則引發。
    """
    if title == '' or author == '' or publisher == '' or year == '':
        raise ValueError('=>給定的條件不足，無法進行新增作業')

    # 只有year需要被判斷 因為所有的輸入皆可被判定為字串 但不是所有型別都可以被轉為整數
    try:
        year = int(year)
    except ValueError as ve:
        raise ValueError('year 必須是整數') from ve
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO books(title, author, publisher, year)
        VALUES (?, ?, ?, ?);""",
        (title, author, publisher, year)
    )

    print(f"異動 {cursor.rowcount} 記錄")
    conn.commit()
    data_list(db_name)

    cursor.close()
    conn.close()


def del_records(db_name: str, title: str) -> None:
    """
    從books資料表中刪除符合標題的記錄。

    參數:
        db_name (str): 資料庫名稱。
        title (str): 要刪除的書籍標題。

    返回值:
        None

    Raises:
        ValueError: 如果提供的標題為空字符串，則引發。
    """
    if title == '':
        raise ValueError('=>給定的條件不足，無法進行刪除作業')

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM books WHERE title=?;", (title,))
        print(f"異動 {cursor.rowcount} 記錄")
        conn.commit()
    except sqlite3.Error as error:
        print(f"執行 DELETE 操作時發生錯誤：{error}")
    else:
        data_list(db_name)
    conn.close()


def revision_records(db_name: str, title: str, new_title: str, author: str,
                     publisher: str, year: int) -> None:
    """
    修改書籍資料表中符合標題的記錄。

    參數:
        db_name (str): 資料庫名稱。
        title (str): 要修改的書籍標題。
        new_title (str): 新的書籍標題。
        author (str): 新的書籍作者。
        publisher (str): 新的書籍出版商。
        year (int): 新的書籍出版年份。

    返回值:
        None

    Raises:
        ValueError: 如果提供的標題、新標題、作者、出版商或年份為空字符串，則引發。
        ValueError: 如果年份無法轉換為整數，則引發。
    """
    if title == '' or new_title == '' or author == '' or publisher == '' or year == '':
        raise ValueError('=>給定的條件不足，無法進行修改作業')

    try:
        year = int(year)
    except ValueError as ve:
        raise ValueError('year 必須是整數') from ve
    # 以上try except參考ChatGPT

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""UPDATE books SET title=?, author=?, publisher=?,year=?
                   WHERE title=?;""",
                   (new_title, author, publisher, year, title))
    print(f"異動 {cursor.rowcount} 記錄")
    conn.commit()
    data_list(db_name)

    conn.close()


def query_records(db_name: str, keyword: str) -> None:
    """
    根據關鍵字在書籍資料表中查詢符合標題或作者的記錄。

    參數:
        db_name (str): 資料庫名稱。
        keyword (str): 查詢關鍵字。

    返回值:
        None
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT title, author, publisher, year FROM books
                        WHERE title LIKE ? OR author LIKE ?;""",
                       ('%' + keyword + '%', '%' + keyword + '%'))
        datas = cursor.fetchall()
    except sqlite3.Error as error:
        print(f"執行 SELECT 操作時發生錯誤：{error}")
    finally:
        cursor.close()
        conn.close()

    if len(datas) > 0:
        print(
                f'|{'書名':{chr(12288)}^10}|'
                f'{'作者':{chr(12288)}^10}|'
                f'{'出版社':{chr(12288)}^10}|'
                f'{'年份':{chr(12288)}^4}|'
            )
        for data in datas:
            print(
                f'|{data[0]:{chr(12288)}<10}|'
                f'{data[1]:{chr(12288)}<10}|'
                f'{data[2]:{chr(12288)}<10}|'
                f'{data[3]:{chr(12288)}<6}|'
                )
    else:
        print("查無資料")
    conn.close()


def data_list(db_name: str) -> None:
    """
    輸出書籍資訊。

    參數:
        db_name (str): 資料庫名稱。

    返回值:
        None
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM books")
        datas = cursor.fetchall()
    except sqlite3.Error as error:
        print(f"執行 SELECT 操作時發生錯誤：{error}")
    else:
        if len(datas) > 0:
            print(
                f'|{'書名':{chr(12288)}^10}|'
                f'{'作者':{chr(12288)}^10}|'
                f'{'出版社':{chr(12288)}^10}|'
                f'{'年份':{chr(12288)}^4}|'
            )
            for data in datas:
                print(
                    f'|{data[1]:{chr(12288)}<10}|'
                    f'{data[2]:{chr(12288)}<10}|'
                    f'{data[3]:{chr(12288)}<10}|'
                    f'{data[4]:{chr(12288)}<6}|'
                    )
        else:
            print("查無資料")

import pack.modu as lib

DB_NAME = 'library.db'

if __name__ == '__main__':

    logging_in = False

    lib.check_and_create_db(DB_NAME)

    # 帳號登入
    while True:
        try:
            logging_in = lib.log_in(DB_NAME)
        except AssertionError as ae:
            print(ae)
            break
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print(e)
        else:
            break

    while logging_in:
        lib.print_menu()
        choose = input("選擇要執行的功能(Enter離開)：")
        if choose == '1':
            try:
                title = input('請輸入要新增的標題：')
                author = input('請輸入要新增的作者：')
                publisher = input('請輸入要新增的出版社：')
                year = input('請輸入要新增的年份：')
                lib.add_records(DB_NAME, title, author, publisher, year)
            except ValueError as e:
                print(e)
            except Exception as e:
                print(e)

        elif choose == '2':
            lib.data_list(DB_NAME)
            try:
                title = input('請問要刪除哪一本書？：')
                lib.del_records(DB_NAME, title)
            except ValueError as ve:
                print(ve)

        elif choose == '3':
            try:
                lib.data_list(DB_NAME)
                title = input('請問要修改哪一本書的標題？：')
                new_title = input('請輸入要更改的標題：')
                author = input('請輸入要更改的作者：')
                publisher = input('請輸入要更改的出版社：')
                year = input('請輸入要更改的年份：')
                lib.revision_records(DB_NAME, title, new_title, author, publisher, year)
            except ValueError as va:
                print(va)

        elif choose == '4':
            keyword = input('請輸入想查詢的關鍵字：')
            lib.query_records(DB_NAME, keyword)

        elif choose == '5':
            lib.data_list(DB_NAME)

        elif choose == '':
            break

        else:
            print('=>無效的選擇')

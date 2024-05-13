import psycopg2
import pandas as pd
import socket
def get_sales_data_f():
    # Импорт параметров БД
    df_db = pd.read_csv('db.csv',delimiter=';')
    # При обращение к хосту из контейнера имя хоста указывается вдругом виде
    if socket.gethostname()[-5:] == 'local':
        host = df_db.loc[0,'host']
    # jenkins
    else: host = df_db.loc[0,'host2']
    # Соединение
    with psycopg2.connect(dbname=df_db.loc[0,'dbname'], user=df_db.loc[0,'user'],
                            password=df_db.loc[0,'password'], host=host) as conn:
        loads = set(df_filters['load_num'])
        df_sales = pd.DataFrame()
        for load in loads:
            df_cur_load = df_filters[df_filters['load_num'] == load]
            df_days = df_cur_load[df_cur_load['load_field'] == 'DAY']
            dates = tuple(df_days['value'])
            df_stores = df_cur_load[df_cur_load['load_field'] == 'STORE']
            stores = tuple(df_stores['value'])
            sql = "SELECT date, store_nbr, sum(sales) as sales FROM public.\"SALES\" where date in %s and store_nbr in %s group by date, store_nbr"
            df_sql = pd.read_sql(sql, conn, params=[dates, stores])
            df_sales = df_sales._append(df_sql, ignore_index = True )
        return df_sales


if __name__ == "__main__":
    df_filters = pd.read_csv('filters/filter.csv')
    df_sales_data = get_sales_data_f()
    print(df_sales_data)






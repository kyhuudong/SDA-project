import csv
import psycopg2
from sql_queries import *  


def csv_data(file_path):
    row_count = 0
    city_data = []
    year_data = []
    file_data = []
    with open('data_source/'+file_path+'.csv', encoding='utf-8') as f:
        data = csv.reader(f)
        row_count = sum(1 for row in data)
        #print(row_count)
    with open('data_source/'+file_path+'.csv', encoding='utf-8') as a:
        data = csv.reader(a)
        i = 0
        row_split = []
        for row in data:      
            if i == 2:
                row_split = row[0].split(';')
                for j in range(len(row_split)):
                    year_data.append(row_split[j][1:5]) if row_split[j] != '" "' else year_data.append('') 
            if i >= 4 and i < row_count:
                row_split = row[0].split(';')
                print(str(i-3)+'---Extracted Line')
                #print(row) 
                city_data.append(row_split[0])     
                file_data.append(row_split[1:len(row[0].split(';'))]) 
            i+=1
        return city_data, year_data[-8:], file_data



def load_data_into_staging_tables(conn, cur, data_source, table_name):
    city_data, year_data, file_data = data_source   
    temp = []
    year = year_data
    city = city_data
   
    #print(len(file_data))
    #print(len(city))
    try:
        for i in range(len(city)):
            data = file_data[i][-8:]
            for k in range(len(data)):
                temp.append(city[i])
                temp.append(year[k]) 
                temp.append(data[k])
                cur.execute(table_name, temp)
                conn.commit()
                #print(city[i]+' '+year[k]+' '+data[k]+' '+' '.join(temp))
                temp = []
            print(str(i+1)+'/'+str(len(city))+" Inserted line -------------", city[i])
        print("===============================Insert successfully")
    except psycopg2.Error as e:
        print(e) 



def load_domain(conn, cur, data_source, table_name):
    city_data, year_data, file_data = data_source
    temp = []
    year = year_data
    city = city_data
    checker = None
    try:
        for i in range(len(city)):
            data = file_data[i][-8:]
            for k in range(len(data)):
                temp.append(data[k])
                temp.append(city[i])
                if year[k] != '':
                    temp.append(year[k])
                else: 
                    checker = False

                #Check
                if checker != False:   
                    cur.execute(table_name, temp)
                    conn.commit()
                    #print(data[k]+' '+city[i]+' '+year[k]+' '+' '.join(temp))
                temp = []
                checker = None
            print("Inserted domain line -------------",str(i+1)+'/'+str(len(city))+' '+city[i])
        print("===============================Insert domain successfully")
 
    except psycopg2.Error as e:
        print(e)



def insert_table(conn, cur, dim):
    try:
        cur.execute(dim)
        conn.commit()
        print("Insert into tables successfully")
    except psycopg2.Error as e:
        print(e)
        print("Insert failed")





def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=smartdashboard user=postgres password=846213579")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    print('------------------------------------')
    
    #data_soure them csv_data o duoi va ` insert them query vao 
    data_sources = ['source_afforestation', 'source_humidity', 'source_population', 'source_industry']
    domain_sources = ['source_rainfall', 'source_temperature', 'source_forestcover']
    for query, data in zip(insert_table_queries, data_sources):
        load_data_into_staging_tables(conn, cur, csv_data(data), query)
    
    print('------------------------------------')
    print('------------------------------------')
    print('------------------------------------')
    for domain_queries ,data in zip(insert_domain, domain_sources):
        load_domain(conn, cur, csv_data(data), domain_queries)
    print('------------------------------------')
    print('------------------------------------')
    print('------------------------------------')
    for dim_queries in insert_tables:
        insert_table(conn, cur, dim_queries)
        
    cur.close() 
    conn.close()
    print('----------------DONE----------------')
#

if __name__ == "__main__":
    main()



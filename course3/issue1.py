import csv
import mysql.connector
from datetime import datetime


class MySQLHelper:
    def __init__(self, host, port, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            port=port,  # 포트 명시
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def insert_weather(self, mars_date, temp, storm):
        query = (
            'INSERT INTO mars_weather (mars_date, temp, storm) '
            'VALUES (%s, %s, %s)'
        )
        values = (mars_date, temp, storm)
        self.cursor.execute(query, values)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


def read_csv(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 헤더 건너뜀
        for row in reader:
            mars_date = datetime.strptime(row[1], '%Y-%m-%d')
            temp = float(row[2])
            storm = int(row[3])
            data.append((mars_date, temp, storm))
    return data


def insert_data(data):
    db_helper = MySQLHelper(
        host='localhost',
        port=3307,  # 여기에서 포트 설정
        user='root',
        password='root',  # 본인의 MySQL 비밀번호로 수정
        database='mars'
    )

    for row in data:
        mars_date, temp, storm = row
        db_helper.insert_weather(mars_date, temp, storm)

    db_helper.commit()
    db_helper.close()


def main():
    file_path = 'course3/mars_weathers_data.csv'  # 실제 파일 경로로 수정
    data = read_csv(file_path)
    insert_data(data)
    print('CSV 데이터가 성공적으로 삽입되었습니다.')


if __name__ == '__main__':
    main()

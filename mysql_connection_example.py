"""
Python MySQL 데이터베이스 연결 예제

필요한 라이브러리 설치:
pip install mysql-connector-python
pip install PyMySQL
pip install mysqlclient
"""

import mysql.connector
import pymysql
from contextlib import contextmanager

# =============================================================================
# 1. mysql-connector-python 사용 예제 (공식 MySQL 라이브러리)
# =============================================================================

def mysql_connector_example():
    """mysql-connector-python을 사용한 MySQL 연결 예제"""
    try:
        # 데이터베이스 연결
        conn = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database',
            charset='utf8mb4'
        )
        
        cursor = conn.cursor()
        
        # SELECT 쿼리
        cursor.execute("SELECT * FROM users LIMIT 5")
        results = cursor.fetchall()
        print("조회 결과:")
        for row in results:
            print(row)
        
        # INSERT 쿼리
        insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        user_data = ("John Doe", "john@example.com")
        cursor.execute(insert_query, user_data)
        conn.commit()
        print(f"새 사용자 추가됨. ID: {cursor.lastrowid}")
        
        # UPDATE 쿼리
        update_query = "UPDATE users SET email = %s WHERE name = %s"
        cursor.execute(update_query, ("newemail@example.com", "John Doe"))
        conn.commit()
        print(f"업데이트된 행 수: {cursor.rowcount}")
        
        # DELETE 쿼리
        delete_query = "DELETE FROM users WHERE name = %s"
        cursor.execute(delete_query, ("John Doe",))
        conn.commit()
        print(f"삭제된 행 수: {cursor.rowcount}")
        
    except mysql.connector.Error as err:
        print(f"MySQL 오류: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("MySQL 연결이 종료되었습니다.")

# =============================================================================
# 2. PyMySQL 사용 예제
# =============================================================================

def pymysql_example():
    """PyMySQL을 사용한 MySQL 연결 예제"""
    try:
        # 데이터베이스 연결
        conn = pymysql.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor  # 딕셔너리 형태로 결과 반환
        )
        
        with conn.cursor() as cursor:
            # SELECT 쿼리
            cursor.execute("SELECT * FROM users LIMIT 5")
            results = cursor.fetchall()
            print("조회 결과 (딕셔너리 형태):")
            for row in results:
                print(row)
            
            # INSERT 쿼리
            insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
            cursor.execute(insert_query, ("Jane Smith", "jane@example.com"))
        
        # 변경사항 커밋
        conn.commit()
        print("데이터가 성공적으로 삽입되었습니다.")
        
    except pymysql.Error as err:
        print(f"PyMySQL 오류: {err}")
        conn.rollback()
    finally:
        conn.close()
        print("PyMySQL 연결이 종료되었습니다.")

# =============================================================================
# 3. Context Manager를 사용한 안전한 연결 관리
# =============================================================================

@contextmanager
def get_mysql_connection():
    """Context Manager를 사용한 MySQL 연결 관리"""
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database',
            charset='utf8mb4'
        )
        yield conn
    except mysql.connector.Error as err:
        print(f"MySQL 연결 오류: {err}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def context_manager_example():
    """Context Manager를 사용한 예제"""
    try:
        with get_mysql_connection() as conn:
            cursor = conn.cursor()
            
            # 안전한 쿼리 실행
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"총 사용자 수: {count}")
            
            cursor.close()
    except Exception as e:
        print(f"오류 발생: {e}")

# =============================================================================
# 4. 연결 풀(Connection Pool) 사용 예제
# =============================================================================

def connection_pool_example():
    """Connection Pool을 사용한 예제"""
    from mysql.connector import pooling
    
    # 연결 풀 설정
    config = {
        'user': 'your_username',
        'password': 'your_password',
        'host': 'localhost',
        'database': 'your_database',
        'charset': 'utf8mb4',
        'raise_on_warnings': True
    }
    
    try:
        # 연결 풀 생성
        pool = pooling.MySQLConnectionPool(
            pool_name="mypool",
            pool_size=5,
            **config
        )
        
        # 풀에서 연결 가져오기
        conn = pool.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"MySQL 버전: {version}")
        
        cursor.close()
        conn.close()  # 풀로 반환
        
    except Exception as e:
        print(f"Connection Pool 오류: {e}")

# =============================================================================
# 5. 설정 파일을 사용한 연결 관리
# =============================================================================

def config_file_example():
    """설정 파일을 사용한 연결 예제"""
    import configparser
    
    # config.ini 파일 형태:
    # [mysql]
    # host = localhost
    # user = your_username
    # password = your_password
    # database = your_database
    
    config = configparser.ConfigParser()
    # config.read('config.ini')  # 실제 설정 파일 경로
    
    # 예제용 설정
    config['mysql'] = {
        'host': 'localhost',
        'user': 'your_username',
        'password': 'your_password',
        'database': 'your_database'
    }
    
    try:
        conn = mysql.connector.connect(**config['mysql'])
        print("설정 파일을 사용한 연결 성공")
        conn.close()
    except Exception as e:
        print(f"설정 파일 연결 오류: {e}")

# =============================================================================
# 메인 실행 부분
# =============================================================================

if __name__ == "__main__":
    print("=== Python MySQL 연결 예제 ===\n")
    
    print("사용하기 전에 다음을 설정하세요:")
    print("1. MySQL 서버가 실행 중인지 확인")
    print("2. 데이터베이스와 테이블 생성")
    print("3. 사용자 계정과 권한 설정")
    print("4. 연결 정보 수정 (host, user, password, database)")
    print("\n" + "="*50 + "\n")
    
    # 각 예제 함수들을 주석 해제하여 실행
    # mysql_connector_example()
    # pymysql_example()
    # context_manager_example()
    # connection_pool_example()
    # config_file_example()
    
    print("예제 코드를 실행하려면 해당 함수의 주석을 해제하세요.")
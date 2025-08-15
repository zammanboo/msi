import pandas as pd
from datetime import datetime
import sys

def generate_time_range(start_time_str, end_time_str, node_name):
    """
    시간 범위와 노드명을 받아서 1분 단위로 "시간, 노드명"을 출력
    
    Args:
        start_time_str (str): 시작 시간 "YYYY-MM-DD HH:MM" 형식
        end_time_str (str): 종료 시간 "YYYY-MM-DD HH:MM" 형식
        node_name (str): GPU 노드명
    """
    # 문자열을 datetime 객체로 변환
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")
    
    # pandas를 사용해 1분 간격으로 시간 범위 생성
    time_range = pd.date_range(start=start_time, end=end_time, freq='1min')
    
    # 각 시간에 대해 "시간, 노드명" 형식으로 출력
    for timestamp in time_range:
        formatted_time = timestamp.strftime("%Y-%m-%d %H:%M")
        print(f"{formatted_time}, {node_name}")

def main():
    if len(sys.argv) != 4:
        print("사용법: python time_range_generator.py '시작시간' '종료시간' '노드명'")
        print("예시: python time_range_generator.py '2025-08-15 07:01' '2025-08-15 07:25' 'gpu01'")
        return
    
    start_time = sys.argv[1]
    end_time = sys.argv[2]
    node_name = sys.argv[3]
    
    try:
        generate_time_range(start_time, end_time, node_name)
    except ValueError as e:
        print(f"시간 형식 오류: {e}")
        print("올바른 형식: 'YYYY-MM-DD HH:MM'")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
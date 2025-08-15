import pandas as pd

def process_gpu_data(csv_file_path):
    """
    CSV 파일을 읽어서 '시간 gpu노드값 gpu노드이름' 형태로 출력
    
    Args:
        csv_file_path (str): CSV 파일 경로
    """
    # CSV 파일 읽기
    df = pd.read_csv(csv_file_path)
    
    # 시간 열을 제외한 GPU 노드 열들 추출
    time_column = df.columns[0]  # 첫 번째 열이 시간 열
    gpu_columns = df.columns[1:]  # 나머지 열들이 GPU 노드 열들
    
    # 각 행에 대해 처리
    for index, row in df.iterrows():
        time_value = row[time_column]
        
        # 각 GPU 노드에 대해 출력
        for gpu_node in gpu_columns:
            gpu_value = row[gpu_node]
            print(f"{time_value} {gpu_value} {gpu_node}")

# 사용 예시
if __name__ == "__main__":
    # CSV 파일 경로를 지정하세요
    import sys
    csv_file_path = sys.argv[1]
    
    try:
        process_gpu_data(csv_file_path)
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {csv_file_path}")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

import datetime
import os

def record_build_date():
    # 현재 스크립트의 디렉토리 경로 얻기
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(script_dir, 'build_date.txt')
    
    # 현재 작업 디렉토리 출력
    print(f"현재 작업 디렉토리: {script_dir}")
    
    # 파일이 존재하는지 확인
    if not os.path.exists(file_name):
        print(f"{file_name} 파일이 없습니다. 새로 생성합니다.")
    
    # 현재 시간 가져오기
    current_time = datetime.datetime.now().strftime('%Y.%m.%d')
    
    # 현재 시간을 build_date.txt 파일에 쓰기
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(current_time)

    print(f"현재 시간이 {file_name} 파일에 기록되었습니다: {current_time}")

record_build_date()
import tkinter as tk
import subprocess
import threading
import os
import sys
import py7zr
import shutil
from tkinter import messagebox, filedialog, StringVar, Label, Entry, Button, OptionMenu

# 다운로드 링크
drive_link = "https://drive.google.com/uc?id="
file_links = {
    "로로나의 아틀리에 DX": drive_link + "144qax7CARxAoMuDe_K4kF_zsgoTGb_qa",
    "토토리의 아틀리에 DX": drive_link + "16hRiKkMgaWBe2yTZ5rlAeTK-w2IxfUyD",
    "메루루의 아틀리에 DX": drive_link + "19pdqLQTmPPLC2bWZUqLWylDdxcT6BjDC",
    "아샤의 아틀리에 DX": drive_link + "1eTGP2EuMh7GJf4ux8vKz4656Lu5EAPV5",
    "에스카&로지의 아틀리에 DX": drive_link + "1_3Y46qfxo2xykbMTqjBSn8r6jLTRpLsc",
    "샤리의 아틀리에 DX": drive_link + "1Tmq6sCZXWxZd6Ul-kF0n60P1Gh08YTFA",
    "소피의 아틀리에 DX": drive_link + "1-tucaRZO-i5e5Qlib22I0ETUfAPTGneD",
    "피리스의 아틀리에 DX": drive_link + "1fvWOAWj-QaHBWkMTEGrFP_MnTmiw73sM",
    "리디&수르의 아틀리에 DX": drive_link + "1jcqTVOwAZ_KQEv4wsi3lc4j58N7vLdMx",
    "네르케와 전설의 연금술사들": drive_link + "1_AWyuKzAoVU6-gi2YG1vRftjyD7zRAzg",
    "루루아의 아틀리에": drive_link + "1QrPAt4pAVa_H_lmIUSzdBVlzvw_BcpHV",
    "라이자의 아틀리에": drive_link + "1dBHaAt-hCLVdhGmXlMq0Or1z8le2iD3f",
}

# 클래스 정의: 터미널 출력을 GUI Text 위젯으로 리디렉션
class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        #self.text_widget.see(tk.END)  # 자동 스크롤

    def flush(self):
        pass  # 표준 출력 스트림과의 호환성 위해 flush 메서드 구현

def select_directory():
    """사용자가 경로를 선택하도록 하고 선택한 경로를 표시"""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        game_path.set(folder_selected)

# 다운로드 및 압축 해제 함수
def download_file(file_name, url):
    try:
        if not game_path.get():  # game_path가 비어 있는지 확인
            messagebox.showerror("오류", "스팀 라이브러리 경로를 지정해주세요")  # 오류 메시지 표시
        elif not game_path.get().endswith("steamapps/common"):  # steamapps/common으로 끝나는지 확인
            messagebox.showerror("오류", "스팀 라이브러리 경로가 유효하지 않습니다.\n...\\steamapps\\common 폴더를 지정해주세요.")
        else:
            if file_name == "로로나의 아틀리에 DX":
                path = os.path.join(game_path.get(), "Atelier Rorona ~The Alchemist of Arland~ DX")  # 게임 설치 경로
                 # 설치된 경로가 존재하는지 확인
                if not os.path.exists(path):
                    messagebox.showerror("오류", f"{file_name}가 설치되지 않았습니다.\n스팀 라이브러리 경로를 다시 한 번 확인해주세요.")
                    return  # 설치되지 않은 경우 함수 종료
            elif file_name == "토토리의 아틀리에 DX":
                path = os.path.join(game_path.get(), "Atelier Totori ~The Adventurer of Arland~ DX")  # 게임 설치 경로
                 # 설치된 경로가 존재하는지 확인
                if not os.path.exists(path):
                    messagebox.showerror("오류", f"{file_name}가 설치되지 않았습니다.\n스팀 라이브러리 경로를 다시 한 번 확인해주세요.")
                    return  # 설치되지 않은 경우 함수 종료
            elif file_name == "메루루의 아틀리에 DX":
                path = os.path.join(game_path.get(), "Atelier Meruru ~The Apprentice of Arland~ DX")  # 게임 설치 경로
                 # 설치된 경로가 존재하는지 확인
                if not os.path.exists(path):
                    messagebox.showerror("오류", f"{file_name}가 설치되지 않았습니다.\n스팀 라이브러리 경로를 다시 한 번 확인해주세요.")
                    return  # 설치되지 않은 경우 함수 종료
            elif file_name == "아샤의 아틀리에 DX":
                path = os.path.join(game_path.get(), "Atelier Ayesha DX")  # 게임 설치 경로
                 # 설치된 경로가 존재하는지 확인
                if not os.path.exists(path):
                    messagebox.showerror("오류", f"{file_name}가 설치되지 않았습니다.\n스팀 라이브러리 경로를 다시 한 번 확인해주세요.")
                    return  # 설치되지 않은 경우 함수 종료
            elif file_name == "에스카&로지의 아틀리에 DX":
                path = os.path.join(game_path.get(), "Atelier Escha and Logy DX")  # 게임 설치 경로
                 # 설치된 경로가 존재하는지 확인
                if not os.path.exists(path):
                    messagebox.showerror("오류", f"{file_name}가 설치되지 않았습니다.\n스팀 라이브러리 경로를 다시 한 번 확인해주세요.")
                    return  # 설치되지 않은 경우 함수 종료
            elif file_name == "샤리의 아틀리에 DX":
                path = os.path.join(game_path.get(), "Atelier Shallie DX")  # 게임 설치 경로
                 # 설치된 경로가 존재하는지 확인
                if not os.path.exists(path):
                    messagebox.showerror("오류", f"{file_name}가 설치되지 않았습니다.\n스팀 라이브러리 경로를 다시 한 번 확인해주세요.")
                    return  # 설치되지 않은 경우 함수 종료
            elif file_name == "소피의 아틀리에 DX":
                path = os.path.join(game_path.get(), "Atelier Sophie DX")  # 게임 설치 경로
                 # 설치된 경로가 존재하는지 확인
                if not os.path.exists(path):
                    messagebox.showerror("오류", f"{file_name}가 설치되지 않았습니다.\n스팀 라이브러리 경로를 다시 한 번 확인해주세요.")
                    return  # 설치되지 않은 경우 함수 종료
            elif file_name == "피리스의 아틀리에 DX":
                path = os.path.join(game_path.get(), "Atelier Firis DX")  # 게임 설치 경로
                 # 설치된 경로가 존재하는지 확인
                if not os.path.exists(path):
                    messagebox.showerror("오류", f"{file_name}가 설치되지 않았습니다.\n스팀 라이브러리 경로를 다시 한 번 확인해주세요.")
                    return  # 설치되지 않은 경우 함수 종료
            elif file_name == "리디&수르의 아틀리에 DX":
                path = os.path.join(game_path.get(), "Atelier Lydie and Suelle DX")  # 게임 설치 경로
                 # 설치된 경로가 존재하는지 확인
                if not os.path.exists(path):
                    messagebox.showerror("오류", f"{file_name}가 설치되지 않았습니다.\n스팀 라이브러리 경로를 다시 한 번 확인해주세요.")
                    return  # 설치되지 않은 경우 함수 종료
            elif file_name == "네르케와 전설의 연금술사들":
                path = os.path.join(game_path.get(), "Nelke and the Legendary Alchemists Ateliers of the New World")  # 게임 설치 경로
                 # 설치된 경로가 존재하는지 확인
                if not os.path.exists(path):
                    messagebox.showerror("오류", f"{file_name}이 설치되지 않았습니다.\n스팀 라이브러리 경로를 다시 한 번 확인해주세요.")
                    return  # 설치되지 않은 경우 함수 종료
            elif file_name == "루루아의 아틀리에":
                path = os.path.join(game_path.get(), "Atelier Lulua")  # 게임 설치 경로
                 # 설치된 경로가 존재하는지 확인
                if not os.path.exists(path):
                    messagebox.showerror("오류", f"{file_name}가 설치되지 않았습니다.\n스팀 라이브러리 경로를 다시 한 번 확인해주세요.")
                    return  # 설치되지 않은 경우 함수 종료
            elif file_name == "라이자의 아틀리에":
                path = os.path.join(game_path.get(), "Atelier Ryza")  # 게임 설치 경로
                 # 설치된 경로가 존재하는지 확인
                if not os.path.exists(path):
                    messagebox.showerror("오류", f"{file_name}가 설치되지 않았습니다.\n스팀 라이브러리 경로를 다시 한 번 확인해주세요.")
                    return  # 설치되지 않은 경우 함수 종료
        
            download_button.config(state=tk.DISABLED)  # 다운로드 시작 시 버튼 비활성화
            dropdown.config(state=tk.DISABLED)  # 다운로드 시작 시 드롭다운 메뉴 비활성화
            current_dir = os.path.dirname(__file__)  # 현재 파일의 경로
            
            # temp 폴더 경로 설정
            temp_dir = os.path.join(current_dir, 'temp')
            os.makedirs(temp_dir, exist_ok=True)  # temp 폴더 생성 (존재하지 않을 경우)

            # temp 폴더 내에 zip 파일 저장 경로
            save_path = os.path.join(temp_dir, f"{file_name}.7z") 
            
            # gdown 다운로드 명령을 subprocess로 실행
            CREATE_NO_WINDOW = 0x08000000
            command = ['gdown', url, '-O', save_path]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=CREATE_NO_WINDOW)

            # 초기 메시지 출력
            text_output.config(state=tk.NORMAL)  # 입력 가능 상태로 변경
            initial_message = "패치에 필요한 파일을 다운로드하는 중입니다.\n잠시만 기다려주세요...\n"
            text_output.insert(tk.END, initial_message)  # 텍스트 위젯에 초기 메시지 삽입
            text_output.see(tk.END)  # 자동 스크롤

            # 출력 실시간으로 읽어 텍스트 위젯에 표시
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    text_output.delete('2.13', 'end')  # 초기 메시지 이후의 내용을 삭제
                    text_output.insert(tk.END, '\n' + output.strip() + '\n')  # 진행 상태 추가
                    text_output.see(tk.END)  # 자동 스크롤

            process.wait()
            print("다운로드가 완료되었습니다.\n압축을 해제하는 중입니다.\n잠시만 기다려주세요...")  # 다운로드 완료 메시지
            
            # 다운로드한 파일의 압축 해제
            with py7zr.SevenZipFile(save_path, mode='r') as archive:
                archive.extractall(path=temp_dir)  # temp 폴더에 내용물 직접 해제
                print("압축 해제가 완료되었습니다.")  # 압축 해제 완료 메시지

            # 압축 해제 후 .7z 파일 삭제
            os.remove(save_path)
            print("압축 파일을 삭제하였습니다.\n한국어 패치를 적용합니다.")  # 삭제 완료 메시지

            if file_name == "로로나의 아틀리에 DX":
                setup_rorona()
            elif file_name == "토토리의 아틀리에 DX":
                setup_totori()
            elif file_name == "메루루의 아틀리에 DX":
                setup_meruru()
            elif file_name == "아샤의 아틀리에 DX":
                setup_ayesha()
            elif file_name == "에스카&로지의 아틀리에 DX":
                setup_escha()
            elif file_name == "샤리의 아틀리에 DX":
                setup_shallie()
            elif file_name == "소피의 아틀리에 DX":
                setup_sophie()
            elif file_name == "피리스의 아틀리에 DX":
                setup_firis()
            elif file_name == "리디&수르의 아틀리에 DX":
                setup_lydie()
            elif file_name == "네르케와 전설의 연금술사들":
                setup_nelke()
            elif file_name == "루루아의 아틀리에":
                setup_lulua()
            elif file_name == "라이자의 아틀리에":
                setup_ryza()
            
            text_output.config(state=tk.DISABLED)  # 다시 입력 불가능 상태로 변경

    except Exception as e:
        print(f"Error downloading {file_name}: {e}")
    finally:
        download_button.config(state=tk.NORMAL)  # 다운로드 완료 후 버튼 활성화
        dropdown.config(state=tk.NORMAL)  # 다운로드 완료 후 드롭다운 메뉴 활성화

# 각 파일에 대해 다운로드 완료 후 호출할 함수 정의
def setup_rorona():
    path = os.path.join(game_path.get(), "Atelier Rorona ~The Alchemist of Arland~ DX")  # 게임 설치 경로
    realpath = os.path.dirname(__file__)  # 프로그램 실행 경로
    filepath = os.path.join(realpath, "temp")  # 설치 파일 경로

    # 폴더 복사
    for folder in ["Event", "Res"]:
        src_folder = os.path.join(filepath, folder)
        dest_folder = os.path.join(path, folder)
        if os.path.exists(src_folder):
            # 디렉토리가 존재하면 복사
            shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)  # 기존 폴더 덮어쓰기

    # 파일 복사
    for file in ["A11R_x64_Release.exe", "ArlandDX_Settings.ini"]:
        shutil.copy(os.path.join(filepath, file), os.path.join(path, file))

    # 파일 삭제
    temp_folder_path = os.path.join(realpath, "temp")
    if os.path.exists(temp_folder_path):
        shutil.rmtree(temp_folder_path)  # temp 폴더와 그 안의 모든 내용 삭제

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "로로나의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

    clear_text_output()

def setup_totori():
    path = os.path.join(game_path.get(), "Atelier Totori ~The Adventurer of Arland~ DX")  # 게임 설치 경로
    realpath = os.path.dirname(__file__)  # 프로그램 실행 경로
    filepath = os.path.join(realpath, "temp")  # 설치 파일 경로

    # 폴더 복사
    for folder in ["Event", "Res"]:
        src_folder = os.path.join(filepath, folder)
        dest_folder = os.path.join(path, folder)
        if os.path.exists(src_folder):
            # 디렉토리가 존재하면 복사
            shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)  # 기존 폴더 덮어쓰기

    # 파일 복사
    for file in ["A12V_x64_Release.exe", "ArlandDX_Settings.ini"]:
        shutil.copy(os.path.join(filepath, file), os.path.join(path, file))

    # 파일 삭제
    temp_folder_path = os.path.join(realpath, "temp")
    if os.path.exists(temp_folder_path):
        shutil.rmtree(temp_folder_path)  # temp 폴더와 그 안의 모든 내용 삭제

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "토토리의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

    clear_text_output()

def setup_meruru():
    path = os.path.join(game_path.get(), "Atelier Meruru ~The Apprentice of Arland~ DX")  # 게임 설치 경로
    realpath = os.path.dirname(__file__)  # 프로그램 실행 경로
    filepath = os.path.join(realpath, "temp")  # 설치 파일 경로

    # 폴더 복사
    for folder in ["Event", "Res"]:
        src_folder = os.path.join(filepath, folder)
        dest_folder = os.path.join(path, folder)
        if os.path.exists(src_folder):
            # 디렉토리가 존재하면 복사
            shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)  # 기존 폴더 덮어쓰기

    # 파일 복사
    for file in ["A13V_x64_Release.exe", "ArlandDX_Settings.ini"]:
        shutil.copy(os.path.join(filepath, file), os.path.join(path, file))

    # 파일 삭제
    temp_folder_path = os.path.join(realpath, "temp")
    if os.path.exists(temp_folder_path):
        shutil.rmtree(temp_folder_path)  # temp 폴더와 그 안의 모든 내용 삭제

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "메루루의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

    clear_text_output()

def setup_ayesha():
    path = os.path.join(game_path.get(), "Atelier Ayesha DX")  # 게임 설치 경로
    realpath = os.path.dirname(__file__)  # 프로그램 실행 경로
    filepath = os.path.join(realpath, "temp")  # 설치 파일 경로

    # 폴더 복사
    for folder in ["Event", "Res"]:
        src_folder = os.path.join(filepath, folder)
        dest_folder = os.path.join(path, folder)
        if os.path.exists(src_folder):
            # 디렉토리가 존재하면 복사
            shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)  # 기존 폴더 덮어쓰기

    # 파일 복사
    for file in ["Atelier_Ayesha.exe", "Setting.ini"]:
        shutil.copy(os.path.join(filepath, file), os.path.join(path, file))

    # 파일 삭제
    temp_folder_path = os.path.join(realpath, "temp")
    if os.path.exists(temp_folder_path):
        shutil.rmtree(temp_folder_path)  # temp 폴더와 그 안의 모든 내용 삭제

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "아샤의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

    clear_text_output()

def setup_escha():
    path = os.path.join(game_path.get(), "Atelier Escha and Logy DX")  # 게임 설치 경로
    realpath = os.path.dirname(__file__)  # 프로그램 실행 경로
    filepath = os.path.join(realpath, "temp")  # 설치 파일 경로

    # 폴더 복사
    for folder in ["Data", "DLC", "Event", "Saves"]:
        src_folder = os.path.join(filepath, folder)
        dest_folder = os.path.join(path, folder)
        if os.path.exists(src_folder):
            # 디렉토리가 존재하면 복사
            shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)  # 기존 폴더 덮어쓰기

    # 파일 복사
    for file in ["Atelier_Escha_and_Logy.exe", "Setting.ini"]:
        shutil.copy(os.path.join(filepath, file), os.path.join(path, file))

    # 파일 삭제
    temp_folder_path = os.path.join(realpath, "temp")
    if os.path.exists(temp_folder_path):
        shutil.rmtree(temp_folder_path)  # temp 폴더와 그 안의 모든 내용 삭제

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "에스카&로지의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

    clear_text_output()

def setup_shallie():
    path = os.path.join(game_path.get(), "Atelier Shallie DX")  # 게임 설치 경로
    realpath = os.path.dirname(__file__)  # 프로그램 실행 경로
    filepath = os.path.join(realpath, "temp")  # 설치 파일 경로

    # 폴더 복사
    for folder in ["Data", "Event_EN", "Saves_EN"]:
        src_folder = os.path.join(filepath, folder)
        dest_folder = os.path.join(path, folder)
        if os.path.exists(src_folder):
            # 디렉토리가 존재하면 복사
            shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)  # 기존 폴더 덮어쓰기

    # 파일 복사
    for file in ["Atelier_Shallie_EN.exe", "Atelier_ShallieEnv.exe", "Setting.ini"]:
        shutil.copy(os.path.join(filepath, file), os.path.join(path, file))

    # 파일 삭제
    temp_folder_path = os.path.join(realpath, "temp")
    if os.path.exists(temp_folder_path):
        shutil.rmtree(temp_folder_path)  # temp 폴더와 그 안의 모든 내용 삭제

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "샤리의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

    clear_text_output()

def setup_sophie():
    path = os.path.join(game_path.get(), "Atelier Sophie DX")  # 게임 설치 경로
    realpath = os.path.dirname(__file__)  # 프로그램 실행 경로
    filepath = os.path.join(realpath, "temp")  # 설치 파일 경로

    # 파일 복사
    for file in ["Atelier_Sophie_DX.exe", "gust_pak.exe"]:
        shutil.copy(os.path.join(filepath, file), os.path.join(path, file))

    # PACK00_02.PAK 처리
    if os.path.exists(os.path.join(path, "PACK00_02.PAK")):
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK00_02.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK00_02{ext}"))
            except FileNotFoundError:
                pass

    # PACK01.PAK 처리
    if os.path.exists(os.path.join(path, "PACK01.PAK")):
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK01.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK01{ext}"))
            except FileNotFoundError:
                pass

    # PACK02_01.PAK 처리
    if os.path.exists(os.path.join(path, "PACK02_01.PAK")):
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK02_01.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK02_01{ext}"))
            except FileNotFoundError:
                pass

    # 폴더 복사
    for folder in ["Data", "DLC", "Event_JP", "Saves_JP"]:
        src_folder = os.path.join(filepath, folder)
        dest_folder = os.path.join(path, folder)
        if os.path.exists(src_folder):
            # 디렉토리가 존재하면 복사
            shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)  # 기존 폴더 덮어쓰기

    # 파일 삭제
    os.remove(os.path.join(path, "gust_pak.exe"))  # 삭제
    temp_folder_path = os.path.join(realpath, "temp")
    if os.path.exists(temp_folder_path):
        shutil.rmtree(temp_folder_path)  # temp 폴더와 그 안의 모든 내용 삭제

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "소피의 아틀리에 DX\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 일본어로 변경해주세요.")

    clear_text_output()

def setup_firis():
    path = os.path.join(game_path.get(), "Atelier Firis DX")  # 게임 설치 경로
    realpath = os.path.dirname(__file__)  # 프로그램 실행 경로
    filepath = os.path.join(realpath, "temp")  # 설치 파일 경로

    # 파일 복사
    for file in ["Atelier_Firis_DX.exe", "gust_pak.exe"]:
        shutil.copy(os.path.join(filepath, file), os.path.join(path, file))

    # PACK02_00.PAK 처리
    if os.path.exists(os.path.join(path, "Data/PACK02_00.PAK")):
        shutil.move(os.path.join(path, "Data/PACK02_00.PAK"), os.path.join(path, "PACK02_00.PAK"))
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK02_00.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK02_00{ext}"))
            except FileNotFoundError:
                pass

    # PACK03.PAK 처리
    if os.path.exists(os.path.join(path, "Data/PACK03.PAK")):
        shutil.move(os.path.join(path, "Data/PACK03.PAK"), os.path.join(path, "PACK03.PAK"))
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK03.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK03{ext}"))
            except FileNotFoundError:
                pass

    # 폴더 복사
    for folder in ["Data", "Event", "Saves"]:
        src_folder = os.path.join(filepath, folder)
        dest_folder = os.path.join(path, folder)
        if os.path.exists(src_folder):
            # 디렉토리가 존재하면 복사
            shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)  # 기존 폴더 덮어쓰기

    # 파일 삭제
    os.remove(os.path.join(path, "gust_pak.exe"))  # 삭제
    temp_folder_path = os.path.join(realpath, "temp")
    if os.path.exists(temp_folder_path):
        shutil.rmtree(temp_folder_path)  # temp 폴더와 그 안의 모든 내용 삭제

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "피리스의 아틀리에 DX\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 일본어로 변경해주세요.")

    clear_text_output()

def setup_lydie():
    path = os.path.join(game_path.get(), "Atelier Lydie and Suelle DX")  # 게임 설치 경로
    realpath = os.path.dirname(__file__)  # 프로그램 실행 경로
    filepath = os.path.join(realpath, "temp")  # 설치 파일 경로

    # 파일 복사
    for file in ["Atelier_Lydie_and_Suelle_DX.exe", "gust_pak.exe"]:
        shutil.copy(os.path.join(filepath, file), os.path.join(path, file))

    # PACK00D4.PAK 처리
    if os.path.exists(os.path.join(path, "Data/PACK00D4.PAK")):
        shutil.move(os.path.join(path, "Data/PACK00D4.PAK"), os.path.join(path, "PACK00D4.PAK"))
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK00D4.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK00D4{ext}"))
            except FileNotFoundError:
                pass

    # PACK01.PAK 처리
    if os.path.exists(os.path.join(path, "Data/PACK01.PAK")):
        shutil.move(os.path.join(path, "Data/PACK01.PAK"), os.path.join(path, "PACK01.PAK"))
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK01.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK01{ext}"))
            except FileNotFoundError:
                pass

    # PACK02.PAK 처리
    if os.path.exists(os.path.join(path, "Data/PACK02.PAK")):
        shutil.move(os.path.join(path, "Data/PACK02.PAK"), os.path.join(path, "PACK02.PAK"))
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK02.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK02{ext}"))
            except FileNotFoundError:
                pass

    # 폴더 복사
    for folder in ["Data", "Event", "Saves"]:
        src_folder = os.path.join(filepath, folder)
        dest_folder = os.path.join(path, folder)
        if os.path.exists(src_folder):
            # 디렉토리가 존재하면 복사
            shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)  # 기존 폴더 덮어쓰기

    # 파일 삭제
    os.remove(os.path.join(path, "gust_pak.exe"))  # 삭제
    temp_folder_path = os.path.join(realpath, "temp")
    if os.path.exists(temp_folder_path):
        shutil.rmtree(temp_folder_path)  # temp 폴더와 그 안의 모든 내용 삭제

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "리디&수르의 아틀리에 DX\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 일본어로 변경해주세요.")

    clear_text_output()

def setup_nelke():
    path = os.path.join(game_path.get(), "Nelke and the Legendary Alchemists Ateliers of the New World")  # 게임 설치 경로
    realpath = os.path.dirname(__file__)  # 프로그램 실행 경로
    filepath = os.path.join(realpath, "temp")  # 설치 파일 경로

    # 파일 복사
    for file in ["Nelke_and_the_Legendary_Alchemists.exe", "gust_pak.exe"]:
        shutil.copy(os.path.join(filepath, file), os.path.join(path, file))

    # PACK00_01.PAK 처리
    if os.path.exists(os.path.join(path, "data/PACK00_01.PAK")):
        shutil.move(os.path.join(path, "data/PACK00_01.PAK"), os.path.join(path, "PACK00_01.PAK"))
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK00_01.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK00_01{ext}"))
            except FileNotFoundError:
                pass

    # PACK01.PAK 처리
    if os.path.exists(os.path.join(path, "data/PACK01.PAK")):
        shutil.move(os.path.join(path, "data/PACK01.PAK"), os.path.join(path, "PACK01.PAK"))
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK01.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK01{ext}"))
            except FileNotFoundError:
                pass

    # 폴더 복사
    for folder in ["data", "event", "saves"]:
        src_folder = os.path.join(filepath, folder)
        dest_folder = os.path.join(path, folder)
        if os.path.exists(src_folder):
            # 디렉토리가 존재하면 복사
            shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)  # 기존 폴더 덮어쓰기

    # 파일 삭제
    os.remove(os.path.join(path, "gust_pak.exe"))  # 삭제
    temp_folder_path = os.path.join(realpath, "temp")
    if os.path.exists(temp_folder_path):
        shutil.rmtree(temp_folder_path)  # temp 폴더와 그 안의 모든 내용 삭제

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "네르케와 전설의 연금술사들\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 일본어로 변경해주세요.")

    clear_text_output()

def setup_lulua():
    path = os.path.join(game_path.get(), "Atelier Lulua")  # 게임 설치 경로
    realpath = os.path.dirname(__file__)  # 프로그램 실행 경로
    filepath = os.path.join(realpath, "temp")  # 설치 파일 경로

    # 파일 복사
    for file in ["Atelier_Lulua.exe", "gust_pak.exe"]:
        shutil.copy(os.path.join(filepath, file), os.path.join(path, file))

    # PACK00_01.PAK 처리
    if os.path.exists(os.path.join(path, "Data/PACK00_01.PAK")):
        shutil.move(os.path.join(path, "Data/PACK00_01.PAK"), os.path.join(path, "PACK00_01.PAK"))
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK00_01.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK00_01{ext}"))
            except FileNotFoundError:
                pass

    # PACK00_04_03.PAK 처리
    if os.path.exists(os.path.join(path, "Data/PACK00_04_03.PAK")):
        shutil.move(os.path.join(path, "Data/PACK00_04_03.PAK"), os.path.join(path, "PACK00_04_03.PAK"))
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK00_04_03.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK00_04_03{ext}"))
            except FileNotFoundError:
                pass

    # PACK00_01.PAK 처리
    if os.path.exists(os.path.join(path, "Data/PACK00_01.PAK")):
        shutil.move(os.path.join(path, "Data/PACK00_01.PAK"), os.path.join(path, "PACK00_01.PAK"))
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK00_01.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK00_01{ext}"))
            except FileNotFoundError:
                pass

    # PACK02.PAK 처리
    if os.path.exists(os.path.join(path, "Data/PACK02.PAK")):
        shutil.move(os.path.join(path, "Data/PACK02.PAK"), os.path.join(path, "PACK02.PAK"))
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK02.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK02{ext}"))
            except FileNotFoundError:
                pass

    # 폴더 복사
    for folder in ["Data", "event", "saves"]:
        src_folder = os.path.join(filepath, folder)
        dest_folder = os.path.join(path, folder)
        if os.path.exists(src_folder):
            # 디렉토리가 존재하면 복사
            shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)  # 기존 폴더 덮어쓰기

    # 파일 삭제
    os.remove(os.path.join(path, "gust_pak.exe"))  # 삭제
    temp_folder_path = os.path.join(realpath, "temp")
    if os.path.exists(temp_folder_path):
        shutil.rmtree(temp_folder_path)  # temp 폴더와 그 안의 모든 내용 삭제

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "루루아의 아틀리에\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 일본어로 변경해주세요.")

    clear_text_output()

def setup_ryza():
    path = os.path.join(game_path.get(), "Atelier Ryza")  # 게임 설치 경로
    realpath = os.path.dirname(__file__)  # 프로그램 실행 경로
    filepath = os.path.join(realpath, "temp")  # 설치 파일 경로

    # gust_pak.exe 복사
    shutil.copy(os.path.join(filepath, "gust_pak.exe"), os.path.join(path, "gust_pak.exe"))

    # PACK00_04_02.PAK 처리
    if os.path.exists(os.path.join(path, "Data/PACK00_04_02.PAK")):
        shutil.move(os.path.join(path, "Data/PACK00_04_02.PAK"), os.path.join(path, "PACK00_04_02.PAK"))
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK00_04_02.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK00_04_02{ext}"))
            except FileNotFoundError:
                pass

    # PACK01.PAK 처리
    if os.path.exists(os.path.join(path, "Data/PACK01.PAK")):
        shutil.move(os.path.join(path, "Data/PACK01.PAK"), os.path.join(path, "PACK01.PAK"))
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK01.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK01{ext}"))
            except FileNotFoundError:
                pass

    # PACK02.PAK 처리
    if os.path.exists(os.path.join(path, "Data/PACK02.PAK")):
        shutil.move(os.path.join(path, "Data/PACK02.PAK"), os.path.join(path, "PACK02.PAK"))
        subprocess.run([os.path.join(path, "gust_pak.exe"), os.path.join(path, "PACK02.PAK")])
        for ext in [".PAK", ".pak", ".JSON", ".json"]:
            try:
                os.remove(os.path.join(path, f"PACK02{ext}"))
            except FileNotFoundError:
                pass

    # 폴더 복사
    for folder in ["Data", "DLC", "event", "saves"]:
        src_folder = os.path.join(filepath, folder)
        dest_folder = os.path.join(path, folder)
        if os.path.exists(src_folder):
            # 디렉토리가 존재하면 복사
            shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)  # 기존 폴더 덮어쓰기

    # 파일 삭제
    os.remove(os.path.join(path, "gust_pak.exe"))  # 삭제
    temp_folder_path = os.path.join(realpath, "temp")
    if os.path.exists(temp_folder_path):
        shutil.rmtree(temp_folder_path)  # temp 폴더와 그 안의 모든 내용 삭제

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "라이자의 아틀리에\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 중국어 번체로 변경해주세요.")

    clear_text_output()

# 드롭다운 메뉴에서 파일 선택 시 텍스트 박스를 지우는 함수
def clear_text_output(*args):
    text_output.config(state=tk.NORMAL)  # 입력 가능 상태로 변경
    text_output.delete(1.0, tk.END)  # 텍스트 박스 내용 삭제
    text_output.config(state=tk.DISABLED)  # 다시 입력 불가능 상태로 변경

# 버튼 클릭 시 호출되는 함수
def start_download():
    file_name = selected_file.get()  # 드롭다운 메뉴에서 선택된 파일 이름
    url = file_links[file_name]  # 선택된 파일 이름에 대한 URL 가져오기
    threading.Thread(target=download_file, args=(file_name, url)).start()

# GUI 설정
def create_gui():
    global text_output  # 전역으로 선언하여 다운로드 함수에서 접근 가능
    global window
    global download_button
    global dropdown

    window = tk.Tk()
    window.title("아틀리에 시리즈 통합 한국어 패치")
    window.geometry("723x315")
    window.resizable(False, False)  # 크기 조정 불가 설정

    # 창을 화면 중앙에 위치시키기
    window.update_idletasks()  # 모든 위젯이 화면에 배치되도록 업데이트
    width = window.winfo_width()  # 창의 너비
    height = window.winfo_height()  # 창의 높이
    screen_width = window.winfo_screenwidth()  # 화면의 너비
    screen_height = window.winfo_screenheight()  # 화면의 높이

    # 중앙 위치 계산
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")  # 창 위치 설정

    # 텍스트 출력창 생성 (입력이 불가능하도록 설정)
    text_output = tk.Text(window, height=9, width=100, state=tk.DISABLED)
    text_output.grid(row=2, column=0, columnspan=3, pady=10)  # grid 사용

    # sys.stdout을 텍스트 위젯으로 리디렉션
    sys.stdout = RedirectText(text_output)

    global game_path
    game_path = StringVar()  # 경로를 저장하는 변수

    # 게임 설치 경로 라벨과 텍스트박스
    Label(window, text="스팀 라이브러리 경로:").grid(row=0, column=0, padx=5, pady=10)
    Entry(window, textvariable=game_path, width=70).grid(row=0, column=1, padx=5, pady=10)

    # 경로 선택 버튼
    select_button = Button(window, text="경로 선택", command=select_directory)
    select_button.grid(row=0, column=2, padx=10, pady=10)

    # 기본 경로 안내 문구 추가
    Label(window, text="※ 스팀 라이브러리 기본 경로는 C:\\Program Files (x86)\\Steam\\steamapps\\common입니다.").grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # 드롭다운 메뉴 생성
    global selected_file
    selected_file = StringVar(window)  # 선택된 파일 이름 저장
    selected_file.set(list(file_links.keys())[11])  # 기본값 설정
    dropdown = OptionMenu(window, selected_file, *file_links.keys(), command=clear_text_output)
    dropdown.grid(row=3, column=0, columnspan=3, padx=0, pady=5)

    # 다운로드 버튼 생성
    download_button = Button(window, text="패치 실행", command=start_download)  # 인자 없이 함수 호출
    download_button.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

    window.mainloop()

# GUI 실행
if __name__ == "__main__":
    create_gui()

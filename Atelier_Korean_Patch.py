import tkinter as tk
import subprocess
import threading
import os
import sys
import py7zr
import shutil
import gdown
import webbrowser
from tkinter import messagebox, filedialog, StringVar, Label, Entry, Button, OptionMenu, font, DISABLED, NORMAL

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
    "네르케와 전설의 연금술사들": drive_link + "1Bwq1Q4vzNBmTFgmggXfgttu3CdhNZ7qm",
    "루루아의 아틀리에": drive_link + "1QrPAt4pAVa_H_lmIUSzdBVlzvw_BcpHV",
    "라이자의 아틀리에": drive_link + "1dBHaAt-hCLVdhGmXlMq0Or1z8le2iD3f",
}

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
            # 게임 설치 및 경로 지정이 올바른지 확인
            if not check_game_installation(file_name):  # 경로가 없으면 함수 종료
                return
            
            output_message(f"{file_name} 한국어 패치를 실행합니다.")

            # 메뉴 비활성화
            patch_button.config(state=tk.DISABLED)
            dropdown.config(state=tk.DISABLED)

            # 경로 설정
            current_dir = os.path.dirname(sys.executable)  # 현재 파일의 경로

            temp_dir = os.path.join(current_dir, 'temp')
            os.makedirs(temp_dir, exist_ok=True)  # temp 폴더 생성 (존재하지 않을 경우)

            save_path = os.path.join(temp_dir, f"{file_name}.7z")  # temp 폴더 내에 압축 파일 저장 경로

            text_output.config(state=tk.NORMAL)  # 입력 가능 상태로 변경
            
            output_message("패치에 필요한 파일을 다운로드하는 중입니다.\n잠시만 기다려주세요...\n이 작업은 환경에 따라 1분 이상 소요될 수 있습니다.")

            # 다운로드
            try:
                gdown.download(url, save_path, quiet=True)
            except Exception as e:
                output_message(f"Download failed: {e}")
                return

            output_message("다운로드가 완료되었습니다.\n압축을 해제하는 중입니다.\n잠시만 기다려주세요...")  # 다운로드 완료 메시지
            
            # 다운로드한 파일의 압축 해제
            with py7zr.SevenZipFile(save_path, mode='r') as archive:
                archive.extractall(path=temp_dir)  # temp 폴더에 내용물 직접 해제
                output_message("압축 해제가 완료되었습니다.")  # 압축 해제 완료 메시지

            # 압축 해제 후 .7z 파일 삭제
            os.remove(save_path)
            output_message("압축 파일을 삭제하였습니다.\n한국어 패치를 설치합니다.")  # 삭제 완료 메시지

            # 패치 실행
            setup_functions = {
                "로로나의 아틀리에 DX": setup_rorona,
                "토토리의 아틀리에 DX": setup_totori,
                "메루루의 아틀리에 DX": setup_meruru,
                "아샤의 아틀리에 DX": setup_ayesha,
                "에스카&로지의 아틀리에 DX": setup_escha,
                "샤리의 아틀리에 DX": setup_shallie,
                "소피의 아틀리에 DX": setup_sophie,
                "피리스의 아틀리에 DX": setup_firis,
                "리디&수르의 아틀리에 DX": setup_lydie,
                "네르케와 전설의 연금술사들": setup_nelke,
                "루루아의 아틀리에": setup_lulua,
                "라이자의 아틀리에": setup_ryza,
            }

            if file_name in setup_functions:
                setup_functions[file_name]()
            
            text_output.config(state=tk.DISABLED)  # 다시 입력 불가능 상태로 변경

    except Exception as e:
        output_message(f"Error downloading {file_name}: {e}")
    finally:
        patch_button.config(state=tk.NORMAL)  # 다운로드 완료 후 버튼 활성화
        dropdown.config(state=tk.NORMAL)  # 다운로드 완료 후 드롭다운 메뉴 활성화

def output_message(message):
    """텍스트 박스에 메시지를 출력하는 함수"""
    global text_output
    if text_output is not None:
        text_output.config(state=tk.NORMAL)  # 텍스트 박스를 수정 가능 상태로 전환
        text_output.insert(tk.END, message + "\n")  # 메시지 추가
        text_output.config(state=tk.DISABLED)  # 텍스트 박스를 다시 읽기 전용으로 설정
        text_output.yview(tk.END)  # 항상 마지막 메시지로 스크롤

# 게임 이름과 설치 경로를 매핑하는 딕셔너리
game_paths = {
    "로로나의 아틀리에 DX": "Atelier Rorona ~The Alchemist of Arland~ DX",
    "토토리의 아틀리에 DX": "Atelier Totori ~The Adventurer of Arland~ DX",
    "메루루의 아틀리에 DX": "Atelier Meruru ~The Apprentice of Arland~ DX",
    "아샤의 아틀리에 DX": "Atelier Ayesha DX",
    "에스카&로지의 아틀리에 DX": "Atelier Escha and Logy DX",
    "샤리의 아틀리에 DX": "Atelier Shallie DX",
    "소피의 아틀리에 DX": "Atelier Sophie DX",
    "피리스의 아틀리에 DX": "Atelier Firis DX",
    "리디&수르의 아틀리에 DX": "Atelier Lydie and Suelle DX",
    "네르케와 전설의 연금술사들": "Nelke and the Legendary Alchemists Ateliers of the New World",
    "루루아의 아틀리에": "Atelier Lulua",
    "라이자의 아틀리에": "Atelier Ryza"
}

def check_game_installation(file_name):
    # 파일 이름에 해당하는 설치 경로 찾기
    if file_name in game_paths:
        path = os.path.join(game_path.get(), game_paths[file_name])  # 게임 설치 경로
        # 설치된 경로가 존재하는지 확인
        if not os.path.exists(path):
            if file_name == "네르케와 전설의 연금술사들":
                messagebox.showerror("오류", f"{file_name}이 설치되지 않았습니다.\n스팀 라이브러리 경로를 다시 한 번 확인해주세요.")
            else:
                messagebox.showerror("오류", f"{file_name}가 설치되지 않았습니다.\n스팀 라이브러리 경로를 다시 한 번 확인해주세요.")
            return False  # 설치되지 않은 경우 False 반환
        return True  # 설치 경로가 올바르면 True 반환
    else:
        messagebox.showerror("오류", f"{file_name}는 지원되지 않는 게임입니다.")
        return False  # 지원되지 않는 게임이면 False 반환

# 각 파일에 대해 다운로드 완료 후 호출할 함수 정의
def setup_rorona():
    path = os.path.join(game_path.get(), "Atelier Rorona ~The Alchemist of Arland~ DX")  # 게임 설치 경로
    realpath = os.path.dirname(sys.executable)  # 프로그램 실행 경로
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

    output_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "로로나의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

    clear_text_output()

def setup_totori():
    path = os.path.join(game_path.get(), "Atelier Totori ~The Adventurer of Arland~ DX")  # 게임 설치 경로
    realpath = os.path.dirname(sys.executable)  # 프로그램 실행 경로
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

    output_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "토토리의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

    clear_text_output()

def setup_meruru():
    path = os.path.join(game_path.get(), "Atelier Meruru ~The Apprentice of Arland~ DX")  # 게임 설치 경로
    realpath = os.path.dirname(sys.executable)  # 프로그램 실행 경로
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

    output_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "메루루의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

    clear_text_output()

def setup_ayesha():
    path = os.path.join(game_path.get(), "Atelier Ayesha DX")  # 게임 설치 경로
    realpath = os.path.dirname(sys.executable)  # 프로그램 실행 경로
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

    output_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "아샤의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

    clear_text_output()

def setup_escha():
    path = os.path.join(game_path.get(), "Atelier Escha and Logy DX")  # 게임 설치 경로
    realpath = os.path.dirname(sys.executable)  # 프로그램 실행 경로
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

    output_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "에스카&로지의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

    clear_text_output()

def setup_shallie():
    path = os.path.join(game_path.get(), "Atelier Shallie DX")  # 게임 설치 경로
    realpath = os.path.dirname(sys.executable)  # 프로그램 실행 경로
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

    output_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "샤리의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

    clear_text_output()

def setup_sophie():
    path = os.path.join(game_path.get(), "Atelier Sophie DX")  # 게임 설치 경로
    realpath = os.path.dirname(sys.executable)  # 프로그램 실행 경로
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

    output_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "소피의 아틀리에 DX\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 일본어로 변경해주세요.")

    clear_text_output()

def setup_firis():
    path = os.path.join(game_path.get(), "Atelier Firis DX")  # 게임 설치 경로
    realpath = os.path.dirname(sys.executable)  # 프로그램 실행 경로
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

    output_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "피리스의 아틀리에 DX\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 일본어로 변경해주세요.")

    clear_text_output()

def setup_lydie():
    path = os.path.join(game_path.get(), "Atelier Lydie and Suelle DX")  # 게임 설치 경로
    realpath = os.path.dirname(sys.executable)  # 프로그램 실행 경로
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

    output_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "리디&수르의 아틀리에 DX\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 일본어로 변경해주세요.")

    clear_text_output()

def setup_nelke():
    path = os.path.join(game_path.get(), "Nelke and the Legendary Alchemists Ateliers of the New World")  # 게임 설치 경로
    realpath = os.path.dirname(sys.executable)  # 프로그램 실행 경로
    filepath = os.path.join(realpath, "temp")  # 설치 파일 경로
    userpath = os.path.expanduser(r'~/Documents/KoeiTecmo/Nelke and the Legendary Alchemists')

    # 파일 복사
    for file in ["Nelke_and_the_Legendary_Alchemists.exe", "gust_pak.exe"]:
        shutil.copy(os.path.join(filepath, file), os.path.join(path, file))

    os.makedirs(userpath, exist_ok=True)
    shutil.copy(os.path.join(filepath, "Setting.ini"), os.path.join(userpath, "Setting.ini"))

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

    output_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "네르케와 전설의 연금술사들\n한국어 패치가 완료되었습니다!")

    clear_text_output()

def setup_lulua():
    path = os.path.join(game_path.get(), "Atelier Lulua")  # 게임 설치 경로
    realpath = os.path.dirname(sys.executable)  # 프로그램 실행 경로
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

    output_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "루루아의 아틀리에\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 일본어로 변경해주세요.")

    clear_text_output()

def setup_ryza():
    path = os.path.join(game_path.get(), "Atelier Ryza")  # 게임 설치 경로
    realpath = os.path.dirname(sys.executable)  # 프로그램 실행 경로
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

    output_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "라이자의 아틀리에\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 중국어 번체로 변경해주세요.")

    clear_text_output()

# 드롭다운 메뉴에서 파일 선택 시 텍스트 박스를 지우는 함수
def clear_text_output(*args):
    text_output.config(state=tk.NORMAL)  # 입력 가능 상태로 변경
    text_output.delete(1.0, tk.END)  # 텍스트 박스 내용 삭제
    text_output.config(state=tk.DISABLED)  # 다시 입력 불가능 상태로 변경

# 패치 실행
def run_patch():
    try:
        file_name = selected_file.get()  # 드롭다운 메뉴에서 선택된 파일 이름
        url = file_links[file_name]  # 선택된 파일 이름에 대한 URL 가져오기
        
        # 디버깅을 위한 메시지 출력
        print(f"Starting download for: {file_name}")
        
        threading.Thread(target=download_file, args=(file_name, url)).start()
        
        # 스레드가 정상적으로 시작되었는지 확인
        print("Thread started successfully.")
    
    except Exception as e:
        # 예외 발생 시 출력
        print(f"Error starting download thread: {e}")

def open_webpage():
    webbrowser.open("https://gall.dcinside.com/mgallery/board/view/?id=atelierseries&no=88890")

def update_button_state(*args):
    # 드롭다운 메뉴 값이 '타이틀 선택'일 경우 버튼 비활성화
    if selected_file.get() == "타이틀 선택":
        patch_button.config(state=DISABLED)
    else:
        patch_button.config(state=NORMAL)

# GUI 설정
def create_gui():
    global text_output, window, patch_button, dropdown, game_path

    window = tk.Tk()
    window.title("아틀리에 시리즈 통합 한국어 패치")
    window.geometry("800x350")
    window.resizable(False, False)  # 크기 조정 불가 설정
    window.grid_propagate(False)

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

    # 프레임 생성
    top_frame = tk.Frame(window)
    top_frame.grid(padx=32, pady=(15,0))  # 프레임을 창에 추가하고 패딩 추가

    # 게임 설치 경로 라벨, 텍스트 박스 & 경로 선택 버튼
    game_path = StringVar()  # 경로를 저장하는 변수

    Label(top_frame, text="스팀 라이브러리 경로:").grid(row=0, column=0, padx=(80,0), pady=(20,10))
    Entry(top_frame, textvariable=game_path, width=50).grid(row=0, column=1, padx=10, pady=(20,10))

    select_button = Button(top_frame, text="경로 선택", command=select_directory)
    select_button.grid(row=0, column=2, padx=10, pady=(20,10))

    # 프레임 생성
    bottom_frame = tk.Frame(window)
    bottom_frame.grid(padx=32, pady=0)  # 프레임을 창에 추가하고 패딩 추가

    # 기본 경로 안내 문구 추가
    Label(bottom_frame, text="※ 스팀 라이브러리 기본 경로는 C:\\Program Files (x86)\\Steam\\steamapps\\common입니다.").grid(row=1, column=0, columnspan=3, padx=(75,0), pady=10)

    # 기본 폰트를 가져오고 밑줄 추가
    default_font = font.nametofont("TkDefaultFont")
    underline_font = default_font.copy()
    underline_font.configure(underline=True)

    # 설치 가이드 보기 라벨 추가 (파란색 밑줄, 하이퍼링크)
    guide_label = Label(bottom_frame, text="설치 가이드 보기", fg="blue", cursor="hand2", font=underline_font)
    guide_label.grid(row=2, column=0, columnspan=3, padx=(75,0), pady=(0,15))
    guide_label.bind("<Button-1>", lambda e: open_webpage())

    # 텍스트 출력창 생성 (입력이 불가능하도록 설정)
    text_output = tk.Text(bottom_frame, height=5, width=70, state=tk.DISABLED)
    text_output.grid(row=3, column=0, columnspan=3, padx=(75,0), pady=10)

    # 드롭다운 메뉴 생성
    global selected_file
    selected_file = StringVar(bottom_frame)  # 선택된 파일 이름 저장
    selected_file.set("타이틀 선택")  # 기본값을 '타이틀 선택'으로 설정 (설명 문자열)
    selected_file.trace("w", update_button_state)  # 드롭다운 값 변경 시 update_button_state 함수 호출

    # 드롭다운 메뉴 생성 (선택 가능한 항목은 file_links.keys()만 포함)
    dropdown = OptionMenu(bottom_frame, selected_file, *file_links.keys(), command=clear_text_output)
    dropdown.grid(row=4, column=0, columnspan=3, padx=(75,0), pady=(13,5))

    # 패치 실행 버튼 생성   
    patch_button = Button(bottom_frame, text="패치 실행", command=run_patch)
    patch_button.grid(row=5, column=0, columnspan=3, padx=(75,0), pady=5)

    # 초기 버튼 상태 비활성화
    patch_button.config(state=DISABLED)

    window.mainloop()

# GUI 실행
if __name__ == "__main__":
    create_gui()

# pyinstaller --onefile --windowed --hidden-import=gdown Atelier_Korean_Patch.py
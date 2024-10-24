import threading
import webbrowser
import shutil
import subprocess
import os
import sys
import gdown
import py7zr
import winreg
import fnmatch
import vdf
import tkinter as tk
from datetime import datetime
from tkinter import PhotoImage, messagebox, StringVar, Label, Button, OptionMenu, font, DISABLED, NORMAL

DB = {
    "로로나의 아틀리에 DX": [
        "Atelier Rorona ~The Alchemist of Arland~ DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "1uEYArKmjFXBCqwf0AZIrFSEFaJe37rBI",  # Download URL
        ["Event", "Res"],  # Patch Folder
        ["A11R_x64_Release.exe", "ArlandDX_Settings.ini"]  # Patch File
    ],
    "토토리의 아틀리에 DX": [
        "Atelier Totori ~The Adventurer of Arland~ DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "1CYmCSRMT3eVSOn_OOuDnLpHMFvpAVSDB",  # Download URL
        ["Event", "Res"],  # Patch Folder
        ["A12V_x64_Release.exe", "ArlandDX_Settings.ini"]  # Patch File
    ],
    "메루루의 아틀리에 DX": [
        "Atelier Meruru ~The Apprentice of Arland~ DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "1pCiaute1tcLiFNdih1rbC9haG0B2baKd",  # Download URL
        ["Event", "Res"],  # Patch Folder
        ["A13V_x64_Release.exe", "ArlandDX_Settings.ini"]  # Patch File
    ],
    "아샤의 아틀리에 DX": [
        "Atelier Ayesha DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "1kBJ82u0LyUDsWKQM-G_mr3EJpp2k1UGq",  # Download URL
        ["Event", "Res"],  # Patch Folder
        ["Atelier_Ayesha.exe", "Setting.ini"]  # Patch File
    ],
    "에스카&로지의 아틀리에 DX": [
        "Atelier Escha and Logy DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "1_3Y46qfxo2xykbMTqjBSn8r6jLTRpLsc",  # Download URL
        ["Data", "DLC", "Event", "Saves"],  # Patch Folder
        ["Atelier_Escha_and_Logy.exe", "Setting.ini"]  # Patch File
    ],
    "샤리의 아틀리에 DX": [
        "Atelier Shallie DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "1Tmq6sCZXWxZd6Ul-kF0n60P1Gh08YTFA",  # Download URL
        ["Data", "Event_EN", "Saves_EN"],  # Patch Folder
        ["Atelier_Shallie_EN.exe", "Atelier_ShallieEnv.exe", "Setting.ini"]  # Patch File
    ],
    "소피의 아틀리에 DX": [
        "Atelier Sophie DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "1a0tokxsD3KRUma_zXdUMeVpK_h6rJD3_",  # Download URL
        ["Data", "DLC", "Event_JP", "Saves_JP"],  # Patch Folder
        ["Atelier_Sophie_DX.exe", "gust_pak.exe"],  # Patch File
        ["PACK00_02.PAK", "PACK01.PAK", "PACK02_01.PAK"]  # Patch PAK
    ],
    "피리스의 아틀리에 DX": [
        "Atelier Firis DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "1jexLNgPMGS0pjTsIFn3yNqPrga1IckXX",  # Download URL
        ["Data", "Event", "Saves"],  # Patch Folder
        ["Atelier_Firis_DX.exe", "gust_pak.exe"],  # Patch File
        ["PACK02_00.PAK", "PACK03.PAK"]  # Patch PAK
    ],
    "리디&수르의 아틀리에 DX": [
        "Atelier Lydie and Suelle DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "1376TWCw3AJUytfpl3ejInZpuMBuAf0dB",  # Download URL
        ["Data", "Event", "Saves"],  # Patch Folder
        ["Atelier_Lydie_and_Suelle_DX.exe", "gust_pak.exe"],  # Patch File
        ["PACK00D4.PAK", "PACK01.PAK", "PACK02.PAK"]  # Patch PAK
    ],
    "네르케와 전설의 연금술사들": [
        "Nelke and the Legendary Alchemists Ateliers of the New World",  # Folder Name
        "https://drive.google.com/uc?id=" + "1Bwq1Q4vzNBmTFgmggXfgttu3CdhNZ7qm",  # Download URL
        ["data", "event", "saves"],  # Patch Folder
        ["Nelke_and_the_Legendary_Alchemists.exe", "gust_pak.exe"],  # Patch File
        ["PACK00_01.PAK", "PACK01.PAK"]  # Patch PAK
    ],
    "루루아의 아틀리에": [
        "Atelier Lulua",  # Folder Name
        "https://drive.google.com/uc?id=" + "1QrPAt4pAVa_H_lmIUSzdBVlzvw_BcpHV",  # Download URL
        ["Data", "event", "saves"],  # Patch Folder
        ["Atelier_Lulua.exe", "gust_pak.exe"],  # Patch File
        ["PACK00_01.PAK", "PACK00_04_03.PAK", "PACK01.PAK", "PACK02.PAK"]  # Patch PAK
    ],
    "라이자의 아틀리에": [
        "Atelier Ryza",  # Folder Name
        "https://drive.google.com/uc?id=" + "1dBHaAt-hCLVdhGmXlMq0Or1z8le2iD3f",  # Download URL
        ["Data", "DLC", "event", "saves"],  # Patch Folder
        ["gust_pak.exe"],  # Patch File
        ["PACK00_04_02.PAK", "PACK01.PAK", "PACK02.PAK"]  # Patch PAK
    ]
}

class SteamPath:
    steam_apps = "steamapps"
    library_folders = "libraryfolders.vdf"

    def __init__(self) -> None:
        self.__install_path: str = self.__get_steam_path()
        self.__library_path: str = os.path.join(self.__install_path, SteamPath.steam_apps, SteamPath.library_folders)
        
        # libraryfolders.vdf를 파싱해서 library_path와 apps만 포함하는 리스트를 반환
        self.__library_data = self.parse_vdf(self.__library_path)

    # 스팀 설치 경로를 확인하는 함수
    def __get_steam_path(self) -> str:

        # 32비트인지 64비트인지 체크
        is_64bit = sys.maxsize > 2**32

        # 레지스트리 경로 설정
        if is_64bit:
            registry_path = r"SOFTWARE\Wow6432Node\Valve\Steam"
        else:
            registry_path = r"SOFTWARE\Valve\Steam"

        try:
            # 레지스트리 키 열기
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path, 0, winreg.KEY_READ)
            install_path: str = ""
            # InstallPath 값 읽기
            install_path, _ = winreg.QueryValueEx(key, "InstallPath")
            # 레지스트리 키 닫기
            winreg.CloseKey(key)
            return install_path

        except FileNotFoundError:
            raise FileNotFoundError("스팀이 설치되지 않았습니다.")
        except Exception as e:
            raise e

    # libraryfolders.vdf 파일을 파싱하는 함수
    def parse_vdf(self, vdf_path: str):

        # libraryfolders.vdf 열기
        dic: dict = vdf.load(open(vdf_path, encoding="utf-8"))
        inner: dict = dic['libraryfolders']
        
        # library_path와 apps만 가져오는 튜플 생성
        result: tuple = []
        
        for key, value in inner.items():
            library_path: str = value['path'] + "\\steamapps\\common"
            library_path = library_path.replace('\\', '/')
            apps: list[str] = list(value['apps'])
            
            # library_path와 apps만 담은 튜플 추가
            result.append((library_path, apps))

        return result

    @property
    def library_data(self) -> list:
        return self.__library_data
    
    @property
    def library_path(self) -> list:
        return [library[0] for library in self.__library_data]

# 전역 변수
steam_path = SteamPath()
library_list = steam_path.library_path

# GUI 설정
def create_gui():
    global root, message_widget, dropdown_menu, patch_button

    root = tk.Tk()
    root.title(f"아틀리에 통합 한국어 패치 툴 (Build: {datetime.today().strftime("%Y.%m.%d")})")
    root.geometry("464x330")
    root.resizable(False, False)  # 크기 조정 불가 설정
    root.grid_propagate(False)

    # 창을 화면 중앙에 위치시키기
    root.update_idletasks()  # 모든 위젯이 화면에 배치되도록 업데이트
    width = root.winfo_width()  # 창의 너비
    height = root.winfo_height()  # 창의 높이
    screen_width = root.winfo_screenwidth()  # 화면의 너비
    screen_height = root.winfo_screenheight()  # 화면의 높이

    # 중앙 위치 계산
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")  # 창 위치 설정

    # 아이콘 추가
    if getattr(sys, 'frozen', False):  # 패키징된 상태인지 확인
        current_dir = sys._MEIPASS  # 패키징된 실행 파일의 임시 경로
    else:
        current_dir = os.path.dirname(__file__)  # 개발 중일 때 현재 스크립트의 경로

    icon_file = os.path.join(current_dir, 'icon.png')
    icon = PhotoImage(file=icon_file)
    root.iconphoto(False, icon)

    # 프레임 생성
    frame = tk.Frame(root)
    frame.grid(padx=0, pady=0)  # 프레임을 창에 추가하고 패딩 추가

    # 메시지 창 생성
    message_widget = tk.Text(frame, height=12, width=60, state=tk.DISABLED)
    message_widget.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

    # 타이틀 선택
    global selected_title
    selected_title = StringVar(frame)  # 선택된 파일 이름 저장
    selected_title.set("타이틀 선택")  # 기본값을 '타이틀 선택'으로
    selected_title.trace_add("write", lambda *args: update_button_state())  # 드롭다운 값 변경 시 update_button_state 함수 호출

    # 드롭다운 메뉴 생성
    dropdown_menu = OptionMenu(frame, selected_title, *DB.keys(), command=clear_message)
    dropdown_menu.grid(row=1, column=0, columnspan=3, padx=0, pady=0)

    # 패치 버튼 생성   
    patch_button = Button(frame, text="패치 실행", command=run_patch, state=tk.DISABLED)
    patch_button.grid(row=2, column=0, columnspan=3, padx=0, pady=10)

    # 폰트 설정
    default_font = font.nametofont("TkDefaultFont")
    underline_font = default_font.copy()
    underline_font.configure(underline=True)

    # 설치 가이드
    guide_label = Label(frame, text="설치 가이드 보기", fg="blue", cursor="hand2", font=underline_font)
    guide_label.grid(row=3, column=0, columnspan=3, padx=0, pady=10)
    guide_label.bind("<Button-1>", lambda e: webbrowser.open("https://gall.dcinside.com/mgallery/board/view/?id=atelierseries&no=88890"))

    root.mainloop()

# 메시지를 출력하는 함수
def print_message(Message):
    root.after(0, lambda: message_widget.config(state=NORMAL))
    root.after(0, lambda: message_widget.insert(tk.END, Message + "\n"))
    root.after(0, lambda: message_widget.see(tk.END))
    root.after(0, lambda: message_widget.yview(tk.END))  # 항상 마지막 메시지로 스크롤
    root.after(0, lambda: message_widget.config(state=DISABLED))

# 메시지를 지우는 함수
def clear_message(*args):
    message_widget.config(state=NORMAL)
    message_widget.delete(1.0, tk.END)
    message_widget.config(state=DISABLED)

# 타이틀 선택 시 패치 버튼을 활성화
def update_button_state(*args):
    if selected_title.get() == "타이틀 선택":
        patch_button.config(state=DISABLED)
    else:
        patch_button.config(state=NORMAL)
        set_library(selected_title.get())

# 라이브러리 경로를 설정하는 함수
def set_library(title):
    global library_path
    library_path = "Not found"

    if not library_list:
        messagebox.showerror("오류", "스팀이 설치되지 않았습니다.")
    else:
        found = False # 라이브러리를 찾았는지 여부를 체크하는 변수

        # library_data의 경로와 folder_name이 포함된 리스트 검색
        for entry in steam_path.library_data:
            global lib_path
            lib_path = entry[0]
            # 선택된 타이틀의 설치 폴더가 존재하는지 확인
            if os.path.exists(os.path.join(lib_path, DB[title][0])):
                library_path = lib_path

                if title == "네르케와 전설의 연금술사들":
                    print_message(f"{title}을 기반으로 경로가 설정되었습니다.")
                else:
                    print_message(f"{title}를 기반으로 경로가 설정되었습니다.")
                found = True
                break  # 일치하는 경로를 찾으면 종료
        
        if not found:
            if title == "네르케와 전설의 연금술사들":
                print_message(f"{title}이 설치되지 않았습니다.")
            else:
                print_message(f"{title}가 설치되지 않았습니다.")

# 패치 실행
def run_patch():
    try:
        title = selected_title.get()  # 드롭다운 메뉴에서 선택한 타이틀

        # 라이브러리가 지정되지 않은 경우 오류 메시지 출력
        if library_path == "Not found":
            if title == "네르케와 전설의 연금술사들":
                messagebox.showerror("오류", f"{title}이 설치되지 않았습니다.")
                return
            else:
                messagebox.showerror("오류", f"{title}가 설치되지 않았습니다.")
                return
        else:
            if fnmatch.filter(os.listdir(os.path.join(lib_path, DB[title][0])), '*.exe'):
                print(f"Starting download for: {title}") # 디버깅 메시지
                threading.Thread(target=download_file, args=(title,)).start()
                print("Thread started successfully.") # 디버깅 메시지
            else:
                messagebox.showerror("오류", "게임 설치가 완료된 뒤에 패치를 진행해주세요.")

    except Exception as e:
        print(f"Error starting download thread: {e}") # 디버깅 메시지

# 파일을 다운로드하는 함수
def download_file(title):
    patch_button.config(state=DISABLED)
    dropdown_menu.config(state=DISABLED)
    message_widget.config(state=NORMAL)

    # 경로 설정
    current_path = os.path.dirname(sys.executable)  # 패치 프로그램 경로
    temp_path = os.path.join(current_path, 'temp') # temp 폴더 경로
    os.makedirs(temp_path, exist_ok=True)  # temp 폴더가 존재하지 않을 경우 폴더 생성
    save_path = os.path.join(temp_path, f"{title}.7z")  # 압축 파일 저장 경로

    # 다운로드 URL
    download_url = DB[title][1]

    print_message("패치에 필요한 파일을 다운로드하는 중입니다.")
    print_message("잠시만 기다려주세요...")
    print_message("이 작업은 환경에 따라 1분 이상 소요될 수 있습니다.")

    try:
        gdown.download(download_url, save_path, quiet=False)
    except Exception as e:
        messagebox.showerror("오류", "다운로드 주소가 변경되었습니다.\n최신 버전을 다운받은 뒤 다시 시도해주세요.\n\n확인 버튼을 누르면 웹페이지에 자동으로 연결됩니다.")
        webbrowser.open("https://gall.dcinside.com/mgallery/board/view/?id=atelierseries&no=88890")
        root.quit()
        root.destroy()
        return

    print_message("다운로드가 완료되었습니다.")

    unzip_file(title, save_path, temp_path)

# 파일의 압축을 해제하는 함수
def unzip_file(title, save_path, temp_path):
    print_message("압축을 해제하는 중입니다.")
    print_message("잠시만 기다려주세요...")
    
    with py7zr.SevenZipFile(save_path, mode='r') as archive:
        archive.extractall(path=temp_path)  # temp 폴더에 내용물 직접 해제
        print_message("압축 해제가 완료되었습니다.")

    # 압축 파일 삭제
    os.remove(save_path)
    print_message("압축 파일 삭제가 완료되었습니다.")

    patch_file(title)

# 패치를 실행하는 함수
def patch_file(title):
    print_message("한국어 패치를 설치합니다.")
    
    path = os.path.join(library_path, DB[title][0])  # 게임 설치 경로
    realpath = os.path.dirname(sys.executable)  # 프로그램 실행 경로
    filepath = os.path.join(realpath, "temp")  # 설치 파일 경로
    userpath = os.path.expanduser(r'~/Documents/KoeiTecmo/Nelke and the Legendary Alchemists') # 네르케 ini 파일 경로

    # 파일 복사
    for file in DB[title][3]:
        shutil.copy(os.path.join(filepath, file), os.path.join(path, file))
    
    if title == "네르케와 전설의 연금술사들":
        os.makedirs(userpath, exist_ok=True)
        shutil.copy(os.path.join(filepath, "Setting.ini"), os.path.join(userpath, "Setting.ini"))

    if title == "소피의 아틀리에 DX":
        for pak_file in DB[title][4]:
            pack_path = os.path.join(path, pak_file)
            if os.path.exists(pack_path):
                subprocess.run([os.path.join(path, "gust_pak.exe"), pack_path])
                for ext in [".PAK", ".pak", ".JSON", ".json"]:
                    try:
                        os.remove(os.path.join(path, f"{pak_file.split('.')[0]}{ext}"))
                    except FileNotFoundError:
                        pass

    if title in ["피리스의 아틀리에 DX", "리디&수르의 아틀리에 DX", "네르케와 전설의 연금술사들", "루루아의 아틀리에", "라이자의 아틀리에"]:
        for pak_file in DB[title][4]:
            src_pack_path = os.path.join(path, "Data/" + f"{pak_file}")
            dest_pack_path = os.path.join(path, pak_file)
            if os.path.exists(src_pack_path):
                shutil.move(src_pack_path, dest_pack_path)
                subprocess.run([os.path.join(path, "gust_pak.exe"), dest_pack_path])
                for ext in [".PAK", ".pak", ".JSON", ".json"]:
                    try:
                        os.remove(os.path.join(path, f"{pak_file.split('.')[0]}{ext}"))
                    except FileNotFoundError:
                        pass

    # 폴더 복사
    for folder in DB[title][2]:
        src_folder = os.path.join(filepath, folder)
        dest_folder = os.path.join(path, folder)
        if os.path.exists(src_folder):
            # 디렉토리가 존재하면 복사
            shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)  # 기존 폴더 덮어쓰기

    # 파일 삭제
    if os.path.exists(os.path.join(path, "gust_pak.exe")):
        os.remove(os.path.join(path, "gust_pak.exe"))  # 삭제

    temp_folder_path = os.path.join(realpath, "temp")
    if os.path.exists(temp_folder_path):
        shutil.rmtree(temp_folder_path)  # temp 폴더와 그 안의 모든 내용 삭제

    print_message("패치가 완료되었습니다.")

    patch_button.config(state=NORMAL)
    dropdown_menu.config(state=NORMAL)
    message_widget.config(state=DISABLED)

    # 패치가 완료된 후 메시지 박스 표시
    if title in ["소피의 아틀리에 DX", "피리스의 아틀리에 DX", "리디&수르의 아틀리에 DX", "루루아의 아틀리에"]:
        messagebox.showinfo("패치 완료", f"{title}\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 일본어로 변경해주세요.") 
    elif title == "라이자의 아틀리에":
        messagebox.showinfo("패치 완료", f"{title}\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 중국어 번체로 변경해주세요.")
    else:
        messagebox.showinfo("패치 완료", f"{title}\n한국어 패치가 완료되었습니다!")
    root.quit()
    root.destroy()

# GUI 실행
create_gui()

# pyinstaller --onefile --windowed --hidden-import=gdown --icon=icon.ico --add-data "icon.png;." AtelierKOR.py
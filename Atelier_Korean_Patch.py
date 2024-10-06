import threading
import webbrowser
import shutil
import subprocess
import os
import sys
import gdown
import py7zr
import winreg
import vdf
import tkinter as tk
from tkinter import PhotoImage, messagebox, StringVar, Label, Button, OptionMenu, font, DISABLED, NORMAL

class SteamPath:
    # 전역 상수
    steam_apps = "steamapps"  # 스팀 설치 경로의 steamapps 폴더 이름
    library_folders = "libraryfolders.vdf"  # 스팀 설치 경로의 steamapps 폴더 안에 있는 libraryfolders.vdf 파일 이름

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

steam_path = SteamPath()
library_list = steam_path.library_path

DB = {
    "로로나의 아틀리에 DX": [ # 00
        "Atelier Rorona ~The Alchemist of Arland~ DX",  # F
        "https://drive.google.com/uc?id=" + "144qax7CARxAoMuDe_K4kF_zsgoTGb_qa"  # Download URL
    ],
    "토토리의 아틀리에 DX": [ # 01
        "Atelier Totori ~The Adventurer of Arland~ DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "16hRiKkMgaWBe2yTZ5rlAeTK-w2IxfUyD"  # Download URL
    ],
    "메루루의 아틀리에 DX": [ # 02
        "Atelier Meruru ~The Apprentice of Arland~ DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "19pdqLQTmPPLC2bWZUqLWylDdxcT6BjDC"  # Download URL
    ],
    "아샤의 아틀리에 DX": [ # 03
        "Atelier Ayesha DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "1eTGP2EuMh7GJf4ux8vKz4656Lu5EAPV5"  # Download URL
    ],
    "에스카&로지의 아틀리에 DX": [ # 04
        "Atelier Escha and Logy DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "1_3Y46qfxo2xykbMTqjBSn8r6jLTRpLsc"  # Download URL
    ],
    "샤리의 아틀리에 DX": [ # 05
        "Atelier Shallie DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "1Tmq6sCZXWxZd6Ul-kF0n60P1Gh08YTFA"  # Download URL
    ],
    "소피의 아틀리에 DX": [ # 06
        "Atelier Sophie DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "1-tucaRZO-i5e5Qlib22I0ETUfAPTGneD"  # Download URL
    ],
    "피리스의 아틀리에 DX": [ # 07
        "Atelier Firis DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "1fvWOAWj-QaHBWkMTEGrFP_MnTmiw73sM"  # Download URL
    ],
    "리디&수르의 아틀리에 DX": [ # 08
        "Atelier Lydie and Suelle DX",  # Folder Name
        "https://drive.google.com/uc?id=" + "1jcqTVOwAZ_KQEv4wsi3lc4j58N7vLdMx"  # Download URL
    ],
    "네르케와 전설의 연금술사들": [ # 09
        "Nelke and the Legendary Alchemists Ateliers of the New World",  # Folder Name
        "https://drive.google.com/uc?id=" + "1Bwq1Q4vzNBmTFgmggXfgttu3CdhNZ7qm"  # Download URL
    ],
    "루루아의 아틀리에": [ # 10
        "Atelier Lulua",  # Folder Name
        "https://drive.google.com/uc?id=" + "1QrPAt4pAVa_H_lmIUSzdBVlzvw_BcpHV"  # Download URL
    ],
    "라이자의 아틀리에": [ # 11
        "Atelier Ryza",  # Folder Name
        "https://drive.google.com/uc?id=" + "1dBHaAt-hCLVdhGmXlMq0Or1z8le2iD3f"  # Download URL
    ]
}

# GUI 설정
def create_gui():
    global console_box, root, patch_button, dropdown

    root = tk.Tk()
    root.title("아틀리에 시리즈 통합 한국어 패치")
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

    # 콘솔 박스 생성
    console_box = tk.Text(frame, height=12, width=60, state=tk.DISABLED)
    console_box.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

    # 타이틀 선택 드롭다운 메뉴 생성
    global selected_title
    selected_title = StringVar(frame)  # 선택된 파일 이름 저장
    selected_title.set("타이틀 선택")  # 기본값을 '타이틀 선택'으로 설정 (설명 문자열)
    selected_title.trace("w", update_button_state)  # 드롭다운 값 변경 시 update_button_state 함수 호출
    selected_title.trace("w", lambda *args: set_library(selected_title.get()))

    dropdown = OptionMenu(frame, selected_title, *DB.keys(), command=clear_textbox)
    dropdown.grid(row=1, column=0, columnspan=3, padx=0, pady=0)

    # 패치 실행 버튼 생성   
    patch_button = Button(frame, text="패치 실행", command=run_patch)
    patch_button.grid(row=2, column=0, columnspan=3, padx=0, pady=10)

    # 초기 버튼 상태 비활성화
    patch_button.config(state=DISABLED)

    # 기본 폰트를 가져오고 밑줄 추가
    default_font = font.nametofont("TkDefaultFont")
    underline_font = default_font.copy()
    underline_font.configure(underline=True)

    # 설치 가이드 보기 라벨 추가 (파란색 밑줄, 하이퍼링크)
    guide_label = Label(frame, text="설치 가이드 보기", fg="blue", cursor="hand2", font=underline_font)
    guide_label.grid(row=3, column=0, columnspan=3, padx=0, pady=10)
    guide_label.bind("<Button-1>", lambda e: webbrowser.open("https://gall.dcinside.com/mgallery/board/view/?id=atelierseries&no=88890"))

    root.mainloop()

# 텍스트 박스에 메시지를 출력하는 함수
def print_message(Message):
    root.after(0, lambda: console_box.config(state=tk.NORMAL))  # 텍스트 박스를 수정 가능 상태로 전환
    root.after(0, lambda: console_box.insert(tk.END, Message + "\n"))
    root.after(0, lambda: console_box.see(tk.END))
    root.after(0, lambda: console_box.yview(tk.END))  # 항상 마지막 메시지로 스크롤

# 텍스트 박스를 지우는 함수
def clear_textbox(*args):
    console_box.config(state=tk.NORMAL)  # 입력 가능 상태로 변경
    console_box.delete(1.0, tk.END)  # 텍스트 박스 내용 삭제
    console_box.config(state=tk.DISABLED)  # 다시 입력 불가능 상태로 변경

# 타이틀 선택 시 버튼을 활성화시키는 함수
def update_button_state(*args):
    if selected_title.get() == "타이틀 선택":
        patch_button.config(state=DISABLED)
    else:
        patch_button.config(state=NORMAL)

# 패치 실행
def run_patch():
    try:
        title = selected_title.get()  # 드롭다운 메뉴에서 선택한 타이틀
        url = DB.get(selected_title.get(), [None])[1]  # 선택된 타이틀의 URL 가져오기
    
        print(f"Starting download for: {title}") # 디버깅 메시지
        print(f"download from: {url}") # 디버깅 메시지
        threading.Thread(target=download_file, args=(title,)).start()
        print("Thread started successfully.") # 디버깅 메시지
    
    except Exception as e:
        print(f"Error starting download thread: {e}") # 예외 발생 시 출력

def find_library_path(title):
    global library_path  # 전역 변수 선언
    found = False

    # library_data의 경로와 folder_name이 포함된 리스트 검색
    for entry in steam_path.library_data:
        path = entry[0]  # path는 첫 번째 요소
        # 해당 경로에 folder_name 폴더가 존재하는지 확인
        if os.path.exists(os.path.join(path, DB[title][0])):
            library_path = path
            found = True
            break  # 일치하는 경로를 찾으면 종료
    
    if not found:
        library_path = "Not found"
        print_message("스팀 라이브러리 경로를 찾지 못했습니다.")

# 라이브러리 경로 초기화
def set_library(title):
    global library_path  # 전역 변수 선언

    if not library_list:
        messagebox.showerror("오류", "스팀이 설치되지 않았습니다.")
    else:
        find_library_path(title)
        if title == "네르케와 전설의 연금술사들":
            print_message(f"{title}을 기반으로 경로가 설정되었습니다.")
        else:
            print_message(f"{title}를 기반으로 경로가 설정되었습니다.")

# 다운로드 및 압축 해제 함수
def download_file(title):
    try:
        # 라이브러리가 지정되지 않은 경우 오류 메시지 출력
        if library_path == "Not found":
            if title == "네르케와 전설의 연금술사들":
                messagebox.showerror("오류", f"{title}이 설치되지 않았습니다.")
                return
            else:
                messagebox.showerror("오류", f"{title}가 설치되지 않았습니다.")
                return
        else:
            # 메뉴 비활성화
            patch_button.config(state=tk.DISABLED)
            dropdown.config(state=tk.DISABLED)

            # 경로 설정
            current_dir = os.path.dirname(sys.executable)  # 패치 프로그램 경로
            temp_dir = os.path.join(current_dir, 'temp') # temp 폴더 경로
            os.makedirs(temp_dir, exist_ok=True)  # temp 폴더가 존재하지 않을 경우 폴더 생성
            save_path = os.path.join(temp_dir, f"{title}.7z")  # 압축 파일 저장 경로

            # 콘솔 박스 입력 가능 상태로 변경
            console_box.config(state=tk.NORMAL)
            
            print_message("패치에 필요한 파일을 다운로드하는 중입니다.")
            print_message("잠시만 기다려주세요...")
            print_message("이 작업은 환경에 따라 1분 이상 소요될 수 있습니다.")

            # 다운로드
            download_url = DB[title][1] # 다운로드 URL

            try:
                gdown.download(download_url, save_path, quiet=True)
            except Exception as e:
                print_message(f"다운로드 실패: {e}") # 디버깅 메시지
                return

            print_message("다운로드가 완료되었습니다.")

            # 압축 해제
            print_message("압축을 해제하는 중입니다.")
            print_message("잠시만 기다려주세요...")
            
            with py7zr.SevenZipFile(save_path, mode='r') as archive:
                archive.extractall(path=temp_dir)  # temp 폴더에 내용물 직접 해제
                print_message("압축 해제가 완료되었습니다.")

            # 압축 파일 삭제
            os.remove(save_path)
            print_message("압축 파일을 삭제하였습니다.")

            # 패치 실행
            print_message("한국어 패치를 설치합니다.")
            
                        # 패치 실행
            apply_func = {
                "로로나의 아틀리에 DX": apply_rorona,
                "토토리의 아틀리에 DX": apply_totori,
                "메루루의 아틀리에 DX": apply_meruru,
                "아샤의 아틀리에 DX": apply_ayesha,
                "에스카&로지의 아틀리에 DX": apply_escha,
                "샤리의 아틀리에 DX": apply_shallie,
                "소피의 아틀리에 DX": apply_sophie,
                "피리스의 아틀리에 DX": apply_firis,
                "리디&수르의 아틀리에 DX": apply_lydie,
                "네르케와 전설의 연금술사들": apply_nelke,
                "루루아의 아틀리에": apply_lulua,
                "라이자의 아틀리에": apply_ryza,
            }

            if title in apply_func:
                apply_func[title]()

    except Exception as e:
        print_message(f"Error downloading {title}: {e}")
    finally:
        console_box.config(state=tk.DISABLED)
        patch_button.config(state=tk.NORMAL)
        dropdown.config(state=tk.NORMAL)

def apply_rorona():
    path = os.path.join(library_path, "Atelier Rorona ~The Alchemist of Arland~ DX")  # 게임 설치 경로
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

    print_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "로로나의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

def apply_totori():
    path = os.path.join(library_path, "Atelier Totori ~The Adventurer of Arland~ DX")  # 게임 설치 경로
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

    print_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "토토리의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

def apply_meruru():
    path = os.path.join(library_path, "Atelier Meruru ~The Apprentice of Arland~ DX")  # 게임 설치 경로
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

    print_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "메루루의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

def apply_ayesha():
    path = os.path.join(library_path, "Atelier Ayesha DX")  # 게임 설치 경로
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

    print_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "아샤의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

def apply_escha():
    path = os.path.join(library_path, "Atelier Escha and Logy DX")  # 게임 설치 경로
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

    print_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "에스카&로지의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

def apply_shallie():
    path = os.path.join(library_path, "Atelier Shallie DX")  # 게임 설치 경로
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

    print_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "샤리의 아틀리에 DX\n한국어 패치가 완료되었습니다!")

def apply_sophie():
    path = os.path.join(library_path, "Atelier Sophie DX")  # 게임 설치 경로
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

    print_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "소피의 아틀리에 DX\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 일본어로 변경해주세요.")

def apply_firis():
    path = os.path.join(library_path, "Atelier Firis DX")  # 게임 설치 경로
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

    print_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "피리스의 아틀리에 DX\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 일본어로 변경해주세요.")

def apply_lydie():
    path = os.path.join(library_path, "Atelier Lydie and Suelle DX")  # 게임 설치 경로
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

    print_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "리디&수르의 아틀리에 DX\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 일본어로 변경해주세요.")

def apply_nelke():
    path = os.path.join(library_path, "Nelke and the Legendary Alchemists Ateliers of the New World")  # 게임 설치 경로
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

    print_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "네르케와 전설의 연금술사들\n한국어 패치가 완료되었습니다!")

def apply_lulua():
    path = os.path.join(library_path, "Atelier Lulua")  # 게임 설치 경로
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

    print_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "루루아의 아틀리에\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 일본어로 변경해주세요.")

def apply_ryza():
    path = os.path.join(library_path, "Atelier Ryza")  # 게임 설치 경로
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

    print_message("패치가 완료되었습니다.")

    # 패치가 완료된 후 메시지 박스 표시
    messagebox.showinfo("패치 완료", "라이자의 아틀리에\n한국어 패치가 완료되었습니다!\n\n스팀에서 게임 언어를 중국어 번체로 변경해주세요.")

# GUI 실행
create_gui()

# pyinstaller --onefile --windowed --hidden-import=gdown --icon=icon.ico --add-data "icon.png;." Atelier_Korean_Patch.py
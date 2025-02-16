import os
import random
import subprocess
import tempfile
import time
import signal
import sys

systems = ["win10", "macos15", "macos14"]
browsers = ["chrome", "firefox", "safari"]
chrome_versions = [122, 123, 124, 125, 126, 127]
firefox_versions = [113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128]
safari_versions_macos14 = [17]
safari_versions_macos15 = [18]

temp_dir = tempfile.mkdtemp(prefix="chrome_profiles")
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

def get_chrome_path():
    program_files = os.environ.get('ProgramFiles', 'C:\\Program Files')
    chrome_path = os.path.join(program_files, 'Google', 'Chrome', 'Application', 'chrome.exe')
    return chrome_path

def close_chrome_process(process):
    try:
        process.terminate()
        process.wait()  # Ensure the process has closed
        print("Chrome process closed.")
    except Exception as e:
        print(f"Error closing Chrome process: {e}")

def open_profiles(n):
    chrome_processes = []
    for i in range(1, 6):
        system_name = random.choice(systems)
        browser_name = random.choice(browsers)

        if browser_name == "chrome":
            browser_version = random.choice(chrome_versions)
        elif browser_name == "firefox":
            browser_version = random.choice(firefox_versions)
        elif browser_name == "safari":
            if system_name == "macos14":
                browser_version = random.choice(safari_versions_macos14)
            elif system_name == "macos15":
                browser_version = random.choice(safari_versions_macos15)

        profile_folder = os.path.join(temp_dir, f"profile{n}{i}")
        if not os.path.exists(profile_folder):
            os.makedirs(profile_folder)

        random_url = f"https://www.browserling.com/browse/{system_name}/{browser_name}{browser_version}/https://www.bilibili.com/video/BV1vx4y1e7t2/"

        chrome_path = get_chrome_path()

        print(f"启动第 {n}-{i} 个配置文件：系统={system_name} 浏览器={browser_name} 版本={browser_version}...")

        try:
            process = subprocess.Popen([
                chrome_path, 
                "--user-data-dir=" + profile_folder, 
                "--profile-directory=Profile " + str(i), 
                "--no-first-run", 
                "--disable-extensions", 
                "--disable-plugins", 
                random_url
            ])
            chrome_processes.append(process)
            print(f"第 {n}-{i} 个配置文件启动成功，正在浏览：{random_url}")
        except Exception as e:
            print(f"第 {n}-{i} 个配置文件启动失败，错误信息：{e}")
            
        time.sleep(5)

    return chrome_processes

def main():
    try:
        n = 1
        while True:
            chrome_processes = open_profiles(n)
            print("Waiting for 60 seconds before closing Chrome instances...")
            time.sleep(60)

            # Close the opened Chrome processes after 60 seconds
            for process in chrome_processes:
                close_chrome_process(process)
                
            n += 1
    except KeyboardInterrupt:
        print("User exited the script.")
        sys.exit(0)

if __name__ == "__main__":
    main()

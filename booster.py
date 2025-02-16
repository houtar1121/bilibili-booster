import os
import random
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

systems = ["win10", "macos15", "macos14"]
browsers = ["chrome", "firefox", "safari"]
chrome_versions = [122, 123, 124, 125, 126, 127]
firefox_versions = [113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128]
safari_versions_macos14 = [17]
safari_versions_macos15 = [18]

temp_dir = tempfile.mkdtemp(prefix="chrome_profiles")
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

def get_chrome_options(system_name, browser_version):
    options = ChromeOptions()
    options.add_argument(f"user-data-dir={temp_dir}/profile_{random.randint(1, 5)}")
    options.add_argument(f"profile-directory=Profile {random.randint(1, 5)}")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--headless")  # 无头模式
    return options

def start_chrome_browser(system_name, browser_version, i):
    options = get_chrome_options(system_name, browser_version)
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    random_url = f"https://www.browserling.com/browse/{system_name}/{browser_name}{browser_version}/https://www.bilibili.com/video/BV1vx4y1e7t2/"
    print(f"启动第 {i} 个配置文件：系统={system_name} 浏览器={browser_name} 版本={browser_version}...")

    try:
        driver.get(random_url)
        print(f"第 {i} 个配置文件启动成功，正在浏览：{random_url}")
        time.sleep(40)  # 浏览 40 秒后关闭
        driver.quit()
        print(f"第 {i} 个配置文件已关闭。")
    except Exception as e:
        print(f"第 {i} 个配置文件启动失败，错误信息：{e}")
        driver.quit()

def run_browser_instance(i):
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

    start_chrome_browser(system_name, browser_version, i)

def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(run_browser_instance, i) for i in range(1, 11)]
        for future in futures:
            future.result()  # 等待所有线程完成

    print("所有浏览器实例执行完毕。")

if __name__ == "__main__":
    main()

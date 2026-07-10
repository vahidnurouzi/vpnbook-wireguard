import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print("در حال باز کردن صفحه VPNBook...")
    driver.get("https://www.vpnbook.com/zh/freevpn/wireguard-vpn")
    
    wait = WebDriverWait(driver, 20)
    
    try:
        server_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Germany')]")))
        server_element.click()
        print("سرور آلمان انتخاب شد.")
    except Exception as e:
        print("خطا در انتخاب سرور. ممکنه نیاز به بروزرسانی Selector داشته باشی.")
        print(e)
    
    time.sleep(5)
    
    try:
        download_button = driver.find_element(By.XPATH, "//button[contains(text(),'Download')]")
        download_button.click()
        print("دکمه دانلود کلیک شد.")
    except:
        print("دکمه دانلود پیدا نشد.")
    
    time.sleep(5)
    
    try:
        config_content = driver.find_element(By.TAG_NAME, "pre").text
    except:
        config_content = driver.find_element(By.TAG_NAME, "textarea").text
    
    if config_content:
        with open("vpnbook-wg.conf", "w") as f:
            f.write(config_content)
        print("فایل کانفیگ جدید با موفقیت ذخیره شد.")
    else:
        print("خطا: محتوای کانفیگ پیدا نشد.")

except Exception as e:
    print(f"یک خطا رخ داد: {e}")

finally:
    driver.quit()

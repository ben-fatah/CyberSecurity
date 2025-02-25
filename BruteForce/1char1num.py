from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import itertools
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def brute_force_attack():
    # إعداد متصفح Chrome مع تحديد المسار
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome"  # مسار Google Chrome

    # إنشاء ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://alaboudi1.github.io/guessPassword/")  # رابط الموقع

    # قائمة الأحرف الإنجليزية الصغيرة والأرقام
    letters = "abcdefghij"
    numbers = "0123456"

    # إنشاء قائمة بجميع التوليفات الممكنة (حرف واحد ورقم واحد)
    password_list = ["".join(combo) for combo in itertools.product(letters, numbers)]

    found = False

    for password in password_list:
        if found:
            break

        try:
            # اختر النوع المناسب (1 character, 1 number) باستخدام القائمة المنسدلة
            dropdown = driver.find_element(By.ID, "passwordType")
            dropdown.click()
            dropdown_option = driver.find_element(By.XPATH, "//option[text()='1 character, 1 number']")
            dropdown_option.click()

            # أدخل كلمة المرور
            input_box = driver.find_element(By.ID, "passwordInput")
            input_box.clear()
            input_box.send_keys(password)

            # اضغط على زر "Guess"
            guess_button = driver.find_element(By.ID, "guess")
            guess_button.click()

            # انتظر تحديث النتيجة
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "result"))
            ).text

            # تحقق من النتيجة
            if "is Correct!" in result:
                print(f"[+] Password found: {password}")
                found = True
            else:
                print(f"[-] Tried password: {password}")
        except Exception as e:
            print(f"Error: {e}")

    if not found:
        print("[-] No password found in the list.")

    # أغلق المتصفح
    driver.quit()

if __name__ == "__main__":
    brute_force_attack()

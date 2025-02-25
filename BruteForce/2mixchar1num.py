from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import itertools
import time

def brute_force_attack():
    # إعداد متصفح Chrome مع تحديد الإعدادات الصحيحة
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome"  # تأكد من مسار Google Chrome
    options.add_argument("--headless")  # تشغيل المتصفح في الخلفية (اختياري)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # إعداد ChromeDriver باستخدام webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # فتح الموقع
    driver.get("https://alaboudi1.github.io/guessPassword/")

    # قائمة الأحرف الكبيرة، الصغيرة، والأرقام
    uppercase_letters = "ABCDEFGHIJ"
    lowercase_letters = "abcdefghij"
    numbers = "0123456"

    # إنشاء التوليفات الممكنة (حرف كبير، حرف صغير، ورقم)
    password_list = [
        "".join(combo)
        for combo in itertools.product(uppercase_letters, lowercase_letters, numbers)
    ]

    found = False
    attempt_count = 0

    for password in password_list:
        if found:
            break

        try:
            attempt_count += 1

            # إعادة تشغيل المتصفح بعد 500 محاولة لتجنب مشاكل الأداء
            if attempt_count % 500 == 0:
                driver.quit()
                driver = webdriver.Chrome(service=service, options=options)
                driver.get("https://alaboudi1.github.io/guessPassword/")

            # اختر النوع المناسب (2 mixed case characters, 1 number)
            dropdown = driver.find_element(By.ID, "passwordType")
            dropdown.click()
            dropdown_option = driver.find_element(By.XPATH, "//option[text()='2 mixed case characters, 1 number']")
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
                if attempt_count % 100 == 0:  # طباعة كل 100 محاولة
                    print(f"[-] Attempted {attempt_count} passwords so far...")

            # أضف تأخيرًا بسيطًا بين المحاولات لتجنب حظر الموقع
            time.sleep(0.1)

        except Exception as e:
            print(f"Error: {e}")

    if not found:
        print("[-] No password found in the list.")

    # أغلق المتصفح
    driver.quit()

if __name__ == "__main__":
    brute_force_attack()

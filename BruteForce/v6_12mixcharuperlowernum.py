from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import itertools
def generate_passwords():
    uppercase_letters = "ABCDEFGHIJ"
    lowercase_letters = "abcdefghij"
    numbersc = "0123456"
    numbersf = "123456"

    for part1 in itertools.product(uppercase_letters, lowercase_letters, numbersf):
        for part2 in itertools.product(uppercase_letters, lowercase_letters, numbersc):
            for part3 in itertools.product(uppercase_letters, lowercase_letters, numbersc):
                for part4 in itertools.product(uppercase_letters, lowercase_letters, numbersc):
                    for part5 in itertools.product(uppercase_letters, lowercase_letters, numbersc):
                        for part6 in itertools.product(uppercase_letters, lowercase_letters, numbersc):
                            yield "".join(part1) + "".join(part2) + "".join(part3) + "".join(part4) + "".join(part5) + "".join(part6)


    
def brute_force_attack():
    # النطاق المحدد للأحرف الكبيرة، الصغيرة، والأرقام
    uppercase_letters = "ABCDEFGHIJ"
    lowercase_letters = "abcdefghij"
    numbers = "0123456"

    # توليد كلمات المرور بناءً على الأقسام الثابتة والمتحركة


    



    found = False
    attempt_count = 0

    # إعداد خيارات Chrome لتسريع العملية
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # تشغيل المتصفح في الخلفية
    chrome_options.add_argument("--disable-gpu")  # تعطيل GPU لتسريع العملية
    chrome_options.add_argument("--no-sandbox")  # تعطيل Sandbox لتسريع العملية
    chrome_options.add_argument("--disable-dev-shm-usage")  # تجنب مشاكل الذاكرة

    # إعداد ChromeDriver باستخدام webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://alaboudi1.github.io/guessPassword/")
    except Exception as e:
        print(f"Failed to connect to the server: {e}")
        driver.quit()
        exit()

    try:
        # انتظر تحميل العناصر الأساسية
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "passwordType")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "passwordInput")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "guess")))

        # Cache العناصر لتجنب إعادة البحث عنها
        dropdown = Select(driver.find_element(By.ID, "passwordType"))
        input_box = driver.find_element(By.ID, "passwordInput")
        guess_button = driver.find_element(By.ID, "guess")

        # تقسيم المحاولات إلى دفعات
        for password in generate_passwords():
            attempt_count += 1
            print(f"[-] Trying password: {password} (Attempt {attempt_count})")  # طباعة كلمة المرور

            try:
                # اختر النوع المناسب
                dropdown.select_by_visible_text("Mix of 16 characters (upper, lower, numbers)")
            except:
                print("[-] Dropdown option not found. Trying again...")
                continue

            # أدخل كلمة المرور
            input_box.clear()
            input_box.send_keys(password)

            # اضغط على زر Guess
            guess_button.click()

            # تحقق من النتيجة
            result = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "result"))).text
            if "is Correct!" in result:
                print(f"[+] Password found: {password}")
                found = True
                break

            # إذا وصلت إلى 1000 محاولة، أعد تحميل الصفحة
            if attempt_count % 1000 == 0:
                print("Reached 1000 attempts, reloading page...")
                driver.refresh()
                # إعادة تعيين العناصر بعد إعادة تحميل الصفحة
                dropdown = Select(driver.find_element(By.ID, "passwordType"))
                input_box = driver.find_element(By.ID, "passwordInput")
                guess_button = driver.find_element(By.ID, "guess")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # أغلق المتصفح عند الانتهاء
        driver.quit()

    if not found:
        print("[-] Password not found.")

if __name__ == "__main__":
    brute_force_attack()

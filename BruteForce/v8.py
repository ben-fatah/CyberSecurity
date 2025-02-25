from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import itertools

# دالة لتوليد كلمات المرور بناءً على النمط المحدد
def generate_passwords():
    uppercase_letters = "ABCDEF"
    lowercase_letters = "abcdef"
    numbers = "123456"

    # توليد الأجزاء بناءً على النمط المحدد
    for uppercase in itertools.permutations(uppercase_letters):
        for lowercase in itertools.permutations(lowercase_letters):
            for number in itertools.permutations(numbers):
                password = (
                    uppercase[0] + lowercase[0] + number[0] +
                    uppercase[1] + lowercase[1] + number[1] +
                    uppercase[2] + lowercase[2] + number[2] +
                    uppercase[3] + lowercase[3] + number[3] +
                    uppercase[4] + lowercase[4] + number[4] +
                    uppercase[5] + lowercase[5] + number[5]
                )
                # التحقق من عدم تكرار الأحرف أو الأرقام
                if len(set(password)) == len(password):
                    yield password

# دالة لتنفيذ الهجوم
def brute_force_attack():
    found = False
    attempt_count = 0

    # إعداد خيارات Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # إعداد ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://alaboudi1.github.io/guessPassword/")
    except Exception as e:
        print(f"Failed to connect to the server: {e}")
        driver.quit()
        return

    try:
        # انتظار حتى تحميل العناصر
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "passwordType")))
        dropdown = Select(driver.find_element(By.ID, "passwordType"))
        input_box = driver.find_element(By.ID, "passwordInput")
        guess_button = driver.find_element(By.ID, "guess")

        # تجربة كلمات المرور
        for password in generate_passwords():
            attempt_count += 1
            print(f"[-] Trying password: {password} (Attempt {attempt_count})")

            try:
                dropdown.select_by_visible_text("Mix of 16 characters (upper, lower, numbers)")
            except:
                print("[-] Dropdown option not found. Trying again...")
                continue

            input_box.clear()
            input_box.send_keys(password)
            guess_button.click()

            # تحقق من النتيجة
            result = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "result"))).text
            if "is Correct!" in result:
                print(f"[+] Password found: {password}")
                found = True
                break

            # إعادة تحميل الصفحة بعد 1000 محاولة
            if attempt_count % 1000 == 0:
                print("Reached 1000 attempts, reloading page...")
                driver.refresh()
                dropdown = Select(driver.find_element(By.ID, "passwordType"))
                input_box = driver.find_element(By.ID, "passwordInput")
                guess_button = driver.find_element(By.ID, "guess")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    if not found:
        print("[-] Password not found.")


if __name__ == "__main__":
    brute_force_attack()
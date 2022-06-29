import time
import pyautogui
import os
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

error_type = ''


def driver_setup():
    username_file = open('usernames.txt', 'r', encoding="utf8")
    usernames = username_file.readlines()
    username_file.close()

    # proxy_list = open("proxy_list.txt", 'r')
    # proxies = proxy_list.readlines()
    # proxy = random.choices(proxies)

    number = 0

    for username in usernames:

        ser = Service("chromedriver.exe")
        op = webdriver.ChromeOptions()
        # op.add_extension("touch.crx")
        # op.add_extension("cor.crx")
        op.add_argument('--ignore-ssl-errors=yes')
        op.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(service=ser, options=op)

        driver.get("https://www.instagram.com")

        try:
            element_username = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            element_password = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )

            element_login_button = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/main/article/div[2]/div[1]/div["
                                                          "2]/form/div/div[3]/button"))
            )
        except Exception as E:
            unchange_username = open('unchanged_usernames.txt', 'a')
            unchange_username.write(f"{username}")
            unchange_username.close()
            continue

        try:
            element_username.send_keys(username.split(':')[0])
            element_password.send_keys(username.split(':')[1])
            time.sleep(1)
            element_login_button.click()

        except Exception as E:
            print("Error: ")

        time.sleep(7)

        try:
            alert = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(By.XPATH, "//*[@id='slfErrorAlert']")
            )
            if "incorrect" in alert.text:
                wrong_pas = open("wrong_password.txt", "a")
                wrong_pas.write(username)
                wrong_pas.close()
                continue

            elif "username" in alert.text:
                wrong_user = open("wrong_username.txt", "a")
                wrong_user.write(username)
                wrong_user.close()
                continue

            else:
                unchange_username = open('unchanged_usernames.txt', 'a')
                unchange_username.write(f"{username}")
                unchange_username.close()
                continue

        except Exception as e:
            driver.get(f"https://instagram.com/{username.split(':')[0]}")

        try:
            profile_pic_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_aadn"))
            )
            profile_pic_element.click()
        except Exception as E:
            unchan_file = open("unchanged_usernames.txt", "a")
            unchan_file.write(username)
            unchan_file.close()
            driver.close()
            continue

        time.sleep(2)

        random_pick = random.choice([x for x in os.listdir("E:\\Personal WorkSpace\\InstaAut\\Images\\") if
                                     os.path.isfile(os.path.join("E:\\Personal WorkSpace\\InstaAut\\Images\\", x))])
        pyautogui.write(f"E:\\Personal WorkSpace\\InstaAut\\Images\\{random_pick}")
        pyautogui.press("enter")
        time.sleep(5)

        try:
            driver.get("https://instagram.com/accounts/edit")

            # names = open("names.txt", "r")
            # names_list = names.readlines()
            # names.close()

            # #Changing Name
            # change_name = driver.find_element(By.XPATH, "//*[@id='pepName']")
            # change_name.clear()
            # change_name.send_keys(random.choice(names_list))

            # Changing Bio
            # getting_bio = open("bio.txt", "r", encoding="utf8")
            # bio_list = getting_bio.readlines()
            # getting_bio.close()
            # bio_field = driver.find_element(By.XPATH, "//*[@id='pepBio']")
            # bio_field.clear()
            # bio_field.send_keys(random.choice(bio_list))

            # Changing Email
            change_email = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="pepEmail"]'))
            )
            changed_mail = username.split(":")[2]
            time.sleep(1)
            change_email.clear()
            time.sleep(1)
            change_email.send_keys(changed_mail)

        except Exception as E:
            print(E)
            unchan_file = open("unchanged_usernames.txt", "a")
            unchan_file.write(username)
            unchan_file.close()
            driver.close()
            continue

        time.sleep(2)

        try:
            submit_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/article/form/div[10]/div/div/button")
            )
            submit_btn.click()
        except Exception as E:
            print(E)
            unchan_file = open("unchanged_usernames.txt", "a")
            unchan_file.write(f"{username}")
            unchan_file.close()
            driver.close()
            continue

        time.sleep(3)

        # Now Confirming the Email
        # First we will open the new tab
        driver.execute_script('''window.open("about:blank");''')
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://firstmail.online/mail/")

        second_username_element = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='rcmloginuser']"))
        )

        second_password_element = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='rcmloginpwd']"))
        )

        second_username_element.send_keys(username.split(":")[2])
        second_password_element.send_keys(username.split(":")[3])

        time.sleep(1)
        # second_submit_btn =  driver.find_element(By.XPATH, "//*[@id='rcmloginsubmit']")
        # second_submit_btn.click()

        time.sleep(2)

        try:
            confirm_message = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[4]/table[2]/tbody/tr/td[3]"))
            )
        except TimeoutException as e:
            driver.refresh()
            try:
                confirm_message = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/div[3]/div[4]/table[2]/tbody/tr/td[3]"))
                )
            except TimeoutException as f:
                continue

        # create action chain object
        action = ActionChains(driver)
        # double-click the item
        action.double_click(on_element=confirm_message)

        # perform the operation
        action.perform()

        last_confirm_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div["
                                            "2]/div/div/table/tbody/tr/td/table/tbody/tr["
                                            "4]/td/table/tbody/tr/td/table/tbody/tr["
                                            "2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr["
                                            "3]/td/a/table/tbody/tr/td"))
        )
        last_confirm_btn.click()
        time.sleep(5)
        print("successfully changed the profile and mail of the Account")
        changed_file = open("changed_usernames.txt", "a")
        # number = 1 + number
        #
        # print(f"On the {number} username out of {len(usernames)}")
        #
        changed_file.write(username)
        changed_file.close()
        driver.quit()


def second_round():
    os.remove("usernames.txt")

    with open('unchanged_usernames.txt', 'r') as unchange_file, open('usernames.txt', 'a') as username_file:
        # read content from first file
        for line in unchange_file:
            # append content to second file
            username_file.write(line)
    os.remove("unchanged_usernames.txt")

    driver_setup()


driver_setup()  # Will run the first time

unchanged_file = open("unchanged_usernames.txt", "r")
unchanged_list = unchanged_file.readlines()
unchanged_file.close()

if len(unchanged_list) > 0:
    print("There are still some usernames that didn't change")
    second_round()
else:
    exit()

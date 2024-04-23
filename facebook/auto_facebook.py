import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains



class FacebookScript:
    def __init__(self, username, password, friend_url):
        self.username = username
        self.password = password
        self.friend_url = friend_url
        self.driver = None
        self.wait = None

    def run(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")  # 禁用通知
        chrome_options.add_argument("--disable-save-password-bubble")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        # 创建一个Chrome浏览器实例
        self.driver = webdriver.Chrome(chrome_options)

        self.driver.get("https://www.facebook.com/login/")  # 打开网页
        self.driver.maximize_window()  # 最大化

        self.wait = WebDriverWait(self.driver, 10000)  # 等待网页加载完成
        self.login()

    def login(self):
        # 账号输入框
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#email"))).send_keys(self.username)
        # 密码输入框
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#pass"))).send_keys(self.password)
        # 登录按钮
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#loginbutton"))).click()

        time.sleep(2)
        self.enter_friend()

    def enter_friend(self):
        # driver.get("https://www.facebook.com/profile.php?id=100091053695643&sk=friends")
        self.driver.get(self.friend_url)
        wait = WebDriverWait(self.driver, 100)
        # 创建ActionChains实例
        actions = ActionChains(self.driver)
        for raw in range(0, 10):
            # 滚动到页面底部
            actions.send_keys(Keys.END).perform()
            time.sleep(1)
            print('scrolling', raw)

        # 获取用户列表
        user_hrefs = []
        user_els = wait.until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, ".x78zum5.x1q0g3np.x1a02dak.x1qughib  .x6s0dn4.x1lq5wgf.xgqcy7u.x30kzoy")))
        # user_els = user_els[1:5]
        for user_el in user_els:
            try:
                a_tag = WebDriverWait(user_el, 1).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy')))
                href = a_tag.get_attribute('href')  # 获取 <a> 标签的 href 属性值
                user_hrefs.append(href)
                print('user_el href', href)
            except Exception as e:
                print('Error:', e)
        for href in user_hrefs:
            self.enter_detail(href)

    def find_el(self, profile, message):
        flag = [True]
        if profile:
            message_element = self.driver.execute_script('''
                           const element = document.querySelector("div.xsgj6o6.xw3qccf.x1xmf6yo.x1w6jkce.xusnbm3 img[src='https://static.xx.fbcdn.net/rsrc.php/v3/y9/r/YjBUcSAL8TC.png']").parentNode
                           element.click();
                           console.log(element);
                           return element;
                       ''')
        else:
            message_element = self.driver.execute_script('''
                    const element = document.querySelector(".x1n2onr6.x1ja2u2z.x78zum5.x2lah0s.xl56j7k.x6s0dn4 img[src='https://static.xx.fbcdn.net/rsrc.php/v3/y9/r/YjBUcSAL8TC.png']").parentNode
                    element.click();
                    console.log(element);
                    return element;
                ''')

        def interval_task():
            nonlocal flag
            p_input = self.driver.execute_script('''
                           const element = document.querySelector("div.x78zum5.x13a6bvl div[aria-label='Message'] p.xat24cr.xdj266r")
                           console.log(element);
                           return element;
                       ''', )
            print('p_input', p_input)

            # 检查是否成功获取到 p_input
            if p_input is not None:

                p_input.send_keys(message)
                time.sleep(1)
                p_input.send_keys(Keys.ENTER)
                self.driver.execute_script('''
                    close_el=document.querySelector('div[aria-label="Close chat"]')
                    close_el.click()
                    ''')
                time.sleep(1)
                print('send message successful:', message, p_input)
                # 获取到 p_input 后取消定时器
                flag[0] = False  # 修改闭包变量
            else:
                print('send message failed:', message)

        while flag[0]:
            interval_task()
            # 每隔 1 秒执行一次 interval_task
            time.sleep(2)
        print("即将进入下一个好友的聊天窗口")

    def enter_detail(self, href):
        try:
            print('href', href)
            self.driver.get(href)  # 打开网页
            wait = WebDriverWait(self.driver, 10000)  # 等待网页加载完成
            # time.sleep(5000)
            # 获取当前页面的 URL
            current_url = self.driver.current_url
            # 检查是否包含 'profile' 和 'id'
            if 'profile' in current_url and 'id' in current_url:
                print("URL 包含 'profile' 和 'id'")
                profile = True
            else:
                print("URL 不包含 'profile' 或 'id'")
                profile = False

            self.find_el(profile, 'nice to meet you')
            time.sleep(1)


        except Exception as e:
            print('Error:', e)





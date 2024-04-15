import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys
from ai.zhipu_ai import get_csdn_article
from lib.same_zh import chinese_similarity


def login(wait):
    argv_local = sys.argv[0] if len(sys.argv) >= 1 else 2
    # 等待登录框出现
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".login-box-tabs-items > span:last-child"))).click()

    # 输入用户名和密码
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))).send_keys(
        "18180276692")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[autocomplete='current-password']"))).send_keys(
        "1103661612zl")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".icon-nocheck"))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".login-form-item button"))).click()

    time.sleep(10)

    def create_csdn_blog(article_title="", aritcle_types=None):
        if aritcle_types is None:
            aritcle_types = ["面试", "前端", "javaScript", "AI", "Python", "自动化脚本"]
        driver.get("https://mp.csdn.net/mp_blog/creation/editor")  # 打开网页
        wait = WebDriverWait(driver, 10)
        time.sleep(7)
        driver.execute_script("window.scrollTo(0, 2000)")
        time.sleep(7)
        driver.execute_script("window.scrollTo(0, 2000)")
        # 设置专栏
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".tag__item-list"))).click()
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".tag__options-list > .tag__option-box:first-child"))).click()
        driver.execute_script("document.body.click()")
        time.sleep(2)

        def set_tag(text):

            # 设置标签
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".tag__btn-tag"))).click()
            wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".mark_selection_box_header input"))).send_keys(
                text)
            time.sleep(1)
            # 按下回车键
            wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".mark_selection_box_header input"))).send_keys(Keys.ENTER)
            time.sleep(1)
            driver.execute_script("document.body.click()")

        for aritcle_type in aritcle_types:
            set_tag(aritcle_type)
        # 设置标题和内容
        content = get_csdn_article(article_title)
        # content = get_csdn_article_by_wenxin(article_title)
        print(content)
        title_textarea = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".input__title textarea")))
        title_textarea.send_keys(content['title'])
        # 切换到login iframe 中
        content_iframe = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "iframe.cke_wysiwyg_frame")))
        driver.switch_to.frame(content_iframe)
        content_body = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".cke_editable>p")))
        # 添加子元素
        driver.execute_script('''
                        var childElement = document.createElement("div");
                        childElement.innerHTML = arguments[0];
                        arguments[1].innerHTML = '';
                        arguments[1].appendChild(childElement)''', content['content'], content_body)
        time.sleep(20)
        content_body.send_keys("[[以上内容均由AI自动化生成发布,仅供参考,谢谢您的访问]]")
        driver.switch_to.default_content()
        time.sleep(2)
        driver.execute_script("document.body.click()")
        driver.execute_script("window.scrollTo(0, 20000)")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 20000)")
        time.sleep(4)
        driver.execute_script("window.scrollTo(0, 20000)")
        # 提取摘要
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".btn-getdistill"))).click()
        time.sleep(5)
        # 提交
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".btn-box .btn-outline-danger"))).click()
        time.sleep(5)
        try:
            time.sleep(5)
            print("开始创建文章", article_title)
        except Exception as e:
            print("登录失效，重新登录")
            login(wait)

    if argv_local == 1:
        try:
            argv_title = sys.argv[1]  # title
            argv_aritcle_types = sys.argv[1:]  # aritcle_types
            create_csdn_blog(argv_title, argv_aritcle_types)
        except Exception as e:
            create_csdn_blog()
    else:
        with open('question/local_questions.json', 'r', encoding='utf-8') as file:
            datas = json.load(file)
        for data in datas['server-values']:
            if any(chinese_similarity(data["title"], publish["title"]) > 0.7 for publish in datas["server-published"]):
                print("标题重复：", data["title"])
            else:
                print("开始创建博客：", data["title"])
                create_csdn_blog(data["title"], data["tags"])


if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    # 创建一个Chrome浏览器实例
    driver = webdriver.Chrome(chrome_options)

    driver.get("https://www.csdn.net/")  # 打开网页
    driver.maximize_window()  # 最大化

    wait = WebDriverWait(driver, 10) # 等待网页加载完成

    # 等待登录按钮出现
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".toolbar-btn-loginfun"))).click()

    # 切换到login iframe 中
    login_iframe = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "iframe[name='passport_iframe']")))
    driver.switch_to.frame(login_iframe)
    login(wait)

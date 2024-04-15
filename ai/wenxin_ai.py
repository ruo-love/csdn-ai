# AIP key vtR0KEy4c2VdR1y2r8Nu5VUgmFvrK78E
# Access Key ALTAKwwac2W0mAzYOG5zd8Yvgy
# Secret Key 19beab98cc254b02ba06344dc37aa333

import os
import qianfan
import markdown
# 使用安全认证AK/SK鉴权，通过环境变量初始化；替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk
os.environ["QIANFAN_ACCESS_KEY"] = "ALTAKwwac2W0mAzYOG5zd8Yvgy"
os.environ["QIANFAN_SECRET_KEY"] = "19beab98cc254b02ba06344dc37aa333"

chat_comp = qianfan.ChatCompletion()



def get_csdn_article_by_wenxin(title):
    # 指定特定模型
    resp = chat_comp.do(model="ERNIE-Bot", messages=[{
        "role": "user",
        "content": "我是一位程序员,请帮我写一篇关于" + title + "的高质量csdn博客,要求内容丰富 准确 严谨 正确,适当扩展内容,尽可能去示例说明细节,最好是在最前面给我加上目录方便阅读,谢谢你的帮助"

    }])
    html = markdown.markdown(resp.body['result'])
    html = '<h3 style="margin:20px 0;color:#e2855c">以下内容均由AI自动化生成发布,仅供参考,谢谢您的访问</h3><br>' + html + '<br><br>'
    return {
        "title": title,
        "content": html
    }


from zhipuai import ZhipuAI
import json
import markdown


client = ZhipuAI(api_key="432b814e216cba24d09b9c52c0a1f196.jf4kvde0vFLhFkSC")  # 填写您自己的APIKey




def get_csdn_article_title():
    # 读取json文件
    with open('../question/question.json', 'r', encoding='utf-8') as file:
        #
        datas = json.load(file)
        messages = []
        content = "我是一位前端开发面试官，我需要一道优质的面试题，你前面已经出过的题目,请一定不要再次出现了,知识范围请从[Vue、React、Html、css、js、浏览器知识、计算机网络、webpack、工程化、性能优化]中随机选择一个内容，请给我题目（标题），题要有针对性，聚焦某个特定的知识点，不要太宽泛，标题尽量精简不要太长,不要出现题目要求，只给我题目就行，我自己去补充内容,所有标题以'AI题库：'开头‘,最重要的是你前面已经存在过的题目,请一定不要在出现了,这是最重要的"
        for data in datas['values']:
            # 合并两个数组
            messages.append({"role": "user", "content": content})
            messages.append({"role": "assistant", "content": data})
        messages.append({"role": "user", "content": content})
        print(messages)
        response = client.chat.completions.create(
            model="glm-3-turbo",  # 填写需要调用的模型名称
            temperature=0.99,
            top_p=0.99,
            messages=messages
        )

        datas['values'].append(response.choices[0].message.content)
        with open('../question/question.json', 'w', encoding='utf-8') as file:
            json.dump(datas, file, indent=4, ensure_ascii=False)
        return response.choices[0].message.content


# 获取一篇csdn文章 自定义标题 or 随机ai标题
def get_csdn_article(title):
    if title:
        article_title = title
    else:
        article_title = get_csdn_article_title()
    response = client.chat.completions.create(
        model="glm-3-turbo",  # 填写需要调用的模型名称
        temperature=0.99,
        max_tokens=2048,
        messages=[
            {"role": "user",
             "content": "我是一位程序员,请帮我写一篇关于" + article_title + "的高质量csdn博客,要求内容丰富 准确 严谨 正确,适当扩展内容,尽可能去示例说明细节,最好是在最前面给我加上目录方便阅读,谢谢你的帮助"},
        ],
    )
    html = markdown.markdown(response.choices[0].message.content)
    html = '<h3 style="margin:20px 0;color:#e2855c">以下内容均由AI自动化生成发布,仅供参考,谢谢您的访问</h3><br>' + html + '<br><br>'
    print(html)
    return {
        "title": title,
        "content": html
    }


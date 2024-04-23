import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from facebook.auto_facebook import FacebookScript
from common import log
def submit():
    # 获取用户名和密码
    username = entry_username.get()
    password = entry_password.get()
    friend_url = entry_friend_url.get()
    # 创建一个 FacebookScript 实例
    facebook_script = FacebookScript(username, password, friend_url)
    # facebook_script.run()
    print(facebook_script)


root = ttk.Window()
root.geometry("1200x800")
root.title("Facebook")
# 创建一个 Root Frame
root_frame = ttk.Frame(root, borderwidth=1, relief="raised")
root_frame.pack(expand=True, fill="both")
root_frame.columnconfigure(0, weight=1)
root_frame.columnconfigure(1, weight=8)
# 创建一个 login Frame
form_frame = ttk.Frame(root_frame, borderwidth=1, relief="raised")
form_frame.grid(row=0, column=0, sticky="nsew")
form_frame.columnconfigure(0, weight=1)
form_frame.columnconfigure(1, weight=4)

# 创建用户名标签和输入框
label_username = ttk.Label(form_frame, text="用户名：")
label_username.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
entry_username = ttk.Entry(form_frame)
entry_username.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

# 创建密码标签和输入框
label_password = ttk.Label(form_frame, text="密码：")
label_password.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
entry_password = ttk.Entry(form_frame, show="*")
entry_password.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

# Friend url
label_friend_url = ttk.Label(form_frame, text="好友列表URL")
label_friend_url.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
entry_friend_url = ttk.Entry(form_frame)
entry_friend_url.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')

# 创建登录按钮
button_login = ttk.Button(form_frame, text="运行", bootstyle=SUCCESS, command=submit)
button_login.grid(row=3, columnspan=2, padx=5, pady=5, sticky='nsew')

# 创建一个 日志 Frame
log_frame = ttk.Frame(root_frame, borderwidth=1, relief="raised")
log_frame.grid(row=0, column=1, sticky="nsew")
log_frame.columnconfigure(0, weight=1)

# 创建一个日志显示框
log_text = ttk.Text(log_frame)
log_text.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

# 创建一个滚动条，用于滚动文本框中的内容
scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=log_text.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
# 将文本框与滚动条关联
log_text.config(yscrollcommand=scrollbar.set)





# 创建日志按钮
button_log = ttk.Button(log_frame, text="button_log", command=lambda: log(log_text, "Logging message"))
button_log.grid(row=1, column=0, padx=5, pady=5)

root.mainloop()

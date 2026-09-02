"""AI Desktop Chat - Deepseek集成版本

这个文件启动一个简单的Tkinter聊天窗口，通过ai_client与Deepseek AI进行交互。
使用config.py进行配置管理。
"""
import tkinter as tk
from tkinter import scrolledtext
import threading
import config
import ai_client


class ChatApp:
    def __init__(self, root):
        self.root = root
        root.title(config.WINDOW_TITLE)
        root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")

        # 聊天显示区
        self.chat_display = scrolledtext.ScrolledText(
            root, 
            state='disabled', 
            wrap='word', 
            font=(config.FONT_FAMILY, config.FONT_SIZE)
        )
        self.chat_display.pack(fill='both', expand=True, padx=8, pady=8)

        # 输入框和发送按钮
        frame = tk.Frame(root)
        frame.pack(fill='x', padx=8, pady=(0, 8))

        self.entry = tk.Entry(frame, font=(config.FONT_FAMILY, config.FONT_SIZE))
        self.entry.pack(side='left', fill='x', expand=True, padx=(0, 8))
        self.entry.bind('<Return>', lambda e: self.on_send())

        self.send_btn = tk.Button(frame, text='发送', command=self.on_send)
        self.send_btn.pack(side='right')

        # 对话历史
        self.history = [
            {"role": "system", "content": config.SYSTEM_PROMPT}
        ]

    def append_chat(self, role, text):
        """追加聊天消息到显示区"""
        self.chat_display.configure(state='normal')
        if role == 'user':
            self.chat_display.insert('end', f"你: {text}\n\n")
        else:
            self.chat_display.insert('end', f"Deepseek: {text}\n\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see('end')

    def on_send(self):
        """处理发送事件"""
        user_text = self.entry.get().strip()
        if not user_text:
            return
        
        self.entry.delete(0, 'end')
        self.append_chat('user', user_text)
        self.history.append({"role": "user", "content": user_text})

        # 在后台线程中调用AI，避免UI冻结
        threading.Thread(target=self.call_ai, args=(user_text,), daemon=True).start()

    def call_ai(self, user_text):
        """调用AI获取响应"""
        try:
            ai_text = ai_client.get_response(user_text, self.history)
            if ai_text is None:
                ai_text = "(没有可用的响应)"
        except Exception as e:
            ai_text = f"(调用AI时出错: {e})"
        
        # 保存助手消息到历史
        self.history.append({"role": "assistant", "content": ai_text})
        
        # 在主线程中更新UI
        self.root.after(0, lambda: self.append_chat('assistant', ai_text))


def main():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
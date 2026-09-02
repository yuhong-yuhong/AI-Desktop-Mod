"""AI Desktop Chat - minimal runnable example

This file launches a simple Tkinter chat window that talks to an AI backend via ai_client.
It uses config.py for settings. It's intended for quick testing in PyCharm.
"""
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import config
import ai_client


class ChatApp:
    def __init__(self, root):
        self.root = root
        root.title(config.WINDOW_TITLE)
        root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(root, state='disabled', wrap='word', font=(config.FONT_FAMILY, config.FONT_SIZE))
        self.chat_display.pack(fill='both', expand=True, padx=8, pady=8)

        # Entry + send
        frame = tk.Frame(root)
        frame.pack(fill='x', padx=8, pady=(0, 8))

        self.entry = tk.Entry(frame, font=(config.FONT_FAMILY, config.FONT_SIZE))
        self.entry.pack(side='left', fill='x', expand=True, padx=(0, 8))
        self.entry.bind('<Return>', lambda e: self.on_send())

        self.send_btn = tk.Button(frame, text='Send', command=self.on_send)
        self.send_btn.pack(side='right')

        # Conversation history for the AI client (list of messages)
        self.history = [
            {"role": "system", "content": config.SYSTEM_PROMPT}
        ]

    def append_chat(self, role, text):
        self.chat_display.configure(state='normal')
        if role == 'user':
            self.chat_display.insert('end', f"You: {text}\n")
        else:
            self.chat_display.insert('end', f"AI: {text}\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see('end')

    def on_send(self):
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.entry.delete(0, 'end')
        self.append_chat('user', user_text)
        self.history.append({"role": "user", "content": user_text})

        # Call AI in a background thread to avoid freezing the UI
        threading.Thread(target=self.call_ai, args=(user_text,), daemon=True).start()

    def call_ai(self, user_text):
        try:
            ai_text = ai_client.get_response(user_text, self.history)
            if ai_text is None:
                ai_text = "(没有可用的响应)"
        except Exception as e:
            ai_text = f"(调用AI时出错: {e})"
        # save assistant message into history
        self.history.append({"role": "assistant", "content": ai_text})
        # update UI in main thread
        self.root.after(0, lambda: self.append_chat('assistant', ai_text))


def main():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()

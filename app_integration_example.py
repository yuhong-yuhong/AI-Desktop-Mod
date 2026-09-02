"""
示例：在应用中如何初始化并调用模型。
"""
from ai_models import get_model


def main():
    model = get_model()

    # 简单同步调用
    try:
        resp = model.chat("你好，测试 AI 模型。请返回一条简短回答。")
        print("AI:", resp)
    except Exception as e:
        print("同步调用出错：", e)

    # 如果模型支持流式输出
    if hasattr(model, "chat_stream"):
        try:
            print("流式响应:")
            for chunk in model.chat_stream("请逐步解释什么是量子叠加（分块输出）"):
                print(chunk, end="", flush=True)
            print()
        except Exception as e:
            print("流式调用出错：", e)


if __name__ == "__main__":
    main()

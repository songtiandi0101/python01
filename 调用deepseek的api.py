import os
from openai import OpenAI

#密钥：sk-2c7a6ddd6c404fd0bf624328bb7bd13e

# 1. 初始化客户端
# 它会自动从环境变量 DEEPSEEK_API_KEY 中读取密钥
# base_url 指定了 DeepSeek 的 API 端点[reference:8]
client = OpenAI(
    #api_key=os.environ.get("DEEPSEEK_API_KEY"),
    api_key="sk-2c7a6ddd6c404fd0bf624328bb7bd13e",
    base_url="https://api.deepseek.com"
)
# 消费模型model="deepseek-v4-flash"
# 2. 创建聊天补全请求
# 调用对话API
try:
    response = client.chat.completions.create(
        model="deepseek-v4-flash",  # 指定模型，可选 deepseek-v4-flash / deepseek-v4-pro
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},  # 系统角色定义
            {"role": "user", "content": "100乘100等于多少"},  # 用户提问
        ],
        stream=False  # 非流式输出（一次性返回完整结果）
    )
    # 打印回复内容
    print("回复结果：", response.choices[0].message.content)
except Exception as e:
    print("调用失败：", str(e))

# 3. 打印模型的回复
print(response.choices[0].message.content)
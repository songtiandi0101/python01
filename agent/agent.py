"""
agent.py - 极简 AI Agent 原型（可直接运行）
说明：
- LLM 部分用一个非常简单的"规则回答器"模拟，实际接入 LLM 时替换 LLMInterface.generate(...)
- 包含组件：LLM 抽象、大脑(解析/决策)、规划器、工具注册器、内存、执行器
"""
from typing import Any, Dict, List, Callable
import time

# -----------------------------
# Memory（非常轻量）
# -----------------------------

class Memory:
    def __init__(self):
        self.short = {} # 当前会话上下文
        self.long = {} # 长期偏好/联系人等

    def get_short(self,k,default = None):
        return self.short.get(k,default)
    def set_short(self,k,v):
        self.short[k] = v

    def get_long(self,k,default = None):
        return self.long.get(k,default)
    def set_long(self,k,v):
        self.long[k] = v

# -----------------------------
# LLM 抽象（替换点）
# -----------------------------
class LLMInterface:
    def generate(self,prompt:str) -> str:
        """
        这里给出一个非常简单的规则式模拟回答器。
        真实使用时：替换为 OpenAI/其它模型的调用代码，返回 model 文本。
        """
        # 极简解析示例：识别是否需要判断"下雨"
        if "是否下雨" in prompt or "下雨" in prompt:
            return "请先查询天气；如果有雨，请生成提醒并发送给目标联系人。"
        if "生成提醒" in prompt:
            return "请提醒小王：明天北京有雨，请带伞。"
        return "我理解了。"

# -----------------------------
# 工具注册与模拟工具
# -----------------------------

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable[..., Any]] = {}
        #Dict：表明这是一个字典。
        #str（键）：字典的键是字符串，通常用来存工具的名字，比如"search"或"calculator"。
        #Callable[..., Any]（值）：字典的值是一个可调用对象（即函数或方法）。
        #...表示这个函数可以接收任意数量的参数（参数类型和个数不限）。
        #Any表示这个函数可以返回任意类型的值。

    def register(self, name: str, fn: Callable[..., Any]):
        self.tools[name] = fn

        #def register(...)：定义一个register（注册）的方法。这是一个约定俗成的名字，专门用来添加工具。
        #self：类的实例自己。用来操作该实例的属性（就是上一步定义的self.tools字典）。
        #name: str：要注册的工具名称（字符串）。比如 "get_weather"或"search"。Agent后续会通过这个名字来找工具。
        #fn: Callable[..., Any]：要注册的具体函数（可调用对象）。
        #Callable表示这是一个可以“加括号执行”的东西（比如普通函数或类方法）。
        #...表示这个函数可以接收任意参数。
        #self.tools[name] = fn：核心赋值语句。把传入的函数fn，放进self.tools这个字典里，并将它的键（key）设置为name。

    def call(self, name: str, *args, **kwargs):
        if name not in self.tools:
            raise ValueError(f"工具未注册: {name}")
        return self.tools[name](*args, **kwargs)

# 模拟工具：天气查询（真实情况会调用天气 API）
def mock_weather_api(city: str, date: str) -> Dict[str, Any]:
    # 简单规则：如果 city 包含 "北京" 且 date 包含 "明天"，返回下雨示例
    if "北京" in city and "明天" in date:
        return {"city": city, "date": date, "cond": "雨", "precip_mm": 5}
    return {"city": city, "date": date, "cond": "晴", "precip_mm": 0}

# 模拟工具：发送消息（真实情况会调用短信/邮件/企业微信等）
def mock_send_message(contact: str, message: str) -> bool:
    print(f"[发送消息] to={contact} message={message}")
    return True

# 模拟工具：简单搜索（示意）
def mock_search(query: str) -> str:
    return f"模拟搜索结果：关于 `{query}` 的信息摘要。"


# -----------------------------
# Planner / Executor
# -----------------------------
class SimplePlanner:
    def plan(self, goal: str) -> List[Dict[str, Any]]:
        """
        将目标拆解为步骤列表（非常简化的实现）
        每一步包含：action(工具名或内部动作)、params
        """
        steps = []
        # 例：若提示包含"天气"，生成两个步骤：查天气、判断并可能发提醒
        if "天气" in goal or "下雨" in goal:
            steps.append({"action": "query_weather", "params": {"city": "北京", "date": "明天"}})
            steps.append({"action": "decide_and_notify", "params": {"contact_name": "小王"}})
        else:
            steps.append({"action": "search", "params": {"query": goal}})
        return steps
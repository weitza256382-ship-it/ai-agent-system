# 多功能AI Agent助手

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Agent-Function%20Calling-red.svg" alt="Agent">
  <img src="https://img.shields.io/badge/ZhipuAI-GLM--4-orange.svg" alt="Zhipu AI">
</p>

基于智谱AI Function Calling的多功能智能助手,支持天气查询、计算、搜索、时间查询和待办管理等多种工具调用。

## ✨ 功能特点

- 🤖 智能工具调用 - AI自主决策使用哪个工具
- 🌤️ 天气查询
- 🧮 计算器功能
- 🔍 网络搜索
- ⏰ 时间查询
- 📝 待办事项管理
- 💬 多轮对话支持
- 🎯 上下文理解

## 🛠️ 技术栈

- **框架**: FastAPI
- **大模型**: 智谱AI GLM-4
- **核心技术**: Function Calling
- **对话管理**: 多轮对话历史

## 📦 安装使用

### 安装依赖
```bash
pip install -r requirements.txt
```

### 设置API密钥
```bash
set ZHIPU_API_KEY=your_api_key_here
```

### 运行
```bash
python agent_system.py
```

访问: http://localhost:8000/docs

## 🎮 使用示例

### 示例1: 天气查询
```json
{
  "message": "北京今天天气怎么样?"
}
```

**响应:**
```json
{
  "message": "北京今天天气晴朗,温度15度,空气质量良好!",
  "tool_calls": [
    {
      "tool": "get_weather",
      "args": {"city": "北京"},
      "result": "晴天,温度15°C,空气质量良好"
    }
  ]
}
```

### 示例2: 计算
```json
{
  "message": "帮我算一下 123 * 456"
}
```

### 示例3: 多轮对话
```json
// 第1轮
{"message": "添加待办:明天开会"}

// 第2轮
{"message": "再加一个:买菜"}

// 第3轮
{"message": "我有哪些待办?"}
```

## 🏗️ 核心架构

### Agent工作流程
```
用户输入
    ↓
AI分析(需要什么工具?)
    ↓
调用工具(执行具体功能)
    ↓
工具返回结果
    ↓
AI生成最终答案
    ↓
返回用户
```

### 可用工具

| 工具 | 功能 | 示例 |
|------|------|------|
| get_weather | 查询城市天气 | "北京天气怎么样?" |
| calculator | 数学计算 | "123 * 456 等于多少?" |
| search_web | 网络搜索 | "搜索最新AI新闻" |
| get_current_time | 获取时间 | "现在几点了?" |
| add_todo | 添加待办 | "添加待办:买菜" |
| get_todo_list | 查看待办 | "我的待办事项" |

## 💡 技术亮点

1. **Function Calling**: 让AI自主决策工具调用,无需人工判断
2. **多轮对话**: 支持上下文理解,对话更自然
3. **工具扩展**: 易于添加新工具,架构灵活
4. **智能决策**: AI根据用户意图选择最合适的工具

## 🔧 添加新工具
```python
# 1. 定义工具函数
def your_tool(param: str) -> str:
    """工具描述"""
    # 实现逻辑
    return result

# 2. 添加到工具列表
TOOLS.append({
    "type": "function",
    "function": {
        "name": "your_tool",
        "description": "工具描述",
        "parameters": {...}
    }
})

# 3. 注册到映射
TOOL_FUNCTIONS["your_tool"] = your_tool
```

## 📊 API端点

- `POST /chat` - 与Agent对话
- `GET /todos` - 获取待办列表
- `DELETE /history` - 清空对话历史
- `DELETE /todos` - 清空待办事项
- `GET /health` - 健康检查

## 🎯 应用场景

- 🏢 企业智能助手
- 📱 个人AI助理
- 🤝 客服机器人
- 📊 数据查询助手
- 🎓 教育辅导工具

## 👤 作者

- 你的名字
- GitHub: [@你的用户名](https://github.com/你的用户名)

## 📄 许可证

MIT License

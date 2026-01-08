# agent_system.py - 多功能AI Agent助手
# 使用智谱AI的Function Calling功能

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

# 智谱AI
try:
    from zhipuai import ZhipuAI
except ImportError:
    print("请安装: pip install zhipuai")

# ============================================================================
# FastAPI应用
# ============================================================================

app = FastAPI(
    title="多功能AI Agent助手",
    description="支持天气、计算、搜索、时间等多种功能的智能助手",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# 全局变量
# ============================================================================

zhipu_client = None
conversation_history = []  # 对话历史
todo_list = []  # 待办事项列表

# ============================================================================
# 数据模型
# ============================================================================

class ChatRequest(BaseModel):
    message: str
    clear_history: bool = False  # 是否清空历史

class ChatResponse(BaseModel):
    message: str
    tool_calls: List[Dict[str, Any]] = []  # 调用了哪些工具
    model: str

class TodoItem(BaseModel):
    id: int
    content: str
    created_at: str
    completed: bool = False

# ============================================================================
# 工具函数定义
# ============================================================================

def get_weather(city: str) -> str:
    """
    查询城市天气
    这是一个模拟函数,实际应该调用天气API
    """
    print(f"[工具调用] get_weather(city='{city}')")
    
    # 模拟天气数据
    weather_data = {
        "北京": "晴天,温度15°C,空气质量良好",
        "上海": "多云,温度18°C,有轻微雾霾",
        "深圳": "阴天,温度22°C,可能有小雨",
        "广州": "晴天,温度24°C,适合户外活动"
    }
    
    result = weather_data.get(city, f"{city}天气晴朗,温度20°C")
    print(f"[工具返回] {result}")
    
    return result

def calculator(expression: str) -> str:
    """
    计算数学表达式
    注意:实际使用时要做安全检查!
    """
    print(f"[工具调用] calculator(expression='{expression}')")
    
    try:
        # 简单的安全检查
        allowed_chars = "0123456789+-*/(). "
        if not all(c in allowed_chars for c in expression):
            return "错误:表达式包含非法字符"
        
        result = eval(expression)
        print(f"[工具返回] {result}")
        return f"计算结果: {result}"
    
    except Exception as e:
        error_msg = f"计算错误: {str(e)}"
        print(f"[工具返回] {error_msg}")
        return error_msg

def search_web(query: str) -> str:
    """
    搜索网络信息
    这是模拟函数,实际应该调用搜索API
    """
    print(f"[工具调用] search_web(query='{query}')")
    
    # 模拟搜索结果
    result = f"关于'{query}'的搜索结果:\n"
    result += "1. 最新资讯显示该话题热度很高\n"
    result += "2. 相关内容已被广泛讨论\n"
    result += "3. 建议查看官方网站获取更多信息"
    
    print(f"[工具返回] 搜索完成")
    return result

def get_current_time() -> str:
    """
    获取当前时间
    """
    print(f"[工具调用] get_current_time()")
    
    now = datetime.now()
    time_str = now.strftime("%Y年%m月%d日 %H:%M:%S")
    result = f"当前时间: {time_str}"
    
    print(f"[工具返回] {result}")
    return result

def add_todo(content: str) -> str:
    """
    添加待办事项
    """
    print(f"[工具调用] add_todo(content='{content}')")
    
    global todo_list
    
    todo = {
        "id": len(todo_list) + 1,
        "content": content,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed": False
    }
    
    todo_list.append(todo)
    
    result = f"已添加待办事项: {content}"
    print(f"[工具返回] {result}")
    
    return result

def get_todo_list() -> str:
    """
    获取待办事项列表
    """
    print(f"[工具调用] get_todo_list()")
    
    global todo_list
    
    if not todo_list:
        return "待办事项列表为空"
    
    result = "您的待办事项:\n"
    for todo in todo_list:
        status = "✓" if todo["completed"] else "○"
        result += f"{status} {todo['id']}. {todo['content']}\n"
    
    print(f"[工具返回] 返回{len(todo_list)}个待办事项")
    return result

# ============================================================================
# 工具配置 - 告诉AI有哪些工具可用
# ============================================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称,如:北京、上海"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式,支持加减乘除和括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式,如: 123 * 456"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "搜索网络信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前日期和时间",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_todo",
            "description": "添加待办事项",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "待办事项内容"
                    }
                },
                "required": ["content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_todo_list",
            "description": "查看待办事项列表",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

# 工具函数映射
TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "calculator": calculator,
    "search_web": search_web,
    "get_current_time": get_current_time,
    "add_todo": add_todo,
    "get_todo_list": get_todo_list
}

# ============================================================================
# 初始化
# ============================================================================

def init_zhipu():
    """初始化智谱AI"""
    global zhipu_client
    
    api_key = os.getenv("ZHIPU_API_KEY")
    if not api_key:
        print("⚠️  ZHIPU_API_KEY 未设置")
        return False
    
    try:
        zhipu_client = ZhipuAI(api_key=api_key)
        print("✅ 智谱AI初始化成功")
        return True
    except Exception as e:
        print(f"❌ 智谱AI初始化失败: {e}")
        return False

# ============================================================================
# Agent核心逻辑
# ============================================================================

def run_agent(user_message: str) -> tuple[str, List[Dict]]:
    """
    运行Agent,处理用户消息
    返回: (回答, 工具调用记录)
    """
    global zhipu_client, conversation_history
    
    if not zhipu_client:
        raise Exception("智谱AI未初始化")
    
    print(f"\n{'='*60}")
    print(f"👤 用户: {user_message}")
    print(f"{'='*60}")
    
    # 添加用户消息到历史
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    tool_calls_log = []  # 记录工具调用
    
    # 第一次调用:AI分析并决定是否使用工具
    print("[Agent] 分析用户需求...")
    
    response = zhipu_client.chat.completions.create(
        model="glm-4",
        messages=conversation_history,
        tools=TOOLS,  # ← 关键!告诉AI有哪些工具
        temperature=0.3
    )
    
    assistant_message = response.choices[0].message
    
    # 检查AI是否要调用工具
    if assistant_message.tool_calls:
        print(f"[Agent] AI决定调用 {len(assistant_message.tool_calls)} 个工具")
        
        # 添加AI的工具调用消息到历史
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                } for tc in assistant_message.tool_calls
            ]
        })
        
        # 执行每个工具调用
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"\n[Agent] 执行工具: {function_name}")
            print(f"[Agent] 参数: {function_args}")
            
            # 调用对应的函数
            if function_name in TOOL_FUNCTIONS:
                function_response = TOOL_FUNCTIONS[function_name](**function_args)
                
                # 记录工具调用
                tool_calls_log.append({
                    "tool": function_name,
                    "args": function_args,
                    "result": function_response
                })
                
                # 添加工具返回结果到历史
                conversation_history.append({
                    "role": "tool",
                    "content": function_response,
                    "tool_call_id": tool_call.id
                })
            else:
                print(f"⚠️  未找到工具: {function_name}")
        
        # 第二次调用:基于工具结果生成最终答案
        print("\n[Agent] 基于工具结果生成最终答案...")
        
        final_response = zhipu_client.chat.completions.create(
            model="glm-4",
            messages=conversation_history,
            temperature=0.3
        )
        
        final_answer = final_response.choices[0].message.content
        
    else:
        # AI不需要工具,直接回答
        print("[Agent] AI直接回答,无需调用工具")
        final_answer = assistant_message.content
    
    # 添加最终答案到历史
    conversation_history.append({
        "role": "assistant",
        "content": final_answer
    })
    
    print(f"\n🤖 Assistant: {final_answer}")
    print(f"{'='*60}\n")
    
    return final_answer, tool_calls_log

# ============================================================================
# API端点
# ============================================================================

@app.on_event("startup")
async def startup_event():
    init_zhipu()

@app.get("/")
def read_root():
    return {
        "message": "🤖 多功能AI Agent助手",
        "version": "1.0",
        "available_tools": [tool["function"]["name"] for tool in TOOLS],
        "features": [
            "✅ 智能工具调用",
            "✅ 多轮对话",
            "✅ 天气查询",
            "✅ 计算器",
            "✅ 网络搜索",
            "✅ 时间查询",
            "✅ 待办管理"
        ]
    }

@app.get("/health")
def health_check():
    zhipu_key = os.getenv("ZHIPU_API_KEY")
    
    return {
        "status": "healthy",
        "zhipu_configured": bool(zhipu_key),
        "zhipu_client_ready": zhipu_client is not None,
        "available_tools": len(TOOLS),
        "conversation_turns": len(conversation_history),
        "todo_count": len(todo_list)
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    与Agent对话
    """
    global conversation_history
    
    if not zhipu_client:
        raise HTTPException(status_code=500, detail="智谱AI未配置")
    
    # 是否清空历史
    if request.clear_history:
        conversation_history = []
        print("[系统] 对话历史已清空")
    
    try:
        answer, tool_calls = run_agent(request.message)
        
        return ChatResponse(
            message=answer,
            tool_calls=tool_calls,
            model="GLM-4"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

@app.get("/todos", response_model=List[TodoItem])
def get_todos():
    """获取所有待办事项"""
    return [
        TodoItem(
            id=todo["id"],
            content=todo["content"],
            created_at=todo["created_at"],
            completed=todo["completed"]
        )
        for todo in todo_list
    ]

@app.delete("/history")
def clear_history():
    """清空对话历史"""
    global conversation_history
    count = len(conversation_history)
    conversation_history = []
    
    return {
        "status": "success",
        "message": f"已清空 {count} 条对话记录"
    }

@app.delete("/todos")
def clear_todos():
    """清空待办事项"""
    global todo_list
    count = len(todo_list)
    todo_list = []
    
    return {
        "status": "success",
        "message": f"已清空 {count} 个待办事项"
    }

# ============================================================================
# 启动
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("🤖 多功能AI Agent助手系统启动")
    print("="*70)
    print("🛠️  可用工具:")
    for i, tool in enumerate(TOOLS, 1):
        print(f"   {i}. {tool['function']['name']}: {tool['function']['description']}")
    print("="*70)
    print("💡 示例对话:")
    print("   - '北京今天天气怎么样?'")
    print("   - '帮我算一下 123 * 456'")
    print("   - '搜索最新的AI新闻'")
    print("   - '现在几点了?'")
    print("   - '添加待办:买菜'")
    print("   - '查看我的待办事项'")
    print("="*70)
    print("⚙️  配置检查:")
    
    zhipu_key = os.getenv("ZHIPU_API_KEY")
    if zhipu_key:
        print(f"   ✅ ZHIPU_API_KEY: {zhipu_key[:20]}...")
    else:
        print("   ⚠️  ZHIPU_API_KEY: 未设置")
    
    print("="*70)
    print("📖 API文档: http://localhost:8000/docs")
    print("="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
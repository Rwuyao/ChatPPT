import os
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

def get_deepseek_response(prompt, history=None):
    """
    调用DeepSeek大模型获取回复
    
    Args:
        prompt: 用户输入的问题
        history: 聊天历史，可选
    
    Returns:
        str: 大模型的回复或错误提示
    """
    # 从环境变量获取API token
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    
    if not api_key:
        return "请配置DEEPSEEK_API_KEY环境变量"
    
    try:
        # 加载系统提示词
        system_prompt_path = os.path.join(os.path.dirname(__file__), 'prompts', 'formatter.txt')
        if os.path.exists(system_prompt_path):
            with open(system_prompt_path, 'r', encoding='utf-8') as f:
                system_prompt = f.read().strip()
        else:
            system_prompt = "你是一位专业的IT解决方案顾问，擅长为用户设计全面、实用的IT方案。"
        
        # 创建ChatOpenAI实例（适配DeepSeek API）
        llm = ChatOpenAI(
            model="deepseek-chat",
            base_url="https://api.deepseek.com/v1",
            api_key=api_key,
            temperature=0.7,
            max_tokens=512
        )
        
        # 构建提示词模板（使用LCEL语法）
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("user", "{input}")
        ])
        
        # 构建消息历史，限制历史记录长度以避免过长
        messages_history = []
        if history:
            # 只保留最近的5轮对话，避免历史记录过长
            recent_history = history[-10:] if len(history) > 10 else history
            
            for msg in recent_history:
                if isinstance(msg, dict) and "role" in msg and "content" in msg:
                    if msg["role"] == "user":
                        messages_history.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        messages_history.append(AIMessage(content=msg["content"]))
                elif isinstance(msg, list) and len(msg) == 2:
                    # 处理列表格式的历史消息
                    if msg[0]:
                        messages_history.append(HumanMessage(content=str(msg[0])))
                    if msg[1]:
                        messages_history.append(AIMessage(content=str(msg[1])))
        
        # 构建LCEL链
        chain = prompt_template | llm | StrOutputParser()
        
        # 调用大模型
        response = chain.invoke({
            "input": prompt,
            "history": messages_history
        })
        
        return response
    
    except Exception as e:
        return f"处理回复时出错: {str(e)}"

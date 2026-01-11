import gradio as gr
import os
from deepseek_client import get_deepseek_response
from ppt_generator import generate_ppt

def chat_function(message, history):
    """聊天函数，处理文本消息"""
    # 处理文本消息 - 使用DeepSeek大模型回复
    user_message = {"role": "user", "content": message}
    # 调用DeepSeek大模型获取回复
    response = get_deepseek_response(message, history)
    assistant_message = {"role": "assistant", "content": response}
    
    # 添加到聊天历史
    history.append(user_message)
    history.append(assistant_message)
    
    # 清除输入组件的值
    return "", history

def generate_ppt_function(history):
    """生成PPT文件的函数"""
    if not history:
        print("消息返回为空")
        return None
    
    # 获取最后一条消息的内容
    last_message = history[-1]
    if isinstance(last_message, list) and len(last_message) == 2:
        # Gradio的聊天历史格式：[[user_message, assistant_message], ...]
        content = last_message[1]  # 取助手的回复作为PPT内容
    elif isinstance(last_message, dict) and "content" in last_message:
        # 字典格式的消息
        content = last_message["content"]
    else:
        content = str(last_message)
    print(content)
    # 生成PPT文件
    ppt_path = generate_ppt(content)
    return ppt_path

# 创建聊天界面
with gr.Blocks(title="智能聊天窗口") as demo:
    gr.Markdown("# 智能聊天窗口")
    gr.Markdown("支持文本消息和PPT生成功能")
    
    # 聊天历史组件
    chatbot = gr.Chatbot(
        label="聊天记录",
        height=400
    )
    
    # 消息输入组件
    msg = gr.Textbox(
        label="输入消息",
        placeholder="请输入文本消息..."
    )
    
    # PPT文件输出组件
    ppt_output = gr.File(
        label="生成的PPT文件",
        file_types=[".pptx"],
        height=36
    )
    
    # 所有操作按钮放在同一行
    with gr.Row():
        # 清除按钮
        clear = gr.ClearButton(
            components=[msg, chatbot, ppt_output]
        )
        
        # 提交按钮
        submit = gr.Button("发送")
        
        # PPT生成按钮
        generate_ppt_btn = gr.Button("生成PPT")
    
    # 事件处理
    submit.click(
        fn=chat_function,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    )
    
    msg.submit(
        fn=chat_function,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    )
    
    # PPT生成事件
    generate_ppt_btn.click(
        fn=generate_ppt_function,
        inputs=[chatbot],
        outputs=[ppt_output]
    )

if __name__ == "__main__":
    demo.launch(debug=True)
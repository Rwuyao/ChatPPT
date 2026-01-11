import os
from pptx import Presentation
from pptx.util import Inches

def generate_ppt(content, output_dir="output"):
    """
    将文本内容生成PPT文件
    
    Args:
        content: 要转换为PPT的文本内容
        output_dir: PPT文件的输出目录
    
    Returns:
        str: 生成的PPT文件路径
    """
    try:
        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 创建PPT演示文稿
        prs = Presentation()
        
        # 设置幻灯片大小为标准A4
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)
        
        # 处理不同类型的内容输入
        if isinstance(content, str):
            # 字符串类型
            content_text = content
        elif isinstance(content, list):
            # 列表类型，尝试提取文本内容
            content_text = ""
            for item in content:
                if isinstance(item, dict) and "text" in item:
                    content_text += item["text"] + "\n"
                else:
                    content_text += str(item) + "\n"
        elif isinstance(content, dict):
            # 字典类型，尝试提取文本内容
            if "text" in content:
                content_text = content["text"]
            else:
                content_text = str(content)
        else:
            # 其他类型，转换为字符串
            content_text = str(content)
        
        # 处理内容，按换行符分割为多个部分
        content_parts = content_text.split('\n')
        
        # 创建标题幻灯片
        title_slide_layout = prs.slide_layouts[0]  # 标题幻灯片布局
        slide = prs.slides.add_slide(title_slide_layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        
        # 设置标题和副标题
        if content_parts:
            title.text = content_parts[0]
            subtitle.text = "基于对话内容生成的PPT"
        else:
            title.text = "对话内容"
            subtitle.text = "基于对话内容生成的PPT"
        
        # 创建内容幻灯片
        content_slide_layout = prs.slide_layouts[1]  # 标题和内容布局
        
        # 按内容分段创建幻灯片
        current_content = []
        for part in content_parts[1:]:  # 跳过第一个部分，已经作为标题
            if part.strip():
                current_content.append(part)
                # 每3-4行创建一个新幻灯片
                if len(current_content) >= 3:
                    slide = prs.slides.add_slide(content_slide_layout)
                    slide.shapes.title.text = "内容"
                    content_placeholder = slide.placeholders[1]
                    content_placeholder.text = '\n'.join(current_content)
                    current_content = []
        
        # 处理剩余内容
        if current_content:
            slide = prs.slides.add_slide(content_slide_layout)
            slide.shapes.title.text = "内容"
            content_placeholder = slide.placeholders[1]
            content_placeholder.text = '\n'.join(current_content)
        
        # 生成唯一的文件名
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ppt_filename = f"conversation_{timestamp}.pptx"
        ppt_path = os.path.join(output_dir, ppt_filename)
        
        # 保存PPT文件
        prs.save(ppt_path)
        
        return ppt_path
    
    except Exception as e:
        print(f"生成PPT时出错: {str(e)}")
        return None

if __name__ == "__main__":
    # 测试PPT生成功能
    test_content = "IT解决方案设计\n\n1. 系统架构设计\n- 前端：React\n- 后端：Python FastAPI\n- 数据库：PostgreSQL\n\n2. 技术栈选择\n- 前端框架：React 18\n- 后端框架：FastAPI\n- 数据库：PostgreSQL 15\n- 缓存：Redis\n- 部署：Docker + Kubernetes"
    
    ppt_path = generate_ppt(test_content)
    if ppt_path:
        print(f"PPT生成成功：{ppt_path}")
    else:
        print("PPT生成失败")

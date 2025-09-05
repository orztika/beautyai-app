import streamlit as st
import openai
import os
from dotenv import load_dotenv
import time

# 加载环境变量
load_dotenv()

# 配置页面
st.set_page_config(
    page_title="BeautyAI - 智能文案生成器",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF6B6B;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #4ECDC4;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .style-badge {
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        margin-bottom: 1rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# 初始化OpenAI客户端
def init_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # 尝试从Streamlit secrets获取
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except:
            return None
    
    openai.api_key = api_key
    return api_key

# 生成文案的函数
def generate_content(topic, style):
    """根据主题和风格生成文案"""
    
    style_prompts = {
        "专业": "请以专业、权威、严谨的语调撰写，使用行业术语，体现专业性和可信度。",
        "亲切": "请以温暖、友好、贴近生活的语调撰写，使用日常用语，让人感到亲近和舒适。",
        "时尚": "请以潮流、前卫、有活力的语调撰写，使用时尚词汇，体现年轻化和创新感。"
    }
    
    prompt = f"""
    请根据以下主题生成3条不同的文案，每条文案都要符合{style}风格的特征。
    
    主题：{topic}
    
    风格要求：{style_prompts[style]}
    
    请生成3条文案，每条文案控制在50-100字之间，要求：
    1. 内容要有创意和吸引力
    2. 符合指定的风格特征
    3. 每条文案都要有所不同
    4. 适合用于营销推广
    
    请按以下格式输出：
    文案1：[内容]
    文案2：[内容]
    文案3：[内容]
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是一个专业的文案创作专家，擅长根据不同风格和主题创作吸引人的营销文案。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"生成文案时出现错误：{str(e)}"

# 解析生成的文案
def parse_generated_content(content):
    """解析生成的文案内容"""
    lines = content.split('\n')
    copywriting_list = []
    
    for line in lines:
        if line.strip() and ('文案' in line or '：' in line):
            # 提取冒号后的内容
            if '：' in line:
                copy_text = line.split('：', 1)[1].strip()
                if copy_text:
                    copywriting_list.append(copy_text)
    
    # 如果解析失败，返回原始内容的前3行
    if not copywriting_list:
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        copywriting_list = lines[:3]
    
    return copywriting_list[:3]  # 确保只返回3条

# 主界面
def main():
    # 标题
    st.markdown('<h1 class="main-header">✨ BeautyAI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">智能文案生成器 - 让创意触手可及</p>', unsafe_allow_html=True)
    
    # 检查API密钥
    api_key = init_openai()
    if not api_key:
        st.error("⚠️ 请配置OpenAI API密钥")
        st.info("请在环境变量中设置 OPENAI_API_KEY 或在Streamlit Cloud的Secrets中配置")
        return
    
    # 创建两列布局
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 输入内容")
        
        # 文本输入框
        topic = st.text_area(
            "请输入文案主题内容：",
            placeholder="例如：新款智能手表，具有健康监测功能...",
            height=120,
            help="描述你想要推广的产品、服务或活动"
        )
        
        # 风格选择
        style = st.selectbox(
            "选择文案风格：",
            ["专业", "亲切", "时尚"],
            help="不同风格会影响文案的语调和表达方式"
        )
        
        # 风格说明
        style_descriptions = {
            "专业": "🏢 权威严谨，适合B2B或高端产品",
            "亲切": "🏠 温暖友好，适合生活类产品",
            "时尚": "🌟 潮流前卫，适合年轻化产品"
        }
        
        st.info(style_descriptions[style])
        
        # 生成按钮
        generate_btn = st.button("🚀 生成文案", type="primary")
    
    with col2:
        st.markdown("### 📋 生成结果")
        
        if generate_btn:
            if not topic.strip():
                st.warning("请先输入文案主题内容")
            else:
                # 显示加载状态
                with st.spinner("AI正在创作中，请稍候..."):
                    # 生成文案
                    generated_content = generate_content(topic, style)
                    
                    # 解析文案
                    copywriting_list = parse_generated_content(generated_content)
                    
                    # 显示结果
                    if copywriting_list:
                        st.success(f"✅ 成功生成{len(copywriting_list)}条{style}风格文案")
                        
                        for i, copy_text in enumerate(copywriting_list, 1):
                            st.markdown(f"""
                            <div class="result-card">
                                <div class="style-badge">{style}风格 - 文案{i}</div>
                                <div style="font-size: 1.1rem; line-height: 1.6;">{copy_text}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error("生成文案失败，请重试")
        else:
            st.info("👆 请在左侧输入主题内容并选择风格，然后点击生成按钮")
    
    # 底部信息
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; margin-top: 2rem;'>">
        "💡 Powered by OpenAI GPT-4 | Built with Streamlit | Made with ❤️"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
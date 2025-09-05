import streamlit as st
import openai
import os

# 配置页面
st.set_page_config(
    page_title="BeautyAI - 智能文案生成器",
    page_icon="✨"
)

# 初始化OpenAI客户端
def init_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except:
            return None
    
    openai.api_key = api_key
    return api_key

# 生成文案的函数
def generate_content(topic, style):
    style_prompts = {
        "专业": "请以专业、权威、严谨的语调撰写",
        "亲切": "请以温暖、友好、贴近生活的语调撰写",
        "时尚": "请以潮流、前卫、有活力的语调撰写"
    }
    
    prompt = f"根据主题'{topic}'生成3条{style}风格的文案，每条50-100字。{style_prompts[style]}。格式：文案1：[内容]\n文案2：[内容]\n文案3：[内容]"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是专业文案创作专家"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"生成错误：{str(e)}"

# 解析生成的文案
def parse_generated_content(content):
    lines = content.split('\n')
    copywriting_list = []
    
    for line in lines:
        if line.strip() and '：' in line:
            copy_text = line.split('：', 1)[1].strip()
            if copy_text:
                copywriting_list.append(copy_text)
    
    if not copywriting_list:
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        copywriting_list = lines[:3]
    
    return copywriting_list[:3]

# 主界面
def main():
    st.title("✨ BeautyAI 智能文案生成器")
    
    # 检查API密钥
    api_key = init_openai()
    if not api_key:
        st.error("请配置OpenAI API密钥")
        return
    
    # 输入区域
    topic = st.text_area("请输入文案主题内容：", height=100)
    style = st.selectbox("选择文案风格：", ["专业", "亲切", "时尚"])
    
    if st.button("生成文案"):
        if not topic.strip():
            st.warning("请先输入文案主题内容")
        else:
            with st.spinner("生成中..."):
                generated_content = generate_content(topic, style)
                copywriting_list = parse_generated_content(generated_content)
                
                if copywriting_list:
                    st.success(f"成功生成{len(copywriting_list)}条{style}风格文案")
                    for i, copy_text in enumerate(copywriting_list, 1):
                        st.write(f"**文案{i}：**{copy_text}")
                else:
                    st.error("生成失败，请重试")

if __name__ == "__main__":
    main()
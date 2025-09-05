# BeautyAI - 智能文案生成器

一个基于Streamlit和OpenAI GPT-4的智能文案生成网页应用。

## 功能特性

- 📝 文本输入框：输入文案主题内容
- 🎨 风格选择：专业、亲切、时尚三种文案风格
- 🤖 AI生成：基于OpenAI GPT-4模型
- 📋 多样输出：一次生成3条不同风格的文案

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入你的OpenAI API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```
OPENAI_API_KEY=your_actual_api_key_here
```

### 3. 运行应用

```bash
streamlit run app.py
```

## 部署

本项目已配置Vercel部署，推送到GitHub后可直接部署。

## 技术栈

- Frontend: Streamlit
- AI Model: OpenAI GPT-4
- Deployment: Vercel
- Language: Python
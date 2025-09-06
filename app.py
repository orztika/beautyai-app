from flask import Flask, request, jsonify, render_template_string
import openai
import os

app = Flask(__name__)

# 初始化OpenAI客户端
client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# HTML模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI文案生成工具</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
        textarea { width: 100%; height: 100px; margin: 10px 0; padding: 10px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 15px; background: white; border-radius: 5px; }
        .loading { display: none; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 AI文案生成工具</h1>
        <form id="generateForm">
            <label>输入内容描述：</label>
            <textarea id="content" placeholder="请输入您想要生成文案的内容描述..."></textarea>
            
            <label>选择风格：</label>
            <select id="style">
                <option value="专业">专业</option>
                <option value="活泼">活泼</option>
                <option value="温馨">温馨</option>
                <option value="幽默">幽默</option>
            </select>
            
            <br><br>
            <button type="submit">生成文案</button>
        </form>
        
        <div class="loading" id="loading">正在生成文案，请稍候...</div>
        <div id="result"></div>
    </div>
    
    <script>
        document.getElementById('generateForm').onsubmit = async function(e) {
            e.preventDefault();
            
            const content = document.getElementById('content').value;
            const style = document.getElementById('style').value;
            
            if (!content.trim()) {
                alert('请输入内容描述');
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').innerHTML = '';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content, style })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    let html = '<div class="result"><h3>生成的文案：</h3>';
                    data.copywriting.forEach((item, index) => {
                        html += `<p><strong>${index + 1}. ${item.title}</strong><br>${item.content}</p>`;
                    });
                    html += '</div>';
                    document.getElementById('result').innerHTML = html;
                } else {
                    document.getElementById('result').innerHTML = '<div class="result">生成失败：' + data.error + '</div>';
                }
            } catch (error) {
                document.getElementById('result').innerHTML = '<div class="result">请求失败，请重试</div>';
            }
            
            document.getElementById('loading').style.display = 'none';
        };
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate_copywriting():
    try:
        data = request.get_json()
        content = data.get('content', '')
        style = data.get('style', '专业')
        
        if not content:
            return jsonify({'success': False, 'error': '内容不能为空'})
        
        # 调用OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"你是一个专业的文案创作助手。请根据用户提供的内容描述，生成3条{style}风格的文案。每条文案包含标题和正文。请以JSON格式返回，格式为：[{{\"title\": \"标题\", \"content\": \"正文内容\"}}]"},
                {"role": "user", "content": content}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        # 解析响应
        result_text = response.choices[0].message.content
        
        # 尝试解析JSON
        try:
            import json
            copywriting = json.loads(result_text)
        except:
            # 如果解析失败，创建简单格式
            copywriting = [
                {"title": f"{style}文案1", "content": result_text[:200]},
                {"title": f"{style}文案2", "content": result_text[200:400] if len(result_text) > 200 else result_text},
                {"title": f"{style}文案3", "content": result_text[400:] if len(result_text) > 400 else result_text}
            ]
        
        return jsonify({'success': True, 'copywriting': copywriting})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Vercel需要的应用实例
app = app

if __name__ == '__main__':
    app.run(debug=True)
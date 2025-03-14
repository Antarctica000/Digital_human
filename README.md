---
title: 接口文档
time: 2025-3-6
---

# 接口文档

## 1. web端使用说明

### 1.1 数字人朗读语音视频

`pip install openai`
`pip install python-multipart`

项目新增windows对生成离线视频的支持(linux macOS不支持)


### 1.2 数字人实时对话网页

将`web_demo/static`内的所有内容复制到项目中使用部署。

## 2. 小程序端使用说明































































好的，让我详细说明一下你该怎么做。

### 目标：将数字人朗读功能集成到一个课本朗读网站

假设你已经有了一个数字人朗读的开源项目，通过 `python app.py` 命令来启动它，并通过浏览器访问本地网页，能够看到数字人在朗读。

### 步骤概述：

1. **理解项目结构**：你要知道开源项目中，如何传入音频和视频数据，并且如何通过网页呈现数字人的朗读功能。
2. **搭建网站的前端**：为课本朗读创建一个网页前端，用户可以选择课本内容，传入音频，数字人就会开始朗读。
3. **连接后端（数字人功能）**：把这个数字人朗读功能集成到后端，能够从前端接收数据，调用数字人功能，并返回视频和音频给前端。
4. **使用 Postman 调试 API**：通过 Postman 来测试后端接口，确保数据能够正确传输和处理。

------

### 1. 理解开源项目的基本工作原理

你说在命令行运行 `python app.py` 命令，说明这个数字人项目应该是基于 Flask 或类似的框架来实现的。这意味着你通过访问本地的网页接口，传入音频和视频数据，它会启动数字人并进行朗读。

你需要弄清楚这个 `app.py` 文件中的关键步骤：

- **音频/视频数据传输**：了解 `app.py` 中是如何接收音频和视频数据的，通常是通过 HTTP 请求。
- **数字人模型运行**：`app.py` 会加载数字人模型，然后把传入的音频和视频数据传给模型，生成数字人朗读的效果。
- **网页显示**：`app.py` 可能通过 Flask 或其他框架提供一个网页服务，返回视频数据或动态展示数字人模型的状态。

### 2. 搭建课本朗读的前端网页

接下来，你需要做的是创建一个前端网页，用户可以在网页上浏览课本内容并启动朗读。可以使用 HTML、CSS、JavaScript 来搭建前端页面。

- **展示课本内容**：你可以用 `<textarea>` 或 `<div>` 来展示课本内容。
- **播放数字人朗读**：通过点击按钮触发朗读，后台会处理音频、视频数据并返回。你可以通过 `fetch` 或 `axios` 这样的工具将数据发送给后端。

**前端页面示例**：

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>课本朗读</title>
  <style>
    body { font-family: Arial, sans-serif; }
    .text { margin: 20px; }
    .button { padding: 10px 20px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
    .button:hover { background-color: #45a049; }
  </style>
</head>
<body>
  <div class="text">
    <h2>课本内容</h2>
    <div id="text-content">
      <p>这里是课本的内容。点击下面的按钮开始朗读。</p>
    </div>
  </div>
  <button class="button" id="start-reading">开始朗读</button>

  <script>
    document.getElementById('start-reading').onclick = function() {
      fetch('http://localhost:5000/start_reading', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          text: document.getElementById('text-content').innerText
        })
      })
      .then(response => response.json())
      .then(data => {
        // 这里处理返回的数据，比如播放音频、显示数字人视频
        console.log(data);
      })
      .catch(error => console.error('Error:', error));
    };
  </script>
</body>
</html>
```

### 3. 后端（数字人朗读功能）

你需要将开源项目中的 `app.py` 后端功能集成到这个课本朗读网站的后端。通常情况下，`app.py` 是通过 Flask 或类似的框架来处理 HTTP 请求的。你需要修改 `app.py`，使其能够接收前端发送的文本数据，然后调用数字人模型进行朗读。

**后端 Python 代码示例（Flask）**：

```python
from flask import Flask, request, jsonify
import your_digitalk_person_module  # 引入你的数字人模块

app = Flask(__name__)

@app.route('/start_reading', methods=['POST'])
def start_reading():
    data = request.get_json()  # 获取前端传来的数据
    text = data.get('text')  # 取出文本内容

    # 调用数字人模型进行朗读
    # 假设你有一个函数可以处理朗读
    video_output, audio_output = your_digitalk_person_module.generate_speech(text)

    # 返回音视频数据
    return jsonify({
        'video_url': video_output,  # 返回生成的视频地址
        'audio_url': audio_output   # 返回生成的音频地址
    })

if __name__ == '__main__':
    app.run(debug=True)
```

### 4. 测试 API 接口（使用 Postman）

你可以使用 **Postman** 来调试你自己开发的 API。具体的做法是：

- 打开 Postman，选择 `POST` 请求。
- 输入你的 API 地址：`http://localhost:5000/start_reading`。
- 在请求体中，选择 `raw`，并选择 `JSON` 格式，传入课本文本内容：

```json
{
  "text": "这是课本内容"
}
```

- 点击发送请求，你应该能收到包含音频和视频链接的响应。

### 总结：

1. 创建一个前端网页，显示课本内容并允许用户点击按钮启动朗读。
2. 修改后端代码（如 `app.py`），接收前端文本数据，并调用数字人模型生成朗读效果。
3. 使用 Postman 调试 API，确保前端和后端的数据流通畅。

这样，用户在浏览网页时就可以看到数字人在朗读课本内容。
import json
import requests
import asyncio  # 支持异步操作适用于处理流式数据
import re  # 正则表达式处理
import base64  # 用于音频文件的解码编码
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

# 初始化OpenAI客户端
client = OpenAI(
    api_key="sk-r2ujnbuDgRbnp3gTndbNkZyppryh9f9Q2VGNJyU7v4crH8Di",  # API Key
    base_url="https://api.lkeap.cloud.tencent.com/v1",  # 正确的API地址
)

app = FastAPI()  # 创建一个FastAPI应用实例

# 挂载静态文件
app.mount("/static", StaticFiles(directory="web_demo/static"), name="static")

# CORS 配置 (跨域访问啊可恶搞半天)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或者指定允许的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_audio(text_cache, voice_speed, voice_id):  # 文本转语音
    # 读取一个语音文件模拟语音合成的结果
    # 将test.wav换成用户提供的文字转语音
    # 必须是单通道16K Hz的wav！
    with open("web_demo/static/common/response.wav", "rb") as audio_file:
        audio_value = audio_file.read()
    base64_string = base64.b64encode(audio_value).decode('utf-8')
    return base64_string


async def llm_answer(prompt):
    # 调用 DeepSeek API 来获取智能大模型的回答
    # 通过 messages 数组实现上下文管理
    messages = [{'role': 'user', 'content': prompt}]

    # 获取完整回答
    completion = client.chat.completions.create(
        model="deepseek-r1",  # 替换为你想使用的模型名称
        messages=messages
    )
    # 提取并返回 DeepSeek 模型生成的回答
    answer = completion.choices[0].message.content
    return answer


def split_sentence(sentence, min_length=10):
    # 定义包括小括号在内的主要标点符号
    punctuations = r'[。？！；…，、()（）]'
    # 使用正则表达式切分句子，保留标点符号
    parts = re.split(f'({punctuations})', sentence)
    parts = [p for p in parts if p]  # 移除空字符串
    sentences = []
    current = ''
    for part in parts:
        if current:
            # 如果当前片段加上新片段长度超过最小长度，则将当前片段添加到结果中
            if len(current) + len(part) >= min_length:
                sentences.append(current + part)
                current = ''
            else:
                current += part
        else:
            current = part
    # 将剩余的片段添加到结果中
    if len(current) >= 2:
        sentences.append(current)
    return sentences


async def gen_stream(prompt, asr=False, voice_speed=None, voice_id=None):
    # print("XXXXXXXXX", voice_speed, voice_id)
    if asr:
        chunk = {
            "prompt": prompt
        }
        yield f"{json.dumps(chunk)}\n"  # 使用换行符分隔 JSON 块

    text_cache = llm_answer(prompt)
    sentences = split_sentence(text_cache)

    for index_, sub_text in enumerate(sentences):
        base64_string = get_audio(sub_text, voice_speed, voice_id)
        # 生成 JSON 格式的数据块
        chunk = {
            "text": sub_text,
            "audio": base64_string,
            "endpoint": index_ == len(sentences)-1
        }
        yield f"{json.dumps(chunk)}\n"  # 使用换行符分隔 JSON 块
        await asyncio.sleep(0.2)  # 模拟异步延迟

# 处理用户输入的文本并返回语音流


@app.post("/generate_speech")
async def generate_speech(request: Request):
    try:
        # 获取前端传过来的用户输入
        body = await request.json()
        prompt = body.get("prompt")  # 获取文本输入
        voice_speed = body.get("voice_speed")  # 获取语速
        voice_id = body.get("voice_id")  # 获取语音ID（可以根据需要使用）

        if not prompt:
            raise HTTPException(status_code=400, detail="Text is required")

        # 调用 TTS 流式响应生成语音
        return StreamingResponse(gen_stream(prompt, voice_speed=voice_speed, voice_id=voice_id), media_type="application/json")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 处理 ASR 和 TTS 的端点


@app.post("/process_audio")
async def process_audio(file: UploadFile = File(...)):
    # 模仿调用 ASR API 获取文本
    text = "语音已收到，这里只是模仿，真正对话需要您自己设置ASR服务。"
    # 调用 TTS 生成流式响应
    return StreamingResponse(gen_stream(text, asr=True), media_type="application/json")


async def call_asr_api(audio_data):
    # 调用ASR完成语音识别
    answer = "语音已收到，这里只是模仿，真正对话需要您自己设置ASR服务。"
    return answer


@app.post("/eb_stream")    # 前端调用的path
async def eb_stream(request: Request):
    try:
        body = await request.json()
        input_mode = body.get("input_mode")
        voice_speed = body.get("voice_speed")
        voice_id = body.get("voice_id")

        if input_mode == "audio":
            base64_audio = body.get("audio")
            # 解码 Base64 音频数据
            audio_data = base64.b64decode(base64_audio)
            # 这里可以添加对音频数据的处理逻辑
            prompt = await call_asr_api(audio_data)  # 假设 call_asr_api 可以处理音频数据
            return StreamingResponse(gen_stream(prompt, asr=True, voice_speed=voice_speed, voice_id=voice_id), media_type="application/json")
        elif input_mode == "text":
            prompt = body.get("prompt")
            return StreamingResponse(gen_stream(prompt, asr=False, voice_speed=voice_speed, voice_id=voice_id), media_type="application/json")
        else:
            raise HTTPException(status_code=400, detail="Invalid input mode")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 启动Uvicorn服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)

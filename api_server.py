from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
import subprocess
import os

app = FastAPI()


@app.post("/generate-video/")
async def generate_video(audio: UploadFile, asset_path: str = Form("video_data/000002/assets")):
    # 保存上传的音频
    audio_path = f"video_data/{audio.filename}"
    with open(audio_path, "wb") as f:
        f.write(await audio.read())

    # 调用speak_change.py处理音频格式
    subprocess.run(["python", "speak_change.py", audio_path], check=True)

    # 运行demo_mini.py脚本生成视频
    output_video = "1.mp4"
    # 若一切正常 将下面两行代码去除注释 执行真正的数字人语音视频生成逻辑
    # command = ["python", "demo_mini.py", asset_path, audio_path, output_video]
    # subprocess.run(command, check=True)

    # 返回生成的视频数据
    return FileResponse(output_video, media_type="video/mp4", filename=output_video)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

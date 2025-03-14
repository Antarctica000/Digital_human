from pydub import AudioSegment


def convert_audio(input_file, output_file):
    try:
        # 载入音频文件
        audio = AudioSegment.from_file(input_file)

        # 将音频转换为单通道 (Mono)
        audio = audio.set_channels(1)

        # 设置采样率为 16K Hz
        audio = audio.set_frame_rate(16000)

        # 转换为 WAV 格式
        audio.export(output_file, format="wav")
        print(f"转换完成，保存为: {output_file}")
    except Exception as e:
        print(f"音频转换失败: {e}")

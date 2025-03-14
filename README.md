---
title: 接口文档
time: 2025-3-6
---

# 接口文档

### 1.1 本地部署

#### 平台支持

- **windows**: 支持视频数据处理、离线视频合成、网页服务器。
- **linux&macOS**：支持视频数据处理、搭建网页服务器，不支持离线视频合成。
- **网页&小程序**：支持客户端直接打开。（我没懂小程序什么叫客户端直接打开...直接打开网页么？）
- **App**：webview方式调用网页或重构原生应用。

#### 部署说明

```shell
conda create -n dh_live python=3.12
conda activate dh_live
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

*项目已经增加了对cpu的支持，轻量快速

```shell
python app.py
```

运行项目自带的Gradio，若网页成功运行则证明部署成功，可直接测试接口（不用进行网页指示的操作，我已完成）

### 1.2 数字人朗读语音视频接口

本接口用于收取用户上传的音频文件并生成对应的数字人视频。前端上传音频数据后，后端将调用模型生成视频并返回。
(先试试能否成功展示出视频，成功后再调用生成数字人对应语音视频)

#### 请求说明：

* URL：`http://localhost:8000/generate-video/`
* 请求方式：POST
* 请求头：`{"Content-Type": "multipart/form-data"}`
* 请求参数名：`audio` 请求参数值：`file`（本地上传音频文件）

#### 响应说明：

* 响应成功则返回视频流，响应失败则响应失败 (._. )

### 1.3 数字人实时对话网页部署

将`web_demo/static`内的所有内容复制到项目中使用部署。

（目前出bug待完善。。。）

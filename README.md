# 报销单处理系统

基于千问AI的智能报销单处理系统，可以自动识别报销单图片中的文字信息，并转换为可编辑的Excel表格。

## 功能特性

- 🖼️ 支持多种图片格式（JPG、JPEG、PNG）
- 🤖 使用千问AI进行智能文字识别
- ✏️ 识别结果支持人工编辑和校正
- 📊 一键生成标准Excel报销单
- 🔄 防重复上传检测
- ☁️ MinIO对象存储支持

## 环境要求

- Python 3.8+
- MinIO 服务器
- DashScope API 密钥

## 安装说明

1. 克隆项目：
```bash
git clone https://github.com/yourusername/expense-processor.git
cd expense-processor
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
复制 `.env.example` 为 `.env` 并填写必要的配置信息：
```bash
cp .env.example .env
```

必需的环境变量：
- `MINIO_HOST`：MinIO服务器地址
- `MINIO_ACCESS_KEY`：MinIO访问密钥
- `MINIO_SECRET_KEY`：MinIO秘密密钥
- `DASHSCOPE_API_KEY`：DashScope API密钥

## 使用说明

1. 启动应用：
```bash
streamlit run streamlit_app.py
```

2. 使用流程：
   - 上传报销单图片
   - 等待AI识别完成
   - 检查并编辑识别结果
   - 点击"确认并生成Excel"
   - 下载生成的Excel文件

## 更新日志

[2025-01-13]: [1.5.0] 
- 移除用户认证系统
- 添加识别结果编辑功能
- 添加图片重复上传检测
- 优化用户界面交互

[2025-01-12]: [1.4.1] 
- 添加邮箱和密码验证
- 提升登录注册安全性

[2025-01-12]: [1.4.0] 
- 实现用户认证功能
- 添加数据持久化存储

[2025-01-11]: [1.3.0] 
- 添加MinIO存储支持
- 优化图片处理流程

[2025-01-10]: [1.2.0] 
- 集成千问AI接口
- 实现图片文字识别

[2025-01-09]: [1.1.0] 
- 创建基础项目结构
- 添加图片上传功能

## 贡献指南

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT License

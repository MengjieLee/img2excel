# 报销单处理系统

基于千问大模型的智能报销单处理系统，可以自动识别报销单图片中的关键信息，生成标准化的Excel报表，并将数据持久化到MinIO存储服务。

## 功能特点

- 支持多张报销单图片批量上传
- 自动识别报销单中的关键信息：
  - 报销单号
  - 日期
  - 报销人
  - 部门
  - 费用明细（项目名称和金额）
- 生成标准格式的Excel报表（REI sheet）
- 支持日期格式自动转换
- 实时显示处理结果
- 数据持久化到MinIO存储服务
  - 自动生成带有时间戳的文件名
  - 提供7天有效的下载链接
- 提供导出和清除功能

## 技术栈

- Web框架：Streamlit
- 图像处理：Pillow
- AI模型：千问API
- 存储服务：MinIO
- Excel处理：Pandas, OpenPyXL
- 其他：Python-dotenv, Requests

## 环境要求

- Python 3.11+
- MinIO服务器
- Docker（用于容器化部署）
- 依赖包：见 requirements.txt

## 安装说明

1. 克隆项目：
```bash
git clone [项目地址]
cd project_a
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
创建 .env 文件并设置以下变量：
```
# API Keys
DASHSCOPE_API_KEY=your_api_key_here

# MinIO Configuration
MINIO_HOST=localhost:9000
MINIO_ACCESS_KEY=your_access_key_here
MINIO_SECRET_KEY=your_secret_key_here

# Docker Configuration
DOCKER_USERNAME=your_username
DOCKER_PASSWORD=your_password
```

## 使用说明

1. 启动MinIO服务器（如果是本地开发）：
```bash
docker run -p 9000:9000 -p 9001:9001 minio/minio server /data --console-address ":9001"
```

2. 启动应用：
```bash
streamlit run streamlit_app.py
```

3. 在浏览器中访问应用（默认地址：http://localhost:9527）

## Docker 部署

### 方式一：从阿里云镜像仓库拉取（推荐）
```bash
# 拉取镜像（使用最新版本）
docker pull crpi-608fba9xxjhcq7gx.cn-shanghai.personal.cr.aliyuncs.com/dcby/img2excel:latest

# 或拉取指定版本
docker pull crpi-608fba9xxjhcq7gx.cn-shanghai.personal.cr.aliyuncs.com/dcby/img2excel:latest

# 运行容器
docker run -p 9527:9527 --env-file .env crpi-608fba9xxjhcq7gx.cn-shanghai.personal.cr.aliyuncs.com/dcby/img2excel:latest
```

### 方式二：本地构建
```bash
# 构建并推送镜像
chmod +x local_build_image.sh
./local_build_image.sh <版本号>  # 例如：./local_build_image.sh latest
```

local_build_image.sh 脚本功能：
- 从 .env 文件或环境变量加载 Docker 认证信息
- 构建并标记 Docker 镜像
- 推送镜像到阿里云容器镜像服务
- 保存本地镜像备份（保留最新3个版本）
- 自动清理本地镜像缓存

## 项目结构

```
project_a/
├── streamlit_app.py    # 主应用程序
├── requirements.txt    # 项目依赖
├── .env               # 环境变量配置
├── Dockerfile         # Docker构建文件
├── local_build_image.sh # 本地构建脚本
└── utils/
    ├── qwen_processor.py    # 千问API处理模块
    ├── image_processor.py   # 图片处理模块
    ├── excel_processor.py   # Excel处理模块
    └── storage.py          # MinIO存储模块
```

## 分支管理

项目采用以下分支策略：

- `main`: 生产环境分支，保持稳定可用状态
  - 只接受来自 `dev` 分支的合并请求
  - 每次合并都会自动构建并发布新版本
  - 所有合并到 main 的代码必须经过完整测试

- `dev`: 开发分支，用于功能开发和测试
  - 所有新功能都在此分支上开发
  - 功能开发完成后提交 PR 到 main 分支
  - 定期从 main 分支同步更新

- 功能分支: 从 dev 分支创建，命名格式为 `feature/功能名称`
  - 单个功能开发完成后合并回 dev 分支
  - 合并前需要进行代码审查
  - 合并后删除功能分支

### 分支工作流程

1. 从 dev 分支创建功能分支：
```bash
git checkout dev
git pull
git checkout -b feature/新功能名称
```

2. 开发完成后合并到 dev：
```bash
git checkout dev
git pull
git merge feature/新功能名称
git push origin dev
```

3. 提交 PR 到 main 分支：
在 GitHub 上创建从 dev 到 main 的 Pull Request

## 更新日志

### [2025-01-11]: [latest]
- 优化项目分支管理策略
- 创建开发分支(dev)用于新功能开发
- 更新文档，添加分支管理说明
- 规范化代码提交流程

### [2025-01-10]: [1.3.6]
- 优化 Streamlit UI，将弃用的 use_column_width 参数更新为 use_container_width
- 简化 Dockerfile，提高构建效率
- 更新 MinIO 客户端配置，修复初始化问题
- 更新依赖版本范围，提高兼容性

### [2025-01-10]: [latest]
- 优化 Docker 构建脚本，提高代码可维护性
- 简化镜像构建流程，移除多余标签
- 改进错误处理和日志输出
- 更新文档，完善 Docker 部署说明
- 统一镜像命名规范

### [2025-01-10]: [1.3.1]
- 优化 Docker 构建脚本，使用环境变量管理认证信息
- 更新文档，添加 Docker 配置说明
- 优化构建过程，提高构建速度

### [2025-01-09]: [1.3.0]
- 修改服务端口为 9527
- 优化镜像保存格式，使用版本号作为文件名后缀
- 更新文档中的端口信息

## 注意事项

1. 确保环境变量配置正确（包括 Docker 认证信息）
2. 启动前确保MinIO服务器正常运行
3. 上传的图片格式支持：jpg、jpeg、png
4. Excel文件下载链接有效期为7天
5. 使用Docker时，建议优先使用阿里云镜像源以提高下载速度
6. Docker 相关的敏感信息请通过环境变量管理，不要直接写入代码.

## 许可证

MIT License

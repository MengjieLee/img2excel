import streamlit as st
import os
from dotenv import load_dotenv
import uuid
from utils.image_processor import ImageProcessor
from utils.qwen_processor import QwenProcessor
from utils.excel_processor import ExcelProcessor
from utils.storage import StorageManager
from PIL import Image
import io
import sys
from pathlib import Path
import tempfile

# 获取项目根目录
ROOT_DIR = Path(__file__).resolve().parent

# 加载环境变量
env_path = ROOT_DIR / '.env'
if not env_path.exists():
    load_dotenv(env_path)
else:
    st.warning("WARNING: .env file not found, params will be loaded from env vars!")

# 验证必要的环境变量
REQUIRED_ENV_VARS = {
    'DASHSCOPE_API_KEY': '千问 API Key',
    'MINIO_HOST': 'MinIO 服务器地址',
    'MINIO_ACCESS_KEY': 'MinIO 访问密钥',
    'MINIO_SECRET_KEY': 'MinIO 密钥'
}

missing_vars = []
for var, description in REQUIRED_ENV_VARS.items():
    if not os.getenv(var):
        missing_vars.append(f"{description} ({var})")

if missing_vars:
    st.error(f"缺少必要的环境变量: {', '.join(missing_vars)}")
    sys.exit(1)

def get_qwen_service():
    """按需获取千问服务实例"""
    if 'qwen' not in st.session_state:
        st.session_state.qwen = QwenProcessor(os.getenv("DASHSCOPE_API_KEY"))
    return st.session_state.qwen

def get_excel_service():
    """按需获取Excel处理服务实例"""
    if 'excel' not in st.session_state:
        st.session_state.excel = ExcelProcessor()
    return st.session_state.excel

def get_storage_service():
    """按需获取存储服务实例"""
    if 'storage' not in st.session_state:
        st.session_state.storage = StorageManager(
            os.getenv("MINIO_HOST"),
            os.getenv("MINIO_ACCESS_KEY"),
            os.getenv("MINIO_SECRET_KEY")
        )
    return st.session_state.storage

def process_and_save(image_bytes, filename):
    """处理图片并保存结果"""
    try:
        # 1. 识别图片
        qwen = get_qwen_service()
        result = qwen.process_image(image_bytes)
        if not qwen.validate_response(result):
            return None, "识别结果格式不正确", None
        
        # 2. 生成Excel
        excel_service = get_excel_service()
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            output_path = tmp_file.name
            
        excel_service.create_excel([result], output_path)
        
        # 3. 上传到MinIO
        with open(output_path, 'rb') as f:
            excel_data = f.read()
            
        storage_service = get_storage_service()
        # 使用识别结果中的报销人和报销单号信息
        file_url = storage_service.save_excel(
            excel_data,
            expense_user=result.get('报销人', ''),
            expense_id=result.get('报销单号', '')
        )
        
        # 4. 清理临时文件
        os.unlink(output_path)
        
        return result, None, file_url
    except Exception as e:
        return None, str(e), None

def display_result(result, file_url=None):
    """显示识别结果"""
    st.success("识别成功！")
    st.write("基本信息：")
    st.write(f"- 报销单号：{result['报销单号']}")
    st.write(f"- 日期：{result['日期']}")
    st.write(f"- 报销人：{result['报销人']}")
    st.write(f"- 部门：{result['部门']}")
    
    st.write("费用明细：")
    for item in result['项目']:
        st.write(f"- {item['名称']}: ¥{item['金额']}")
    st.write(f"**总金额：¥{result['总金额']}**")
    
    if file_url:
        st.success("Excel文件已生成并保存")
        st.markdown(f"[点击下载Excel文件]({file_url})")

def main():
    st.title("报销单处理系统")
    st.caption("使用千问AI进行智能识别")
    
    # 文件上传区域
    uploaded_files = st.file_uploader(
        "上传报销单图片",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="file_uploader"
    )
    
    # 处理上传的文件
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # 读取图片数据
            image_bytes = uploaded_file.getvalue()
            image = Image.open(io.BytesIO(image_bytes))
            
            # 创建两列布局
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(image, caption=f"报销单: {uploaded_file.name}", use_container_width=True)
            
            with col2:
                # 处理图片并保存Excel
                with st.spinner(f"正在处理 {uploaded_file.name}..."):
                    result, error, file_url = process_and_save(image_bytes, uploaded_file.name)
                    if result:
                        display_result(result, file_url)
                    else:
                        st.error(f"识别失败: {error}")

if __name__ == "__main__":
    main()

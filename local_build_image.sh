#!/bin/bash

set -e  # 遇到错误立即退出

# 配置变量
REGISTRY="crpi-608fba9xxjhcq7gx.cn-shanghai.personal.cr.aliyuncs.com"
NAMESPACE="dcby"
IMAGE_NAME="img2excel"
SAVE_DIR="dist"

# 函数：检查环境变量
check_env_vars() {
    if [ -f .env ]; then
        export $(cat .env | grep -v '^#' | xargs)
        REGISTRY_USERNAME=${DOCKER_USERNAME}
        REGISTRY_PASSWORD=${DOCKER_PASSWORD}
    else
        echo "WARNING: .env file not found, params will be loaded from env vars"
    fi

    if [ -z "${REGISTRY_USERNAME}" ]; then
        echo "Error: DOCKER_USERNAME not set in .env file"
        echo "Please add DOCKER_USERNAME=your_username to your .env file"
        exit 1
    fi

    if [ -z "${REGISTRY_PASSWORD}" ]; then
        echo "Error: DOCKER_PASSWORD not set in .env file"
        echo "Please add DOCKER_PASSWORD=your_password to your .env file"
        exit 1
    fi
}

# 函数：检查版本参数
check_version() {
    VERSION=$1
    if [ -z "${VERSION}" ]; then
        echo "Error: Version parameter is required"
        echo "Usage: $0 <version>"
        echo "Example: $0 1.3.2"
        exit 1
    fi
    FULL_IMAGE_NAME="${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:${VERSION}"
}

# 函数：登录镜像仓库
docker_login() {
    echo "Logging in to Aliyun Container Registry..."
    echo ${REGISTRY_PASSWORD} | docker login --username ${REGISTRY_USERNAME} --password-stdin "${REGISTRY}"
}

# 函数：构建和推送镜像
build_and_push() {
    echo "Building Docker image: ${FULL_IMAGE_NAME}"
    docker build -t ${FULL_IMAGE_NAME} .
    docker tag ${FULL_IMAGE_NAME} ${FULL_IMAGE_NAME}

    echo "Pushing image to Aliyun Container Registry..."
    docker push ${FULL_IMAGE_NAME}
}

# 函数：保存本地镜像
save_local_image() {
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    mkdir -p "${SAVE_DIR}"

    echo "Saving image locally..."
    docker save ${FULL_IMAGE_NAME} | gzip > "${SAVE_DIR}/${IMAGE_NAME}-${VERSION}-${TIMESTAMP}.tar.gz"

    echo "Cleaning up old image files..."
    ls -t "${SAVE_DIR}/${IMAGE_NAME}-*.tar.gz" 2>/dev/null | tail -n +4 | xargs -I {} rm {} 2>/dev/null
}

# 函数：清理环境
cleanup() {
    echo "Cleaning up local images..."
    docker rmi "${FULL_IMAGE_NAME}" 2>/dev/null || true
}

# 主函数
main() {
    check_env_vars
    check_version "$1"
    docker_login
    build_and_push
    save_local_image
    cleanup

    echo "Done! Image has been built, pushed and saved."
    echo "Local tar archive: ${SAVE_DIR}/${IMAGE_NAME}-${VERSION}-${TIMESTAMP}.tar.gz"
    echo "Remote image: ${FULL_IMAGE_NAME}"
    echo ""
    echo "You can run the image using:"
    echo "docker run -p 9527:9527 --env-file .env ${FULL_IMAGE_NAME}"
}

# 执行主函数
main "$@"

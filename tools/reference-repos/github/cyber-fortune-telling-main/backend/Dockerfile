# 生产环境 Dockerfile - 包含构建和 Sharp 模块修复
FROM node:22.14.0

# 设置工作目录
WORKDIR /app

# 配置 apt 使用阿里云镜像源加速下载
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

# 更新包管理器并安装必要的系统依赖（包括 Sharp 需要的 libvips）
RUN apt-get update && apt-get install -y \
    python3 \
    make \
    g++ \
    git \
    curl \
    libvips-dev \
    libvips-tools \
    && rm -rf /var/lib/apt/lists/*

# 设置npm使用淘宝镜像源
RUN npm config set registry https://registry.npmmirror.com/

# 复制 package.json 和 package-lock.json
COPY package*.json ./

ENV SHARP_IGNORE_GLOBAL_LIBVIPS="1"
ENV npm_config_sharp_libvips_binary_host="https://registry.npmmirror.com/-/binary/sharp-libvips"
# 安装依赖（包括开发依赖，因为构建需要）
RUN npm install --verbose

# 复制源代码（排除node_modules）
COPY . .

# 创建必要的目录
RUN mkdir -p .tmp public/uploads

# 修复 @swc/core native binding 问题 - 基于 Stack Overflow 解决方案
RUN npm update && npm install @swc/core

# 设置环境变量
ENV STRAPI_TELEMETRY_DISABLED=true
ENV NODE_ENV=production

# 构建项目（增加详细输出）
RUN npm run build --verbose

# 清理构建缓存，减少镜像大小（但保留 sharp）
RUN npm prune --omit=dev && npm cache clean --force

# 暴露端口  
EXPOSE 11337

# 健康检查
HEALTHCHECK --interval=60s --timeout=15s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:11337/api/get-tips || exit 1

# 启动应用
CMD ["npm", "run", "start"] 

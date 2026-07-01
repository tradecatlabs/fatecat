# 前端生产环境 Dockerfile
FROM node:22.14.0

# 设置工作目录
WORKDIR /app

# 配置 apt 使用阿里云镜像源加速下载
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources


# 安装必要的系统依赖
RUN apt-get update && apt-get install -y \
    python3 \
    make \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 设置npm使用淘宝镜像源
RUN npm config set registry https://registry.npmmirror.com/
# 安装 pnpm
RUN npm install -g pnpm
# 设置npm使用淘宝镜像源
RUN pnpm config set registry https://registry.npmmirror.com/

# 复制 package.json 
COPY package.json ./

# 安装依赖
RUN pnpm install

# 复制源代码
COPY . .

# 定义构建时参数
ARG NEXT_PUBLIC_API_BASE_URL
# 将构建时参数转换为环境变量
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}

# 构建 Next.js 应用
RUN pnpm run build

# 暴露端口 4000（根据 package.json 中的配置）
EXPOSE 4000

# 启动生产服务器
CMD ["pnpm", "run", "start"]


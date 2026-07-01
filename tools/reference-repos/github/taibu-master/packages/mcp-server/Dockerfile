FROM node:20-alpine

# 安装 pnpm
RUN npm install -g pnpm

WORKDIR /app

# 复制 workspace 配置
COPY pnpm-workspace.yaml package.json pnpm-lock.yaml ./

# 复制所有 packages
COPY packages/core ./packages/core
COPY packages/mcp-server ./packages/mcp-server

# 安装依赖（包括 devDependencies 用于构建）
RUN pnpm install --frozen-lockfile

# 构建 core
WORKDIR /app/packages/core
RUN pnpm build

# 构建 mcp-server
WORKDIR /app/packages/mcp-server
RUN pnpm build

RUN addgroup -S mcpgroup && adduser -S mcpuser -G mcpgroup

EXPOSE 3001

USER mcpuser

CMD ["node", "dist/index.js"]

# 玄乎儿分光镜

科学的尽头是玄学，玄学的尽头是玄乎儿。

## 《玄乎儿分光镜》能干啥？

1. 每日给出趋吉避凶的桌面摆件，提升运势，情绪价值拉满。
2. 活得久才是硬道理，身体革命的本钱，本项目可以根据个人健康状况，给出每日健康建议，做好健康管理。
3. 每天自动化测算八字运势，塔罗运势，幸运数字，幸运色，中午吃什么等等，解决选择困难症。

2025年7月，基于Deepseek的风水算命项目《玄乎儿分光镜》完成了开源，只需提供[deepseek官方的key](https://platform.deepseek.com/api_keys) 即可通过 docker 启动，完美本地运行。

经过一个月的开发和验证，我发现电脑运行这个程序，就会带来好心情，机魂大悦人也开心，有些人想玩这个程序，但担心泄露个人八字隐私，于是这个程序开源了，有 docker 基础就能完全本地部署。希望各路大师能提供强大的提示词，让这个项目更好玩。

如果你不想本地部署，可以用在线体验地址 [https://ft.fangyuanxiaozhan.com/register](https://ft.fangyuanxiaozhan.com/register)

有问题可以通过https://github.com/zhaoolee/cyber-fortune-telling  提 issues 

项目的起源：我有个朋友，喜欢**在桌面搞点风水摆件，提升运势**，我感觉这东西虽然玄学，但确实能提供心理安慰的作用，让人心情愉悦。

![](https://cdn.fangyuanxiaozhan.com/assets/1746849484470a0c7NxG3.png)

于是，我打算搞一个**电子风水摆件**，录入自己的八字信息，每天自动调用满血版DeepSeek，计算今天最适合的风水摆件，并通过**屏幕展示在桌面上**。为了避免过于单调，还可以让Deepseek大模型把**今天中午适合吃什么**，今天**适合联系哪些朋友**，今天**幸运数字是什么**，今天的**幸运色是什么**，变成**一个个小建议轮播**到屏幕上！


## 在线体验

在线体验地址 [https://ft.fangyuanxiaozhan.com/register](https://ft.fangyuanxiaozhan.com/register)


## 一些功能说明

进入网页后，需要录入出生日期和时间，方便大模型八字获取八字信息（点击圆形头像，有惊喜🕶）

![](https://cdn.fangyuanxiaozhan.com/assets/1746852819331AXfdk2fZ.png)

点击注册后，程序会自动跳转到一个url，这个网页的url可以放到树莓派浏览器打开，每天的零点后，浏览器会自动刷新，重新计算当天运势；（底部有个输入框，里面有塔罗占卜，今天适合听什么歌的预制对话，也可以随意提问，和大模型Chat的玩法基本一样）

![](https://cdn.fangyuanxiaozhan.com/assets/17468525802596fhca86F.png)


## 基于个人详细信息，并给出健康建议

![](https://cdn.fangyuanxiaozhan.com/assets/1752137366719zT3faS4b.jpeg)


![](https://cdn.fangyuanxiaozhan.com/assets/1752137492289way5kr6x.jpeg)

「养」方：保持中国传统阅读习惯（从右往左，从上往下读）
![](https://cdn.fangyuanxiaozhan.com/assets/1752139697787X3r2mGMa.jpeg)


## 满级人类常看黄历

有生活经验的人类，出门前都会看黄历

![](https://cdn.fangyuanxiaozhan.com/assets/1752140511198hJbKkipT.jpeg)

我们的程序会根据用户个人状况，给出适合做什么，不适合做什么的建议



## ⚙️录入个人健康状况



大模型输出完成后，可以点击编辑信息按钮，进入设置页


![](https://cdn.fangyuanxiaozhan.com/assets/1752137653099cHGrErED.jpeg)

身体是革命的本钱，支持编辑个人健康状况，便于给出健康建议

![](https://cdn.fangyuanxiaozhan.com/assets/1752137704796Mh0jj764.jpeg)

## 💰增减测算栏目

如果你是私有部署，想要节省 token，可以自行增减测算的栏目，后续会支持用户自定义测算插件。

![](https://cdn.fangyuanxiaozhan.com/assets/1752137758376CFEQQyFR.jpeg)


## 这不是 Bug，是Feature！

界面里面有些色块，是用来隐藏敏感信息的，鼠标 hover即可查看

![no bug](https://cdn.fangyuanxiaozhan.com/assets/1752140232633P5bBsPx2.gif)


## 风水强运摆件模式

点击右上角的「进入玄修」，就会进入风水摆件页面，风水摆件会有一个闪着光晕的细腻动画。


![image-20250510124133540](https://cdn.fangyuanxiaozhan.com/assets/1746856629981Edtrn7R3.png)


实机运行效果如下（画面被压缩了，实际效果好很多，一度引起办公室众多玄学爱好者的围观）

![](https://cdn.fangyuanxiaozhan.com/assets/1746852527676RtQnXNMx.jpeg)

## 番茄钟加强运桌面摆件模式

如果经常工作到忘了放松眼睛，可以使用加强版番茄钟模式，每隔 25 分钟，就会提醒你休息五分钟，左侧显示今日 tips ，右侧的强运摆件显示在表盘上


![](https://cdn.fangyuanxiaozhan.com/assets/1752138271465e8NWGGid.jpeg)


如果你是一个**二手电子垃圾爱好者，或者运维老哥**，也可以将**风水摆件**放到机房，**机魂大悦，让你一觉到天明**。

我为我的二手硬件小机房，添加了一个风水摆件，内网穿透的成功率变高了很多😁 （信则有，不信则无）。


![pi5](https://cdn.fangyuanxiaozhan.com/assets/1746849238609ZsZFGCYQ.jpeg)


## 支持 MCP调用


### 生成docker镜像
```
cd mcp-server
npm run docker:build
```

### 支持 MCP调用 

客户端推荐使用 [ChatBox](https://github.com/chatboxai/chatbox)

```
{
  "mcpServers": {
    "cyber-fortune-telling-mcp-docker": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "--network", "host",
        "-e", "CYBER_FORTUNE_API_BASE_URL=http://localhost:11337/api",
        "-e", "LOG_LEVEL=info",
        "cyber-fortune-mcp-server"
      ],
      "env": {}
    }
  }
} 
```

![参数查看](https://cdn.fangyuanxiaozhan.com/assets/1752393590883peRC28BZ.jpeg)


![请求结果](https://cdn.fangyuanxiaozhan.com/assets/1752393590897iyD0KQpa.jpeg)


## 后续计划，搞个更酷的电子潮玩版本

我打算用分光棱镜做个更酷的简化版本，Demo如下图所示，可以显示有限的文字，依然是每天占卜，给出建议，成本基本在100块以内，而且会非常省电。作为电子潮玩售卖，图一乐！

![trans](https://cdn.fangyuanxiaozhan.com/assets/1746853648246t6cZN4W3.jpeg)


在线体验地址 [https://ft.fangyuanxiaozhan.com/register](https://ft.fangyuanxiaozhan.com/register)


## 如果你不想录入信息，可以试试录好信息的页面，感觉满意，再进行私有化部署

已经录好信息的测试页面 （点击可以查看效果）http://ft.fangyuanxiaozhan.com/linkMe/uid-1752136662802-6760


## 🚀 快速开始

本项目难点不在于代码，而在于产品思路，工程基于Strapi + Next.js构建，目前代码还在整理完善阶段

```bash
# 克隆项目
git clone --depth=1 https://github.com/zhaoolee/cyber-fortune-telling.git
cd cyber-fortune-telling

# 复制环境变量
cp example.env .env
```

## 🔧 环境配置

编辑 `.env` 文件，配置以下必要参数：

```bash
# DeepSeek API 配置 (推荐使用，性价比高)
OPENAI_API_KEY=sk-your-deepseek-api-key
OPENAI_BASE_URL=https://api.deepseek.com/v1
```

## 🚀 启动项目

### 使用 Docker Compose（推荐）

```bash
# 构建服务
docker compose build --no-cache

# 启动所有服务
docker compose up

# 后台运行
docker compose up -d

# 查看日志
docker compose logs -f

# 停止服务
docker compose down
```

## 如果不需要Docker数据库服务(请前往.env自定义数据库信息)
```
docker compose -f docker-compose-no-database.yml
```

## 开发者备忘

```
# 拉取代码
git checkout dev

git pull

# 构建新镜像

docker compose -f ./docker-compose-no-database.yml build --no-cache

# 关闭旧服务
docker compose -f ./docker-compose-no-database.yml down


# 启动
docker compose -f ./docker-compose-no-database.yml up -d

```

## 🛠️ 技术栈

### 前端
- **Next.js 15.1.9** - React 框架
- **React 19.0.1** - JavaScript 库
- **Material-UI 7.1.0** - UI 组件库 (@mui/material)
- **Framer Motion 12.9.4** - 动画库
- **Axios 1.7.9** - HTTP 客户端
- **Showdown** - Markdown 解析器
- **Next PWA** - 渐进式 Web 应用支持
- **Lunar JavaScript** - 农历日期处理
- **Moment.js** - 日期时间处理

### 后端
- **Strapi 5.10.3** - 无头 CMS
- **Node.js 22.14.0+** - 运行时环境
- **PostgreSQL 17.5** - 主数据库
- **SQLite3** - 开发数据库
- **OpenAI API 4.96.2** - AI 服务接口
- **IntelliNode** - AI 服务库
- **MQTT** - 消息队列协议

### 部署
- **Docker** - 容器化部署
- **Docker Compose** - 多容器编排

### 访问地址
- 前端：http://localhost:4000
- 管理后台：http://localhost:11337/admin

## 🌟 功能特色

- 🎯 **AI 算命** - 基于大语言模型的智能算命
- 📱 **响应式设计** - 完美适配手机和电脑
- 🚀 **PWA 支持** - 可安装为手机应用
- 🔐 **用户系统** - 完整的注册登录功能
- 📊 **管理后台** - Strapi 提供的强大后台
- ✨ **风水摆件** - 电子风水摆件展示
- 🌈 **多主题切换** - 支持多种颜色主题
- 📅 **农历支持** - 完整的农历日期系统
- 🔄 **实时聊天** - 与AI实时对话功能
- 📱 **移动优先** - 移动端优化体验
- 🎨 **动画效果** - 流畅的动画交互

## 🔮 项目背景

基于大模型的风水算命摆件，为桌面提供**电子风水摆件**体验。录入八字信息后，每天自动调用 DeepSeek 计算适合的风水摆件，通过屏幕展示在桌面上。

### 特色功能
- 📅 每日运势自动更新
- 🎨 动态风水摆件展示
- 🤖 AI 智能对话
- 📱 多设备适配
- 🔄 自动刷新机制

## 🤝 贡献指南

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🐳 Docker 部署说明

项目使用 Docker Compose 进行容器化部署，包含以下服务：

- **PostgreSQL 17.5** - 数据库服务，端口 5432
- **Strapi Backend** - 后端服务，端口 1337
- **Next.js Frontend** - 前端服务，端口 4000

### 环境要求

- Docker 20.10+
- Docker Compose 2.0+
- Node.js 22.14.0+（本地开发）

### 数据持久化

- `postgres_data` - PostgreSQL 数据
- `backend_uploads` - 后端上传文件
- `backend_data` - 后端临时数据



## 🙏 致谢

- [Next.js](https://nextjs.org/) - 前端框架
- [Strapi](https://strapi.io/) - 后端 CMS
- [DeepSeek](https://deepseek.com/) - AI 服务
- [Material-UI](https://mui.com/) - UI 组件库
- [Framer Motion](https://www.framer.com/motion/) - 动画库
- [PostgreSQL](https://www.postgresql.org/) - 数据库
- [Docker](https://www.docker.com/) - 容器化平台
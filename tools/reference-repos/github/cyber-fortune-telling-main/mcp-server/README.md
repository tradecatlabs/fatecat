# 支持MCP调用

## 生成docker镜像
```
cd mcp-server
npm run docker:build
```



## 支持 MCP调用 

推荐使用 ChatBox

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

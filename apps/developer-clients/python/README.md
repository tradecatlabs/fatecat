# fatecat-client

`fatecat-client` 是 FateCat 公开 HTTP API 的轻量 Python 客户端。该包只发送远程请求，不包含八字、紫微、历法算法、典籍、vendor 快照或服务端运行时。

```python
from fatecat_client import FateCatClient

client = FateCatClient("https://tradecatlabs-fatecat.hf.space")
print(client.health())
print(client.capabilities())
```

带凭证的环境应从进程环境或密钥管理系统读取 token，再通过 `token=` 显式传入。客户端不会保存 token、用户输入或报告正文。

本目录只证明本地构建和 clean-room 安装；是否已发布到 PyPI 以 `contracts/fate/developer/public-client-distribution.json` 为准。

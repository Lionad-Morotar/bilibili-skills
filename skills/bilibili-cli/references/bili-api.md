# bilibili-api 使用指南

当 [bilibili-cli](https://github.com/jackwener/bilibili-cli) 无法满足需求时（如发送图文动态），可使用 [bilibili-api](https://nemo2011.github.io/bilibili-api) 库。

## 安装

```bash
pip3 install bilibili-api-python aiohttp
```

## 凭证构造

bilibili-api 需要 `Credential` 对象进行登录操作。如果你已经使用 bilibili-cli 登录过，可以直接复用其存储的凭证。

### 从 bilibili-cli 读取凭证

```python
import json
import asyncio
from pathlib import Path
from bilibili_api import Credential

# 读取 bilibili-cli 存储的凭证
credential_path = Path.home() / ".bilibili-cli" / "credential.json"

with open(credential_path) as f:
    cred_data = json.load(f)

# 构造 Credential 对象
credential = Credential(
    sessdata=cred_data["sessdata"],
    bili_jct=cred_data["bili_jct"],
    buvid3=cred_data.get("buvid3", ""),
    buvid4=cred_data.get("buvid4", ""),
    dedeuserid=cred_data.get("dedeuserid", "")
)

print(f"已登录用户 UID: {credential.dedeuserid}")
```

### 使用脚本快速获取

提供了辅助脚本 `./references/bili-api/get_credential.py`：

```bash
python ./references/bili-api/get_credential.py
```

在 Python 代码中使用：

```python
from references.bili-api.get_credential import get_credential

async def main():
    credential = get_credential()
    print(f"UID: {credential.dedeuserid}")

asyncio.run(main())
```

## 示例：发送图文动态

```python
import asyncio
from bilibili_api import dynamic
from bilibili_api.utils.picture import Picture
from references.bili-api.get_credential import get_credential

async def main():
    credential = get_credential()

    # 加载本地图片
    picture = Picture.from_file("/path/to/image.jpg")

    # 构建图文动态
    build = dynamic.BuildDynamic.empty()
    build.add_plain_text("这是一条图文动态")
    build.add_image(picture)

    # 发送动态
    result = await dynamic.send_dynamic(
        info=build,
        credential=credential
    )
    print(f"动态ID: {result['dyn_id']}")

asyncio.run(main())
```

**多图示例：**

```python
# 多张图片
pics = [Picture.from_file(f"/path/to/image{i}.jpg") for i in range(1, 4)]
build = dynamic.BuildDynamic.empty()
build.add_plain_text("多条图片动态")
build.add_image(pics)  # 传入列表
```

## 示例：发送纯文本动态

```python
import asyncio
from bilibili_api import dynamic
from references.bili-api.get_credential import get_credential

async def main():
    credential = get_credential()
    result = await dynamic.send_text("Hello from bilibili-api!", credential)
    print(f"动态ID: {result['dyn_id']}")

asyncio.run(main())
```

## 示例：获取用户信息

```python
import asyncio
from bilibili_api import user
from references.bili-api.get_credential import get_credential

async def main():
    credential = get_credential()

    # 获取当前登录用户信息
    u = user.User(uid=int(credential.dedeuserid), credential=credential)
    info = await u.get_user_info()
    print(info)

asyncio.run(main())
```

## 注意事项

1. **异步操作**：bilibili-api 全部为异步 API，需要使用 `async/await`
2. **请求频率**：请求太快会触发 412 错误，必要时添加延迟或使用代理
3. **凭证安全**：不要将凭证泄露给他人
4. **buvid3 缺失**：从 bilibili-cli 读取的凭证可能缺少 `buvid3`，某些 API 可能受影响

## 相关链接

- [bilibili-api 官方文档](https://nemo2011.github.io/bilibili-api)
- [获取凭证文档](https://nemo2011.github.io/bilibili-api/#/get-credential)

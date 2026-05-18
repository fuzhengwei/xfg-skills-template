---
name: api-integration
description: 集成 REST API，包括请求构建、认证处理、错误重试和响应解析。当用户需要调用外部 API、集成第三方服务、处理 HTTP 请求，或提到 API、接口、Webhook 时使用此技能。
license: Apache-2.0
metadata:
  author: xfg-studio
  version: "1.0.0"
  category: integration
---

# API 集成技能

帮助 Agent 正确调用 REST API，处理认证、重试和错误。

## 请求构建

### 使用 requests 库（推荐）

```python
import requests

# GET 请求
response = requests.get(
    "https://api.example.com/v1/users",
    headers={"Authorization": f"Bearer {token}"},
    params={"page": 1, "per_page": 20},
    timeout=30
)

# POST 请求
response = requests.post(
    "https://api.example.com/v1/users",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={"name": "张三", "email": "zhangsan@example.com"},
    timeout=30
)
```

### 使用 curl（简单场景）

```bash
curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "https://api.example.com/v1/users?page=1"
```

## 认证模式

| 类型 | Header 格式 | 适用场景 |
|------|------------|---------|
| Bearer Token | `Authorization: Bearer <token>` | OAuth 2.0 / JWT |
| API Key | `X-API-Key: <key>` | 简单 API 密钥 |
| Basic Auth | `Authorization: Basic <base64>` | 传统认证 |
| HMAC | 自定义 Header | 阿里云/腾讯云 API |

## 错误处理

1. **网络错误**：重试最多 3 次，间隔 1/2/4 秒（指数退避）
2. **429 Too Many Requests**：读取 `Retry-After` Header，等待后重试
3. **5xx 服务端错误**：重试最多 2 次
4. **4xx 客户端错误**：不重试，报告错误详情

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retries = Retry(total=3, backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))
```

## 响应解析

```python
# 检查状态码
response.raise_for_status()

# 解析 JSON
data = response.json()

# 分页处理
while url:
    response = session.get(url, headers=headers, timeout=30)
    data = response.json()
    results.extend(data.get("items", []))
    url = data.get("next_page_url")
```

## Gotchas

- 始终设置 `timeout` 参数，避免请求无限挂起
- 敏感信息（Token、API Key）使用环境变量，不硬编码
- 某些 API 返回的错误信息在 response body 而非 status code
- 分页 API 注意是否有总数限制，避免无限循环

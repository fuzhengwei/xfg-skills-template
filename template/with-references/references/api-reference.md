# API 参考文档

> 这是参考文档模板。根据你的实际 API 替换内容。

## 基础信息

- 基础 URL: `https://api.example.com/v1`
- 认证方式: Bearer Token
- 响应格式: JSON

## 端点列表

### GET /users

获取用户列表。

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认 1 |
| per_page | int | 否 | 每页条数，默认 20 |
| search | string | 否 | 搜索关键词 |

**响应示例：**

```json
{
  "data": [
    {
      "id": 1,
      "name": "张三",
      "email": "zhangsan@example.com"
    }
  ],
  "total": 100,
  "page": 1
}
```

### POST /users

创建用户。

**请求体：**

```json
{
  "name": "string (必填)",
  "email": "string (必填)",
  "role": "string (可选, 默认: member)"
}
```

## 错误码

| 状态码 | 错误码 | 说明 |
|--------|--------|------|
| 400 | INVALID_INPUT | 输入参数无效 |
| 401 | UNAUTHORIZED | 未认证 |
| 403 | FORBIDDEN | 无权限 |
| 404 | NOT_FOUND | 资源不存在 |
| 429 | RATE_LIMITED | 请求频率超限 |
| 500 | INTERNAL_ERROR | 服务器内部错误 |

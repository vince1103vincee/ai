# OpenAPI 3.1.0 規範文件

## 📋 文件信息

**檔案名稱**: `openapi.yaml`  
**格式**: OpenAPI 3.1.0  
**自動生成**: 是  
**修改說明**: 請勿手工編輯！使用 `generate_openapi_spec.py` 重新生成

## ✅ 包含的內容

### 基本信息
```yaml
openapi: 3.1.0
info:
  title: Product Management API
  version: 2.0
  description: API Server for e-commerce product management system
  contact:
    name: API Support
    email: support@example.com
```

### Servers 配置（3 個環境）
```yaml
servers:
  - url: http://localhost:8000/v1
    description: Development server
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server
```

### API Endpoints（15 個）

#### Products
- `GET /products/` - 獲取所有產品 (operationId: list_products)
- `GET /products/{product_id}` - 獲取單個產品 (operationId: get_product_by_id)

#### Users
- `GET /users/` - 獲取所有用戶
- `GET /users/{user_id}` - 獲取單個用戶

#### Orders
- `GET /orders/` - 獲取所有訂單
- `GET /orders/{order_id}` - 獲取訂單詳情
- `GET /orders/user/{user_id}` - 獲取用戶訂單
- `GET /orders/status/{status}` - 按狀態篩選訂單

#### Inventory
- `GET /inventory/` - 獲取庫存
- `GET /inventory/low-stock` - 低庫存產品
- `GET /inventory/{product_id}` - 產品庫存

#### Statistics
- `GET /stats/` - 整體統計
- `GET /stats/revenue` - 收入統計
- `GET /stats/products` - 產品統計
- `GET /stats/inventory` - 庫存統計

## 🔧 如何使用

### 檢視規範
```bash
# 在線檢視
# https://editor.swagger.io
# 上傳 openapi.yaml 文件

# 或使用 ReDoc
# https://redocly.github.io/redoc/?url=file:///path/to/openapi.yaml
```

### 重新生成規範
```bash
source venv/bin/activate
python generate_openapi_spec.py
```

### 驗證規範有效性
```bash
# 使用 OpenAPI 驗證器
npm install -g swagger-cli
swagger-cli validate openapi.yaml

# 或使用 Python
pip install openapi-spec-validator
openapi-spec-validator openapi.yaml
```

## 📈 OpenAPI 版本支援

| 特性 | Swagger 2.0 | OpenAPI 3.0 | OpenAPI 3.1 |
|------|------------|-----------|-----------|
| Servers | ❌ | ✅ | ✅ |
| operationId | ✅ | ✅ | ✅ |
| Tags | ❌ | ✅ | ✅ |
| 最新標準 | ❌ | ✅ | ✅✅ |

## 📝 修改方式

1. **修改 API 端點** → 編輯 `routes/*.py` 中的 docstring
2. **修改 server 配置** → 編輯 `app.py` 中的 Swagger template
3. **重新生成文件** → 執行 `python generate_openapi_spec.py`

## 🔗 相關文件

- `app.py` - Flask 應用配置
- `generate_openapi_spec.py` - 規範生成腳本
- `routes/` - API 端點定義
- `openapi-3.0.yaml` - 完整版本（包含 schema 定義）


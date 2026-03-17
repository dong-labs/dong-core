# dong-core

> 咚咚家族核心库 - 共享基础设施

dong-core 是一个"瘦核心"库，为咚咚家族 CLI 工具集提供通用组件和基础设施。

## 特性

- ✅ **统一 JSON 输出** - `@json_output` 装饰器，标准化所有 CLI 输出格式
- ✅ **统一错误类型** - `ValidationError`、`NotFoundError`、`ConflictError`
- ✅ **日期工具** - `DateUtils` 类，提供常用的日期范围计算
- ✅ **测试工具** - pytest fixtures，简化测试编写

## 安装

```bash
pip install dong-core
```

## 快速开始

### JSON 输出装饰器

```python
from dong import json_output, ValidationError

@json_output
def get_user(user_id: int):
    if user_id <= 0:
        raise ValidationError("user_id", "必须为正整数")
    return {"id": user_id, "name": "Alice"}

# 输出: {"success": true, "data": {"id": 1, "name": "Alice"}}
```

### 错误处理

```python
from dong import ValidationError, NotFoundError, ConflictError

# 输入验证错误
raise ValidationError("email", "邮箱格式不正确")

# 资源不存在
raise NotFoundError("User", 123)

# 冲突错误
raise ConflictError("User", "email", "test@example.com")
```

### 日期工具

```python
from dong import DateUtils

# 获取今天
today = DateUtils.today()

# 获取本周范围
week_start, week_end = DateUtils.this_week()

# 获取本月范围
month_start, month_end = DateUtils.this_month()

# 解析日期字符串
d = DateUtils.parse("2024-01-15")
d = DateUtils.parse("today")
```

## 项目结构

```
dong-core/
├── src/dong/
│   ├── __init__.py
│   ├── output/
│   │   └── formatter.py    # JSON 输出装饰器
│   ├── errors/
│   │   └── exceptions.py   # 统一错误类型
│   ├── dates/
│   │   └── utils.py        # 日期工具
│   └── testing/
│       └── fixtures.py     # 测试 fixtures
├── tests/
└── pyproject.toml
```

## 测试

```bash
# 克隆仓库
git clone https://github.com/xxx/dong-core.git
cd dong-core

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 查看覆盖率
pytest --cov=dong --cov-report=html
```

## 依赖

- Python >= 3.11
- typer >= 0.12.0
- rich >= 13.0.0

## 许可证

MIT License - see [LICENSE](LICENSE) for details.

## 设计理念

dong-core 遵循"瘦核心"原则：

- ✅ **提供**：通用组件（输出格式化、错误类型、日期工具）
- ❌ **不提供**：数据模型、业务逻辑、数据库 schema

每个 CLI 工具保持独立，自主定义数据结构和业务逻辑，dong-core 只提供可复用的基础设施。

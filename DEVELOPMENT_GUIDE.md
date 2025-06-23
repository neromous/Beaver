# Beaver DSL 框架开发指南

## 概述

Beaver DSL 框架采用模块化的三层架构设计，提供了一个可扩展的 Domain Specific Language 执行环境。本指南详细说明了框架的核心架构、设计原则和开发流程。

## 核心架构

### 三层架构模式

Beaver DSL 框架基于 **Function → Wrapper → Register** 的三层架构模式，确保了功能实现的清晰分离和可维护性。

```
┌─────────────────────────────────────────────────────────┐
│                    DSL 层 (注册层)                        │
│  @bf_element 装饰器注册命令，提供 DSL 接口               │
│  命令格式: [':command', arg1, arg2, ...]               │
└─────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────────────────────────────────┐
│                   Wrapper 层 (包装层)                     │
│  对核心功能进行包装，统一返回值格式                        │
│  负责异常处理、结果文本化                                 │
└─────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────────────────────────────────┐
│                  Function 层 (功能层)                     │
│  实现具体的业务逻辑和功能                                 │
│  纯函数实现，便于测试和复用                               │
└─────────────────────────────────────────────────────────┘
```

### 1. Function 层 (功能层)

功能层实现具体的业务逻辑，遵循纯函数设计原则。

**特点：**
- 实现核心业务逻辑
- 无副作用的纯函数
- 直接返回原始数据类型
- 便于单元测试

**示例：**
```python
def file_reader(file_path: Union[str, Path], encoding: str = 'utf-8') -> str:
    """读取文件内容"""
    resolved_path = resolve_file_path(file_path)
    try:
        with open(resolved_path, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {file_path}")
```

### 2. Wrapper 层 (包装层)

包装层对功能层的输出进行统一处理，确保 DSL 命令的输出格式一致。

**职责：**
- 异常处理和错误信息格式化
- 结果文本化处理
- 提供用户友好的输出格式
- 保持接口稳定性

**示例：**
```python
def file_reader_wrapper(file_path: str, encoding: str = 'utf-8') -> str:
    """文件读取的文本化wrapper"""
    try:
        content = file_reader(file_path, encoding)
        return content
    except Exception as e:
        return f"错误: {str(e)}"
```

### 3. Register 层 (DSL注册层)

通过 `@bf_element` 装饰器将功能注册为 DSL 命令，提供统一的调用接口。

**特点：**
- 使用装饰器进行声明式注册
- 包含丰富的元数据信息
- 支持帮助系统自动生成
- 提供统一的命令格式

**示例：**
```python
@bf_element(
    ':file/read',
    description='读取文件内容',
    category='FileIO',
    usage="[':file/read', '文件路径', '编码(可选)']"
)
def file_read_command(file_path: str, encoding: str = 'utf-8'):
    """DSL命令：读取文件"""
    return file_reader_wrapper(file_path, encoding)
```

## 核心组件

### 1. 装饰器系统 (`beaver.core.decorators`)

#### `@bf_element` 装饰器

```python
def bf_element(name: str, **meta: Any) -> Callable:
    """
    注册 DSL 元素的装饰器
    
    Args:
        name: DSL 命令名称，格式: ':category/command'
        **meta: 元数据，包括:
            - description: 命令描述
            - category: 命令分类
            - usage: 使用示例
    """
```

**使用规范：**
- 命令名称采用 `:category/command` 格式
- 必须提供 `description` 和 `category`
- 建议提供 `usage` 示例

### 2. 注册表系统 (`beaver.core.registry`)

#### 全局注册表 `REGISTRY`

```python
REGISTRY: Dict[str, Dict[str, Any]] = {}
```

注册表结构：
```python
{
    ':command/name': {
        'fn': callable,      # 函数对象
        'meta': {           # 元数据
            'description': 'Command description',
            'category': 'Category',
            'usage': 'Usage example'
        }
    }
}
```

#### `RegistryManager` 类

提供注册表的管理功能：
- `register()`: 注册命令
- `get_function()`: 获取函数对象
- `get_metadata()`: 获取元数据
- `list_commands()`: 列出所有命令
- `list_by_category()`: 按分类列出命令

### 3. 调度系统 (`beaver.core.dispatcher`)

#### `dispatch()` 函数

```python
def dispatch(expr: List[Any]) -> Any:
    """
    DSL 表达式调度器
    
    Args:
        expr: DSL 表达式 [command, arg1, arg2, ...]
        
    Returns:
        命令执行结果
    """
```

**调度流程：**
1. 解析 DSL 表达式格式
2. 提取命令名和参数
3. 从注册表获取对应函数
4. 递归解析嵌套表达式
5. 执行函数并返回结果

**深度递归解析：**
```python
# 深度递归解析参数中的嵌套 DSL 表达式
from beaver.core.traversal import postwalk
resolved_args = [postwalk(dispatcher_node, arg) for arg in args]
```

### 4. 遍历系统 (`beaver.core.traversal`)

#### `postwalk()` 函数

提供后序遍历功能，支持复杂数据结构的递归处理：

```python
def postwalk(f: Callable[[Any], Any], data: Any) -> Any:
    """
    后序遍历并转换数据结构
    
    Args:
        f: 转换函数
        data: 嵌套数据结构
        
    Returns:
        转换后的数据结构
    """
```

**支持的数据类型：**
- 基本类型：`str`, `int`, `float`, `bool`
- 集合类型：`list`, `tuple`, `set`, `dict`
- 嵌套结构的递归处理

## Dispatch 机制详解

### 工作原理

Dispatch 机制是 Beaver DSL 的核心执行引擎，负责解析和执行 DSL 表达式。

#### 1. 表达式解析

```python
# DSL 表达式格式
expr = [':command', arg1, arg2, ...]

# 解析过程
cmd, *args = expr  # 提取命令和参数
```

#### 2. 函数查找

```python
fn = RegistryManager.get_function(cmd)
if not fn:
    raise KeyError(f'Command `{cmd}` 未注册')
```

#### 3. 参数预处理

支持嵌套 DSL 表达式的深度解析：

```python
# 递归解析嵌套表达式
resolved_args = [postwalk(dispatcher_node, arg) for arg in args]

# 示例：嵌套表达式
[':file/write', 'output.txt', [':p', 'Hello ', 'World']]
# 内层 [':p', 'Hello ', 'World'] 会先执行，结果作为外层参数
```

#### 4. 函数执行

```python
return fn(*resolved_args)
```

### 执行流程图

```
DSL 表达式输入
      │
      ▼
   格式验证
      │
      ▼
   命令提取
      │
      ▼
   函数查找
      │
      ▼
  参数递归解析
      │
      ▼
   函数执行
      │
      ▼
   结果返回
```

### 嵌套表达式处理

Beaver DSL 支持任意深度的嵌套表达式：

```python
# 简单嵌套
[':file/write', 'result.txt', [':str/upper', 'hello world']]

# 复杂嵌套
[':rows',
  [':md/h1', 'Title'],
  [':p', 'Current time: ', [':sys/time']],
  [':md/list', 
    [':str/upper', 'item 1'],
    [':str/lower', 'ITEM 2']]]
```

**处理机制：**
1. `postwalk` 进行后序遍历
2. `dispatcher_node` 识别并执行 DSL 表达式
3. 内层表达式先执行，结果作为外层参数
4. 最终返回完全解析的结果

## 开发流程

### 1. 新功能开发

#### 步骤 1：实现功能层

```python
# 文件：beaver/func/category/module.py

def core_function(param1: str, param2: int = 0) -> Any:
    """实现核心业务逻辑"""
    # 具体实现
    return result
```

#### 步骤 2：实现包装层

```python
def core_function_wrapper(param1: str, param2: int = 0) -> str:
    """包装函数，处理异常和格式化输出"""
    try:
        result = core_function(param1, param2)
        return f"成功: {result}"
    except Exception as e:
        return f"错误: {str(e)}"
```

#### 步骤 3：注册 DSL 命令

```python
@bf_element(
    ':category/command',
    description='功能描述',
    category='Category',
    usage="[':category/command', 'param1', 'param2']"
)
def command_function(param1: str, param2: int = 0):
    """DSL 命令实现"""
    return core_function_wrapper(param1, param2)
```

### 2. 模块组织

#### 目录结构

```
beaver/
├── core/                    # 核心框架
│   ├── decorators.py       # 装饰器
│   ├── registry.py         # 注册表
│   ├── dispatcher.py       # 调度器
│   ├── traversal.py        # 遍历工具
│   └── help_system.py      # 帮助系统
├── func/                   # 功能层实现
│   ├── io/                 # 文件操作
│   ├── utils/              # 工具函数
│   └── data/               # 数据处理
├── styles/                 # 样式包装层
│   ├── text.py             # 文本样式
│   └── markdown.py         # Markdown 格式
└── nexus/                  # AI 集成
    ├── messages.py         # 消息处理
    └── sync_llm.py         # LLM 同步调用
```

#### 模块导入

```python
# 在模块的 __init__.py 中导入注册函数
from .module import *  # 触发装饰器注册
```

### 3. 测试策略

#### 单元测试

```python
def test_core_function():
    """测试功能层"""
    result = core_function("test", 123)
    assert result == expected_result

def test_wrapper_function():
    """测试包装层"""
    result = core_function_wrapper("test", 123)
    assert "成功:" in result

def test_dsl_command():
    """测试 DSL 命令"""
    result = dispatch([':category/command', 'test', 123])
    assert result == expected_output
```

#### 集成测试

```python
def test_nested_expressions():
    """测试嵌套表达式"""
    expr = [':file/write', 'test.txt', [':p', 'Hello ', 'World']]
    result = dispatch(expr)
    # 验证文件内容和返回值
```

## 扩展指南

### 1. 添加新命令类别

1. 在 `beaver/func/` 下创建新目录
2. 实现功能层、包装层和注册层
3. 在 `__init__.py` 中导入注册函数
4. 更新文档和测试

### 2. 扩展现有功能

1. 在对应模块中添加新函数
2. 遵循三层架构模式
3. 保持接口兼容性
4. 更新相关文档

### 3. 优化性能

1. 缓存注册表查找结果
2. 优化递归遍历算法
3. 减少不必要的字符串操作
4. 使用类型提示优化

## 最佳实践

### 1. 命名规范

- **命令格式**: `:category/command`
- **函数命名**: `{action}_{object}` 格式
- **变量命名**: 使用描述性名称

### 2. 错误处理

- 功能层抛出具体异常
- 包装层统一错误格式
- 提供友好的错误信息

### 3. 文档编写

- 每个函数提供完整的 docstring
- 在 `@bf_element` 中提供使用示例
- 保持文档与实现同步

### 4. 向后兼容

- 谨慎修改现有接口
- 使用版本控制管理变更
- 提供迁移指南

## 附录

### A. 常用装饰器参数

```python
@bf_element(
    ':category/command',           # 必需：命令名称
    description='Command description',  # 必需：功能描述
    category='Category',           # 必需：分类
    usage="[':category/command', 'arg1', 'arg2']",  # 推荐：使用示例
    version='1.0.0',              # 可选：版本信息
    author='Author Name',         # 可选：作者信息
    tags=['tag1', 'tag2']         # 可选：标签
)
```

### B. 支持的参数类型

- **基本类型**: `str`, `int`, `float`, `bool`
- **容器类型**: `list`, `dict`, `tuple`
- **可选参数**: 使用默认值
- **变长参数**: `*args`, `**kwargs`

### C. 调试技巧

1. 使用 `[:help/find ":command"]` 查看命令详情
2. 分层测试：功能层 → 包装层 → DSL 层
3. 使用日志记录调试信息
4. 检查注册表状态：`RegistryManager.list_commands()`

---

*本指南基于 Beaver DSL 框架 v2.0，如有疑问或建议，请提交 Issue 或 Pull Request。* 
# 🚀 跨目录文件操作支持

## 功能概述

成功为 Beaver DSL 框架实现了跨目录文件操作支持，解决了 `bf` 脚本注册到系统执行文件夹后的路径解析问题。

## 📋 核心功能

### ✅ 路径解析器 (`PathResolver`)
- **智能路径解析**: 自动将相对路径转换为绝对路径
- **工作目录检测**: 正确识别命令执行时的当前工作目录
- **脚本目录追踪**: 记录 `bf` 脚本所在目录（用于调试）
- **路径标准化**: 处理 `../` 和 `./` 等相对路径符号

### ✅ 新增 DSL 命令
1. **`:path/cwd`** - 显示当前工作目录
2. **`:path/resolve`** - 将相对路径解析为绝对路径
3. **`:path/info`** - 显示详细的路径信息

### ✅ 文件操作增强
所有文件操作命令现在都支持跨目录使用：
- `:file/read` - 读取文件（支持相对路径）
- `:file/write` - 写入文件（支持相对路径）
- `:file/append` - 追加文件（支持相对路径）
- `:file/exists` - 检查文件存在（支持相对路径）
- `:file/info` - 获取文件信息（支持相对路径）
- `:file/copy` - 复制文件（支持相对路径）
- `:file/move` - 移动文件（支持相对路径）
- `:file/delete` - 删除文件（支持相对路径）

## 🎯 使用场景

### 场景1：将 bf 脚本注册到系统
```bash
# 复制到系统路径
sudo cp /path/to/Beaver/bf /usr/local/bin/bf
sudo chmod +x /usr/local/bin/bf

# 在任意目录使用
cd ~/Documents
bf '[:file/write "note.txt" "Hello World"]'
```

### 场景2：跨目录文件操作
```bash
# 在任意目录创建文件
cd /tmp
bf '[:file/write "report.md" [:rows [:md/h1 "报告"] [:p "内容"]]]'

# 相对路径会正确解析到当前工作目录
bf '[:path/resolve "data/file.txt"]'  # → /tmp/data/file.txt
```

### 场景3：路径调试和验证
```bash
# 查看当前工作目录
bf '[:path/cwd]'

# 查看详细路径信息
bf '[:path/info "config/settings.json"]'

# 解析相对路径
bf '[:path/resolve "../parent/file.txt"]'
```

## 📊 测试验证

### 基础路径解析测试
```bash
# 在 Beaver 目录下
./bf '[:path/cwd]'
# 输出: 当前工作目录: /home/user/Repo/Beaver

./bf '[:path/resolve "test.txt"]'
# 输出: test.txt → /home/user/Repo/Beaver/test.txt
```

### 跨目录操作测试
```bash
# 切换到其他目录
cd /tmp

# 使用绝对路径调用 bf
/home/user/Repo/Beaver/bf '[:path/cwd]'
# 输出: 当前工作目录: /tmp

/home/user/Repo/Beaver/bf '[:file/write "test.txt" "Hello"]'
# 文件会创建在 /tmp/test.txt 而不是脚本目录
```

### 复杂嵌套操作测试
```bash
cd /tmp/project

bf '[:file/write "status.md" [:rows 
  [:md/h1 "项目状态"] 
  [:path/cwd] 
  [:path/info "status.md"] 
  [:md/h2 "完成"]]]'
```

## 🔧 技术实现

### 路径解析器架构
```python
class PathResolver:
    def __init__(self):
        self._cwd = os.getcwd()        # 缓存当前工作目录
        self._script_dir = None        # 脚本所在目录
    
    def resolve_path(self, file_path):
        """将相对路径转换为绝对路径"""
        if os.path.isabs(file_path):
            return file_path
        return os.path.abspath(os.path.join(self._cwd, file_path))
```

### bf 脚本初始化
```python
def init_path_resolver():
    """初始化路径解析器"""
    from beaver.func.io.path_resolver import set_script_directory
    set_script_directory(__file__)
```

### 文件操作集成
```python
def file_writer(file_path, content, encoding='utf-8', append=False):
    """写入文件内容（支持路径解析）"""
    resolved_path = resolve_file_path(file_path)
    # ... 使用 resolved_path 进行文件操作
```

## 📁 新增文件

### 核心模块
- `beaver/func/io/path_resolver.py` - 路径解析器实现
- 修改了 `beaver/func/io/file_ops.py` - 集成路径解析
- 修改了 `bf` 脚本 - 添加路径解析器初始化

### 新增命令
- `:path/cwd` - 显示当前工作目录
- `:path/resolve` - 解析文件路径
- `:path/info` - 显示路径详细信息

## ✅ 兼容性保证

### 向后兼容
- 所有现有的文件操作命令保持相同的使用方式
- 绝对路径的行为保持不变
- 相对路径现在会正确解析到当前工作目录

### 错误处理增强
- 路径解析错误会显示原始路径和解析后路径
- 提供更详细的错误信息帮助调试

## 🚀 未来计划

### 可能的增强功能
1. **环境变量支持**: 支持路径中的环境变量展开
2. **别名路径**: 支持自定义路径别名
3. **相对脚本路径**: 可选的相对于脚本目录的路径解析模式
4. **路径模板**: 支持路径模板和变量替换

### 配置选项
```python
# 未来可能的配置选项
PathResolver.set_mode('cwd')          # 相对于当前工作目录 (默认)
PathResolver.set_mode('script')       # 相对于脚本目录
PathResolver.set_mode('project')      # 相对于项目根目录
```

## 📖 最佳实践

### 推荐用法
1. **使用相对路径**: 让文件操作更灵活和可移植
2. **路径验证**: 使用 `:path/info` 验证路径解析结果
3. **错误处理**: 检查文件操作的错误信息中的解析路径

### 避免的陷阱
1. **路径假设**: 不要假设相对路径相对于脚本目录
2. **硬编码路径**: 避免在 EDN 脚本中使用硬编码的绝对路径
3. **权限问题**: 注意跨目录操作可能遇到的权限问题

## 🎉 总结

这个实现完美解决了 `bf` 脚本注册到系统后的跨目录使用问题：

✅ **智能路径解析** - 相对路径总是相对于当前工作目录  
✅ **完全兼容** - 不影响现有功能的使用方式  
✅ **调试友好** - 提供丰富的路径信息和错误提示  
✅ **性能优化** - 路径解析逻辑高效且缓存友好  
✅ **扩展性强** - 为未来的路径功能扩展奠定基础  

现在用户可以安全地将 `bf` 脚本安装到系统路径中，在任意目录下使用所有文件操作功能！ 
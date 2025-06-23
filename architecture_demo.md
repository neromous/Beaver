# Beaver DSL 三层架构演示
## 1. 功能层示例 (Function Layer)
```python
def file_reader(file_path, encoding='utf-8'):
    # 核心文件读取逻辑
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()
```
## 2. 包装层示例 (Wrapper Layer)
```python
def file_reader_wrapper(file_path, encoding='utf-8'):
    try:
        content = file_reader(file_path, encoding)
        return content
    except Exception as e:
        return f'错误: {str(e)}'
```
## 3. 注册层示例 (Register Layer)
```python
@bf_element(':file/read', description='读取文件内容', category='FileIO')
def file_read_command(file_path, encoding='utf-8'):
    return file_reader_wrapper(file_path, encoding)
```
## 4. Dispatch 机制
当执行 `[:file/read, 'README.md']` 时：
- ["Dispatcher 解析表达式，提取命令 ':file/read' 和参数 'README.md'", '从 REGISTRY 查找对应的函数 file_read_command', '递归解析参数（如果有嵌套表达式）', "调用 file_read_command('README.md')", '返回处理结果']
## 5. 当前系统状态
注册的命令总数: 🔍 搜索 '.' 找到 5 个命令

1. **:file.upload/img** (FileUpload) - 将图片文件转换为OpenAI API格式
2. **:file.upload/video** (FileUpload) - 将视频文件转换为OpenAI API格式
3. **:file.upload/audio** (FileUpload) - 将音频文件转换为OpenAI API格式
4. **:file.upload/batch** (FileUpload) - 批量上传多个媒体文件
5. **:file.upload/get-data** (FileUpload) - 获取上传文件的OpenAI API数据
当前工作目录: 当前工作目录: /home/neromous/Repo/Beaver
README 文件存在: 文件 README.md: 存在
> 这个文档本身就是通过 Beaver DSL 的三层架构生成的！✨
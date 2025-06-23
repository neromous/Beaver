# 🚀 Beaver DSL 命令行工具使用指南

## 概述

你现在可以通过 `./bf` 命令行工具使用强大的 Beaver DSL 系统。该系统提供了丰富的功能模块，包括文件操作、文本处理、AI推理、Markdown生成等。

## 基本语法

```bash
./bf '[DSL表达式]'
```

DSL 表达式使用 EDN 格式，基本结构为 `[命令名, 参数1, 参数2, ...]`

## 🔍 探索和帮助命令

### 查看功能概览
```bash
./bf '[:help]'
```

### 快速查看命令描述
```bash
./bf '[:help ":file/read"]'
```

### 查看命令详细用法
```bash
./bf '[:help/find ":file/read"]'
```

### 搜索相关命令
```bash
./bf '[:help/search "file"]'
./bf '[:help/search "text"]'
./bf '[:help/search "markdown"]'
```

## 📝 实用示例

### 1. 文本处理和格式化

```bash
# 创建段落
./bf '[:p "Hello" " " "World" "!"]'

# 创建多行文本
./bf '[:rows "第一行" "第二行" "第三行"]'

# 文本样式
./bf '[:bold "粗体文本"]'
./bf '[:italic "斜体文本"]'

# 字符串操作
./bf '[:str/upper "hello world"]'
./bf '[:str/replace "Hello World" "World" "Universe"]'
```

### 2. Markdown 生成

```bash
# 标题
./bf '[:md/h1 "主标题"]'
./bf '[:md/h2 "副标题"]'

# 列表
./bf '[:md/list "项目1" "项目2" "项目3"]'

# 链接和图片
./bf '[:md/link "GitHub" "https://github.com"]'
./bf '[:md/image "图片描述" "image.jpg"]'

# 代码块
./bf '[:md/code-block "python" "print(\"Hello World\")"]'
```

### 3. 文件操作

```bash
# 读取文件
./bf '[:file/read "README.md"]'

# 写入文件
./bf '[:file/write "output.txt" "文件内容"]'

# 检查文件是否存在
./bf '[:file/exists "README.md"]'

# 获取文件信息
./bf '[:file/info "README.md"]'

# 创建目录
./bf '[:dir/create "new_folder"]'
```

### 4. 复杂组合示例

#### 文件分析报告生成
```bash
./bf '[:file/write "analysis_results/file_analysis_result.md" 
[:nexus/sync 
 {"provider" "openrouter" "model" "gemini-2.5-flash"}
 [":msg/v2m" [
   [":system" "你是一个资深的技术文档分析专家。请仔细分析用户提供的文件内容，给出专业的评估和建议。"]
   [":user" "请分析以下文件内容，提供详细的分析报告，包括：\n1. 文件类型和主要内容\n2. 技术特点和结构\n3. 关键信息提取\n4. 质量评估和改进建议\n\n文件内容："]
   [":user" [:file/read "README.md"]]
 ]]]]'
```

#### 智能文档生成
```bash
./bf '[:file/write "docs/api_documentation.md"
[:rows
  [:md/h1 "API 文档"]
  [:md/h2 "概述"]
  [:nexus/sync 
   {"provider" "openrouter" "model" "gemini-2.5-flash"}
   [":msg/v2m" [
     [":system" "你是一个API文档专家，请根据提供的代码生成专业的API文档。"]
     [":user" [:p "请为以下代码生成API文档：\n" [:file/read "src/api.py"]]]
   ]]]
  [:md/h2 "使用示例"]
  [:md/code-block "python" "# 示例代码\napi.get_data()"]
]]'
```

#### 批量文件处理
```bash
./bf '[:rows
  [:p "开始处理文件..."]
  [:file/write "processed/summary.md" 
   [:rows
     [:md/h1 "文件处理摘要"]
     [:md/h2 "README 分析"]
     [:file/read "README.md"]
     [:md/h2 "配置文件检查"]
     [:file/exists "config.json"]
   ]]
  [:p "处理完成！"]
]'
```

### 5. AI 推理和消息处理

```bash
# 快速聊天
./bf '[:nexus/quick-chat "请解释什么是函数式编程"]'

# 创建消息格式
./bf '[:msg/v2m [
  [":system" "你是一个编程助手"]
  [":user" "如何学习Python？"]
]]'

# 多媒体消息
./bf '[:user "请分析这个图片" [:file.upload/img "screenshot.png"]]'
```

### 6. 系统功能

```bash
# 截屏
./bf '[:system/screenshot]'

# 延迟截屏
./bf '[:system/screenshot {"delay" 3 "path" "screenshot.png"}]'
```

### 7. EDN 脚本执行

```bash
# 执行 EDN 脚本文件
./bf '[:edn/run "examples/edn_scripts/help_demo.edn"]'

# 加载但不执行 EDN 文件
./bf '[:edn/load "script.edn"]'
```

## 🎯 高级模式：嵌套和组合

Beaver DSL 的强大之处在于可以嵌套和组合命令：

### 条件文档生成
```bash
./bf '[:rows
  [:md/h1 "项目状态报告"]
  [:md/h2 "文件检查"]
  [:p "README 文件: " [:file/exists "README.md"]]
  [:p "配置文件: " [:file/exists "config.json"]]
  [:md/h2 "内容分析"]
  [:bold "README 内容:"]
  [:file/read "README.md"]
]'
```

### 智能内容增强
```bash
./bf '[:file/write "enhanced_content.md"
[:nexus/sync 
 {"provider" "openrouter" "model" "gemini-2.5-flash"}
 [":msg/v2m" [
   [":system" "你是一个内容编辑专家，请优化和增强用户提供的文档内容。"]
   [":user" [:p "请优化以下内容，使其更专业和完整：\n\n" [:file/read "draft.md"]]]
 ]]]]'
```

## 💡 使用技巧

1. **探索功能**: 从 `./bf '[:help]'` 开始，了解所有可用模块
2. **逐步构建**: 先测试简单命令，再组合复杂功能
3. **错误处理**: 如果命令出错，检查语法和参数格式
4. **文件路径**: 使用相对路径，确保文件存在
5. **AI配置**: 确保 API 密钥配置正确

## 🚨 注意事项

- 所有字符串参数都需要用双引号包围
- 文件路径使用正斜杠 `/`
- EDN 格式对语法要求严格，注意括号匹配
- AI 功能需要网络连接和有效的 API 配置

## 🎪 创意应用场景

1. **自动化报告生成**: 结合文件读取和AI分析
2. **文档转换**: 将普通文本转换为格式化的Markdown
3. **内容审核**: 使用AI分析文件内容并生成报告
4. **批量处理**: 组合多个文件操作命令
5. **智能摘要**: 读取长文档并生成摘要
6. **代码文档化**: 自动为代码生成文档

开始使用时，建议先运行 `./bf '[:help]'` 查看所有可用功能，然后根据具体需求选择合适的命令组合！ 
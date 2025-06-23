# 🚀 Beaver DSL 多行输入功能演示

## 功能概述

`bf` 脚本现在支持多种输入方式，包括多行输入、文件输入、管道输入等，让复杂的 DSL 表达式编写更加灵活和方便。

## 📋 支持的输入方式

### 1. 传统单行命令
```bash
./bf '[:p "hello" "world"]'
./bf '[:md/h1 "标题"]'
./bf '[:file/write "test.txt" "Hello World"]'
```

### 2. 交互式多行输入
```bash
./bf
# 然后输入多行DSL，最后按Ctrl+D结束
[:rows
  [:md/h1 "多行标题"]
  [:p "这是多行内容"]
  [:md/list
    ["项目1"
     "项目2"
     "项目3"]]]
```

### 3. Here Document
```bash
./bf << 'EOF'
[:rows
  [:md/h1 "报告标题"]
  [:md/h2 "系统信息"]
  [:p "当前目录: " [:path/cwd]]
  [:p "文件检查: " [:file/exists "README.md"]]
  [:md/h3 "完成"]]
EOF
```

### 4. 从文件读取
```bash
# 创建DSL脚本文件
cat > my_script.edn << 'EOF'
[:file/write "report.md"
  [:rows
    [:md/h1 "自动报告"]
    [:md/h2 "内容"]
    [:p "这是从文件读取的DSL"]]]
EOF

# 执行文件中的DSL
./bf < my_script.edn
```

### 5. 管道输入
```bash
# 简单管道
echo '[:p "Hello " [:str/upper "world"]]' | ./bf

# 复杂管道
cat << 'EOF' | ./bf
[:rows
  [:md/h1 "管道测试"]
  [:p "通过管道传入的命令"]
  [:md/blockquote "测试成功"]]
EOF
```

## 🎯 实际使用场景

### 场景1：生成复杂文档
```bash
./bf << 'EOF'
[:file/write "project_status.md"
  [:rows
    [:md/h1 "项目状态报告"]
    [:md/h2 "基本信息"]
    [:p "生成时间: $(date)"]
    [:p "工作目录: " [:path/cwd]]
    
    [:md/h2 "文件检查"]
    [:md/list
      [[:row "README: " [:file/exists "README.md"]]
       [:row "配置: " [:file/exists "config.json"]]
       [:row "文档: " [:file/exists "docs/"]]]]
    
    [:md/h2 "系统信息"]
    [:help/search "system"]
    
    [:md/h3 "报告完成"]
    [:md/blockquote "所有检查已完成"]]]
EOF
```

### 场景2：批量文件操作
```bash
./bf << 'EOF'
[:rows
  [:file/write "file1.txt" "第一个文件"]
  [:file/write "file2.txt" "第二个文件"] 
  [:file/write "index.md"
    [:rows
      [:md/h1 "文件索引"]
      [:md/list
        [[:row "文件1: " [:file/exists "file1.txt"]]
         [:row "文件2: " [:file/exists "file2.txt"]]]]]]
  [:p "批量操作完成"]]
EOF
```

### 场景3：配置文件处理
```bash
# 从配置模板生成实际配置
./bf << 'EOF'
[:file/write "config.json"
  [:json/object
    {"project_name" "MyProject"
     "version" "1.0.0"
     "paths" {:data_dir [:path/resolve "./data"]
              :log_dir [:path/resolve "./logs"]
              :temp_dir "/tmp/myproject"}
     "features" ["feature1" "feature2" "feature3"]}]]
EOF
```

## 🔧 技术实现细节

### 输入处理逻辑
```python
if len(sys.argv) == 1:
    # 从标准输入读取（支持多行）
    edn_command = sys.stdin.read().strip()
elif len(sys.argv) == 2:
    # 从命令行参数读取（传统方式）
    edn_command = sys.argv[1]
else:
    # 显示帮助信息
    show_help()
```

### 换行符处理
- 保留 DSL 表达式中的原始换行符
- 去除输入的首尾空白字符
- 支持缩进和格式化

### 错误处理
- 优雅处理 `Ctrl+C` 中断
- 处理空输入情况
- 提供清晰的错误提示

## ✅ 功能验证

### 基本多行输入测试
```bash
./bf << 'EOF'
[:p "第一行\n" "第二行\n" "第三行"]
EOF
```

### 复杂嵌套测试
```bash
./bf << 'EOF'
[:rows
  [:md/h1 "嵌套测试"]
  [:file/write "nested_test.md"
    [:rows
      [:md/h2 "内嵌文档"]
      [:p "这是嵌套在文件写入命令中的内容"]
      [:md/list
        ["嵌套列表项1"
         "嵌套列表项2"]]]]
  [:p "嵌套测试完成"]]
EOF
```

### 路径功能测试
```bash
./bf << 'EOF'
[:rows
  [:md/h1 "路径功能测试"]
  [:path/cwd]
  [:path/info "test.txt"]
  [:path/resolve "../parent/file.txt"]]
EOF
```

## 📖 最佳实践

### 推荐的文件组织
```
project/
├── scripts/
│   ├── generate_docs.edn
│   ├── check_status.edn
│   └── setup_project.edn
├── templates/
│   └── report_template.edn
└── output/
```

### EDN 脚本示例
```edn
; generate_docs.edn
[:rows
  [:md/h1 "项目文档"]
  [:md/toc]
  [:file/read "README.md"]
  [:md/h2 "API参考"]
  [:file/read "docs/api.md"]
  [:md/h2 "更新日志"]
  [:file/read "CHANGELOG.md"]]
```

### 执行方式
```bash
# 生成文档
./bf < scripts/generate_docs.edn > docs/complete.md

# 检查状态
./bf < scripts/check_status.edn

# 管道组合
cat templates/report_template.edn | sed 's/{{DATE}}/2024-01-01/' | ./bf
```

## 🎉 优势总结

✅ **灵活输入** - 支持多种输入方式满足不同需求  
✅ **多行支持** - 复杂DSL表达式可以优雅地分行编写  
✅ **文件集成** - 可以将DSL脚本保存为文件重复使用  
✅ **管道友好** - 与Shell管道和重定向完美配合  
✅ **交互体验** - 提供清晰的提示和错误处理  
✅ **向后兼容** - 完全兼容原有的单行命令方式  

现在 `bf` 脚本不仅支持简单的单行命令，还能处理复杂的多行 DSL 表达式，大大提升了 Beaver DSL 框架的实用性和用户体验！ 
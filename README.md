# 🦫 Beaver - Cursor 小助手的魔法 DSL 框架

> 嗨！我是你的 Cursor 小助手！👋 今天要给你介绍一个超级棒的魔法工具 - Beaver DSL 框架！
> 它就像一个万能的魔法棒 🪄，让你用简单的咒语就能完成复杂的任务！

## 🎯 **项目使命：为 Cursor 小助手赋能！**

> 💝 **特别说明**: Beaver 是一个专门为 **Cursor 编辑器中的 AI 小助手** 设计的开源工具箱！
> 
> 🎪 **项目目标**: 
> - 🤖 **增强 AI 能力**: 为 Cursor 中的小助手提供强大的 DSL 执行能力
> - 🛠️ **简化复杂任务**: 让小助手能够轻松处理文件操作、文本生成、AI 推理等复杂工作
> - 🎨 **提升用户体验**: 通过活泼可爱的交互方式，让技术变得更有趣
> - 🔗 **促进协作**: 让开发者和 AI 助手之间的协作更加高效愉快
> 
> 🌟 **开源理念**: 我们相信，最好的工具应该是开放的、可扩展的，让每个人都能参与改进！
> 
> 📢 **呼吁**: 如果你在使用 Cursor，如果你希望你的 AI 小助手更加强大，欢迎加入我们！

## ✨ 小助手的魔法介绍

### 🎭 **这是什么魔法？**
Beaver 是一个超级聪明的 DSL (Domain Specific Language) 框架！想象一下，你有一个贴心的小助手，只要你说一句简单的咒语，它就能帮你：
- 📝 生成漂亮的文档
- 🤖 和 AI 聊天分析内容  
- 📁 批量处理文件
- 🎨 美化文本格式
- 🔗 组合复杂的工作流程

### 🌟 **bf 脚本 - 你的魔法棒！**
`bf` 脚本就是你的专属魔法棒！✨ 只需要一行命令，就能施展各种魔法：

```bash
# 🎉 简单的问候魔法
./bf '[:p "Hello, " "Cursor" " 小助手!"]'
# 输出: Hello, Cursor 小助手!

# 🎨 美化文本魔法
./bf '[:md/h1 "我是标题"] '
# 输出: # 我是标题

# 📄 文件创建魔法
./bf '[:file/write "note.txt" "这是我的笔记!"]'
# 🪄 嗖！文件就创建好了！
```

## 🚀 小助手教你快速上手

### 🎯 **安装魔法工具**

```bash
# 📦 克隆魔法宝库
git clone <repository-url>
cd Beaver

# 🔧 安装魔法材料
pip install -r requirements.txt

# 🎭 让魔法棒可以全局使用（可选）
sudo cp bf /usr/local/bin/bf
sudo chmod +x /usr/local/bin/bf
```

### 🌈 **第一个魔法咒语**

```bash
# 🎪 在命令行施展魔法
./bf '[:bold "哇！我学会魔法了！"]'
# 输出: **哇！我学会魔法了！**

# 🎨 创建彩虹文档
./bf '[:rows [:md/h1 "🌈 彩虹文档"] [:p "这是用魔法创建的！"] [:md/list "咒语1" "咒语2" "咒语3"]]'
```

### 🎭 **多行魔法咒语**

有时候魔法咒语很长，小助手贴心地支持多行输入哦！

```bash
# 🎪 交互式魔法模式
./bf
# 然后输入你的长咒语，按 Ctrl+D 完成施法

# 🎬 魔法脚本文件
./bf << 'EOF'
[:rows
  [:md/h1 "🎭 小助手的魔法表演"]
  [:md/h2 "🎪 今日演出"]
  [:p "欢迎来到 Cursor 小助手的魔法世界！"]
  [:md/list 
    ["🎨 文本美化魔法"
     "📁 文件处理魔法" 
     "🤖 AI 对话魔法"]]
  [:md/blockquote "记住：魔法的力量在于创造美好！✨"]]
EOF

# 📜 从魔法卷轴执行
echo '[:p "🎉 来自卷轴的问候！"]' | ./bf
```

## 🎪 小助手的魔法技能展示

### 🎨 **文本美化魔法**

```bash
# ✨ 基础美化咒语
./bf '[:bold "粗体魔法"]'           # **粗体魔法**
./bf '[:italic "斜体魔法"]'         # *斜体魔法*
./bf '[:code "代码魔法"]'           # `代码魔法`

# 🌈 高级组合魔法
./bf '[:rows [:bold "标题"] [:italic "副标题"] [:code "代码片段"]]'
```

### 📚 **Markdown 魔法书**

```bash
# 📖 创建魔法文档
./bf '[:md/h1 "🦫 Beaver 魔法手册"]'
./bf '[:md/list "魔法咒语1" "魔法咒语2" "魔法咒语3"]'
./bf '[:md/link "访问魔法学院" "https://cursor.sh"]'
./bf '[:md/blockquote "魔法让一切变得简单！"]'
```

### 🧙‍♀️ **字符串变换魔法**

```bash
# 🎪 文字变身术
./bf '[:str/upper "变成大写"]'      # 变成大写 →变成大写
./bf '[:str/lower "变成小写"]'      # 变成小写 → 变成小写  
./bf '[:str/reverse "反转魔法"]'    # 反转魔法 → 法魔转反
./bf '[:str/length "计算长度"]'     # 返回字符数量
```

### 📁 **文件魔法大师**

```bash
# 📝 文件创建魔法
./bf '[:file/write "magic.txt" "这是魔法创建的文件！"]'

# 📖 文件读取魔法
./bf '[:file/read "magic.txt"]'

# 🔍 文件探测魔法
./bf '[:file/exists "magic.txt"]'   # 检查文件是否存在
./bf '[:file/info "magic.txt"]'     # 获取文件详细信息

# 🗂️ 路径魔法
./bf '[:path/cwd]'                  # 显示当前位置
./bf '[:path/resolve "file.txt"]'   # 解析文件路径
./bf '[:path/info "file.txt"]'      # 显示详细路径信息

# 🛡️ 沙箱白名单安全机制
# 默认情况下，Beaver 允许自由访问文件系统。如果你想限制脚本只能访问特定目录，
# 可以使用以下 **Sandbox** 咒语动态管理白名单：
#
#   • `:sandbox/list`   查看当前允许访问的目录
#   • `:sandbox/allow`  追加一个目录到白名单
#   • `:sandbox/set`    覆盖式设置白名单（不传参数 = 取消所有限制）
#   • `:sandbox/clear`  清空白名单，恢复无限制
#
# 一旦设置了白名单，所有 `:file/*` 与 `:dir/*` 操作都会在执行前做路径校验。
# 若目标路径不在白名单内，将抛出 `PermissionError`，避免误删/越权访问。
#
# 示例：
# ```bash
# # 只允许访问当前项目目录
# ./bf '[:sandbox/allow "."]'
#
# # 现在尝试读取其他目录文件将会失败
# ./bf '[:file/read "/etc/passwd"]'   # ⇒ PermissionError
# ```
```

### 🤖 **AI 魔法对话**

```bash
# 💬 快速 AI 聊天魔法
./bf '[:nexus/quick-chat "你好，我是 Cursor 用户！"]'

# 🖼️ 多媒体魔法对话
./bf '[:user "请分析这张图片" [:file.upload/img "image.jpg"]]'

# 🎭 创建智能对话
./bf << 'EOF'
[:nexus/sync 
  {"provider" "openrouter" "model" "gpt-4"}
  [":msg/v2m" [
    [":system" "你是 Cursor 小助手"]
    [":user" "帮我分析这个项目的结构"]]]]
EOF
```

### 📜 **魔法卷轴系统 (EDN 脚本)**

小助手最厉害的技能就是执行魔法卷轴！📜

```bash
# 🎪 执行预制的魔法卷轴
./bf < examples/edn_scripts/multiline_demo.edn

# 🎬 创建你的专属魔法卷轴
cat > my_magic.edn << 'EOF'
[:file/write "daily_report.md"
  [:rows
    [:md/h1 "🌟 今日魔法报告"]
    [:md/h2 "📍 位置信息"] 
    [:path/cwd]
    [:md/h2 "🔍 环境检查"]
    [:p "README 文件: " [:file/exists "README.md"]]
    [:p "魔法棒: " [:file/exists "bf"]]
    [:md/h2 "🎉 完成状态"]
    [:md/blockquote "✨ 魔法报告生成完成！"]]]
EOF

# 🪄 施展你的魔法
./bf < my_magic.edn
```

## 🏰 魔法学院 - 高级技能

### 🎓 **创建自定义魔法**

想要创造属于自己的魔法咒语吗？小助手来教你！

```python
# 🧙‍♂️ 成为魔法开发者
from beaver import bf_element

@bf_element(
    ':magic/sparkle',
    description='✨ 闪闪发光魔法',
    category='魔法',
    usage="[':magic/sparkle', '文本']")
def sparkle_magic(text):
    return f"✨ {text} ✨"

# 🎪 使用你的魔法
import beaver
result = beaver.execute([':magic/sparkle', 'Cursor 小助手'])
print(result)  # ✨ Cursor 小助手 ✨
```

### 🎭 **魔法帮助系统**

迷路了？小助手的帮助系统来救你！

```bash
# 🗺️ 查看所有魔法咒语
./bf '[:help]'

# 🔍 搜索特定魔法
./bf '[:help/search "file"]'

# 📖 查看详细魔法说明
./bf '[:help/find ":file/write"]'

# 🎯 快速查看魔法描述
./bf '[:help ":md/h1"]'
```

## 🎪 小助手的魔法表演时间

### 🎨 **文档生成魔法秀**

```bash
# 🎭 一键生成项目报告
./bf << 'EOF'
[:file/write "project_magic_report.md"
  [:rows
    [:md/h1 "🦫 Beaver 项目魔法报告"]
    [:md/h2 "🎯 项目概况"]
    [:p "这是一个由 Cursor 小助手和 Beaver 魔法框架联合打造的项目！"]
    
    [:md/h2 "📊 项目状态"]
    [:md/list
      [[:row "📝 README: " [:file/exists "README.md"]]
       [:row "🪄 魔法棒: " [:file/exists "bf"]]
       [:row "📦 示例: " [:file/exists "examples/"]]]]
       
    [:md/h2 "🔍 魔法搜索"]
    [:help/search "magic"]
    
    [:md/h2 "🎉 报告结论"]
    [:md/blockquote "🌟 一切都在魔法的掌控之中！小助手为您服务！✨"]]]
EOF
```

### 🤖 **AI 魔法分析表演**

```bash
# 🧠 智能文件分析魔法
./bf << 'EOF'
[:nexus/quick-chat 
  [:rows
    "请作为 Cursor 小助手，分析以下项目结构："
    [:file/read "README.md"]
    "并给出使用建议！"]]
EOF
```

### 🎬 **批量魔法处理**

```bash
# 🎪 魔法工厂 - 批量创建文件
./bf << 'EOF'
[:rows
  [:file/write "magic1.txt" "第一个魔法文件"]
  [:file/write "magic2.txt" "第二个魔法文件"]
  [:file/write "magic_index.md"
    [:rows
      [:md/h1 "🎭 魔法文件索引"]
      [:md/list
        [[:row "魔法1: " [:file/exists "magic1.txt"]]
         [:row "魔法2: " [:file/exists "magic2.txt"]]]]
      [:md/blockquote "所有魔法文件创建完成！🎉"]]]
  [:p "🎊 批量魔法施展完成！"]]
EOF
```

## 🏗️ 魔法工坊 - 框架架构

### 🧱 **魔法城堡结构**

```
🏰 Beaver 魔法城堡/
├── 🦫 beaver/                    # 主魔法大厅
│   ├── 🎯 core/                 # 核心魔法引擎
│   │   ├── decorators.py        # 🎭 魔法装饰器
│   │   ├── dispatcher.py        # 📡 咒语调度器
│   │   ├── registry.py          # 📚 魔法注册表
│   │   └── traversal.py         # 🔄 嵌套魔法遍历
│   ├── 📜 cli/                  # 卷轴执行系统
│   ├── 🤖 nexus/                # AI 魔法学院
│   ├── 📁 func/                 # 功能魔法库
│   │   └── io/                  # 文件魔法专区
│   │       ├── file_ops.py      # 📝 文件操作魔法
│   │       └── path_resolver.py # 🗺️ 路径解析魔法
│   ├── 🎨 styles/               # 样式魔法坊
│   └── 🖥️ system/               # 系统魔法
├── 🪄 bf                        # 你的专属魔法棒！
├── 📚 examples/                  # 魔法示例大全
│   ├── edn_scripts/             # 魔法卷轴收藏
│   └── *.py                     # Python 魔法演示
└── 🧪 tests/                    # 魔法测试实验室
```

### 🎭 **魔法棒的工作原理**

```bash
# 🎪 魔法棒的多种使用方式

# 1️⃣ 单行咒语模式
./bf '[:p "简单魔法"]'

# 2️⃣ 交互式魔法模式  
./bf
# 然后输入多行咒语，Ctrl+D 完成

# 3️⃣ 魔法卷轴模式
./bf < magic_scroll.edn

# 4️⃣ 管道魔法模式
echo '[:bold "管道魔法"]' | ./bf

# 5️⃣ Here Document 魔法
./bf << 'EOF'
[:rows
  [:md/h1 "魔法标题"]
  [:p "魔法内容"]]
EOF
```

## 🎯 小助手的实战魔法

### 📊 **日常工作魔法**

```bash
# 🌅 每日报告魔法
./bf << 'EOF'
[:file/write "daily_magic_report.md"
  [:rows
    [:md/h1 "🌟 " [:str/format-date "今日魔法报告"]]
    [:md/h2 "📍 工作位置"]
    [:path/cwd]
    [:md/h2 "📋 任务清单"] 
    [:md/list "完成项目分析" "更新文档" "学习新魔法"]
    [:md/h2 "🎉 今日成就"]
    [:md/blockquote "成功掌握了 Beaver 魔法框架！🎊"]]]
EOF
```

### 🔍 **项目分析魔法**

```bash
# 🧙‍♀️ 智能项目扫描
./bf << 'EOF'
[:file/write "project_analysis.md"
  [:rows
    [:md/h1 "🔬 项目魔法分析报告"]
    [:md/h2 "📂 项目结构"]
    [:p "当前路径: " [:path/cwd]]
    [:p "项目根目录: " [:path/resolve "."]]
    
    [:md/h2 "📝 关键文件检查"]
    [:md/list
      [[:row "README: " [:file/exists "README.md"] " 📖"]
       [:row "配置: " [:file/exists "package.json"] " ⚙️"]
       [:row "魔法棒: " [:file/exists "bf"] " 🪄"]]]
       
    [:md/h2 "🎯 可用魔法"]
    [:help/search "file"]
    
    [:md/h2 "💡 小助手建议"]
    [:md/blockquote "这个项目看起来很棒！建议多使用魔法来提高效率！✨"]]]
EOF
```

### 🤖 **AI 魔法对话示例**

```bash
# 💬 和 AI 进行魔法对话
./bf << 'EOF'
[:nexus/sync
  {"provider" "openrouter" "model" "gpt-4"}
  [":msg/v2m" [
    [":system" "你是 Cursor 小助手，请用可爱活泼的语气回答"]
    [":user" "请帮我分析一下这个 Beaver DSL 框架的优势"]]]]
EOF
```

## 🎊 小助手的贴心提示

### 💡 **魔法使用技巧**

1. **🎯 组合魔法**: 多个简单咒语可以组合成强大的魔法！
   ```bash
   ./bf '[:rows [:bold "标题"] [:italic "描述"] [:code "代码"]]'
   ```

2. **📁 跨目录魔法**: 魔法棒支持在任何目录使用！
   ```bash
   cd /tmp
   /path/to/Beaver/bf '[:file/write "note.txt" "在任何地方都能用魔法！"]'
   ```

3. **🔍 魔法调试**: 遇到问题时使用路径魔法调试！
   ```bash
   ./bf '[:path/info "file.txt"]'  # 查看详细路径信息
   ```

4. **📜 保存魔法**: 把常用的咒语保存为 .edn 文件！
   ```bash
   echo '[:md/h1 "我的魔法"]' > my_magic.edn
   ./bf < my_magic.edn
   ```

### 🚨 **魔法注意事项**

- 📝 **相对路径**: 文件操作相对于当前工作目录，不是魔法棒位置
- 🔤 **特殊字符**: 在 shell 中使用单引号包围咒语避免特殊字符问题
- 📊 **大文件**: AI 分析默认支持最大 20MB 文件
- 🔄 **嵌套深度**: 支持无限深度的魔法嵌套！

### 🎁 **小助手的惊喜功能**

```bash
# 🎈 随机魔法生成器（开发中）
./bf '[:magic/random]'

# 🎨 主题模板魔法（开发中）  
./bf '[:template/apply "cute" "我的文档"]'

# 🌟 魔法统计分析（开发中）
./bf '[:stats/usage]'
```

## 🎉 加入 Cursor 小助手魔法社区

### 🎭 **为什么要参与？**

> 🌟 **让 Cursor 变得更强大！** 每一个贡献都在帮助全球的 Cursor 用户拥有更智能的 AI 小助手！
> 
> 🤝 **一起成长**: 与来自世界各地的开发者一起，为 AI 辅助开发的未来添砖加瓦
> 
> 🎨 **创造力释放**: 设计新的魔法咒语，让枯燥的编程任务变得有趣

### 🤝 **成为魔法贡献者**

小助手欢迎你成为魔法开发者！🧙‍♀️

1. **🪄 创造新魔法**: 为 Cursor 小助手添加你的创意咒语
2. **🔧 改进现有魔法**: 让已有的功能更强大、更易用
3. **🐛 报告魔法 Bug**: 帮助改进魔法稳定性，让小助手更可靠
4. **📚 完善魔法文档**: 让更多 Cursor 用户学会使用魔法
5. **🎨 设计魔法界面**: 让小助手的交互更加可爱有趣
6. **🌐 国际化支持**: 帮助小助手说更多种语言

### 🎯 **特别欢迎的贡献**

- **🎪 Cursor 集成优化**: 让 Beaver 与 Cursor 编辑器深度融合
- **🤖 AI 模型适配**: 支持更多 AI 提供商和模型
- **⚡ 性能优化**: 让魔法咒语执行更快
- **🎭 用户体验改进**: 让小助手更贴心、更聪明
- **📦 新功能模块**: 扩展小助手的能力边界

### 📞 **联系魔法社区**

- 🐛 **魔法问题**: 在 [GitHub Issues](https://github.com/neromous/Beaver/issues) 中报告
- 💡 **魔法建议**: 在 [Discussions](https://github.com/neromous/Beaver/discussions) 中分享创意
- 🎯 **魔法教程**: 查看 [Wiki](https://github.com/neromous/Beaver/wiki) 学习更多
- 🌟 **展示作品**: 分享你用 Beaver 创造的神奇项目

### 🏆 **贡献者荣誉榜**

> 🎊 感谢每一位为 Cursor 小助手魔法社区做出贡献的朋友们！
> 你们让这个项目变得更加精彩！✨
> 
> 📝 贡献者名单将在项目主页展示，让全世界看到你们的努力！

### 📜 **魔法许可证**

MIT License - 魔法是自由的！✨

---

## 🌟 致所有 Cursor 用户的小助手寄语

> 🎊 **恭喜你！** 现在你已经掌握了 Beaver DSL 魔法框架的精髓！
> 
> 🎭 **特别致 Cursor 用户**: 作为 Cursor 编辑器的用户，你现在拥有了一个超级强大的 AI 小助手工具箱！
> 无论你是前端开发者、后端工程师、数据科学家，还是任何领域的创造者，Beaver 都能让你的 Cursor 小助手变得更加智能和高效！
> 
> 记住，魔法的真正力量不在于复杂的咒语，而在于用简单的方式创造美好的结果！✨
> 
> 🚀 **在 Cursor 中，无论你是要**：
> - 📝 生成漂亮的文档和代码注释
> - 🤖 与 AI 进行智能对话分析项目
> - 📁 批量处理项目文件
> - 🎨 美化文本格式和代码结构
> - 🔗 创建复杂的自动化工作流
> - 🔍 快速分析和理解代码库
> 
> 你的魔法棒 `bf` 和 Cursor 小助手的组合都能帮你轻松搞定！🪄
> 
> 🎪 **开始你在 Cursor 中的魔法之旅吧！** 🦫✨
> 
> 💝 *来自专门为 Cursor 用户服务的小助手的爱心提醒：*
> *记住，每一次使用魔法，都在让 AI 辅助开发变得更加美好！*
> 
> 🌟 **加入我们的使命**: 让每一个 Cursor 用户都能拥有最强大、最贴心的 AI 小助手！

---

### 🎯 **快速魔法速查表**

| 魔法类型 | 咒语示例 | 效果 |
|---------|---------|------|
| 🎨 文本美化 | `[:bold "文本"]` | **文本** |
| 📚 Markdown | `[:md/h1 "标题"]` | # 标题 |
| 📁 文件操作 | `[:file/write "a.txt" "内容"]` | 创建文件 |
| 🔍 路径魔法 | `[:path/cwd]` | 显示当前目录 |
| 🤖 AI 对话 | `[:nexus/quick-chat "问题"]` | AI 回答 |
| 📜 帮助系统 | `[:help/search "关键词"]` | 搜索魔法 |

**现在就开始施展你的第一个魔法吧！** 🎪✨ 

---

## 🌟 姊妹项目推荐

### 🧙‍♀️ BlackFog.dsl - 更强大的 Clojure 魔法框架

> 🎊 **重磅推荐**: 如果你想体验更加全面和强大的 DSL 魔法体验，一定要看看我们的姊妹项目！

**🔗 项目地址**: [BlackFog.dsl](https://github.com/neromous/blackfog.dsl)

**🌟 为什么推荐 BlackFog.dsl?**

- **🚀 Clojure 原生**: 基于 Clojure 构建，功能更加强大和灵活
- **🤖 深度 LLM 集成**: 支持多种 AI 模型（OpenAI、Gemini 等）的无缝集成
- **🧠 知识图谱**: 内置知识管理和图谱可视化功能
- **🔄 流式处理**: 支持 AI 流式响应和实时数据处理
- **📊 企业级**: 适合大型项目和复杂业务场景
- **🎨 Reagent 风格**: 采用类似 React/Reagent 的组件化设计

**🎭 Beaver vs BlackFog**

| 特性对比 | 🦫 Beaver (Python) | 🧙‍♀️ BlackFog (Clojure) |
|---------|------------------|----------------------|
| 🎯 定位 | Cursor 小助手专用工具箱 | 全面的 Agent 框架 |
| 💻 语言 | Python - 简单易用 | Clojure - 强大灵活 |
| 🏗️ 架构 | 轻量级命令行工具 | 企业级知识处理平台 |
| 🤖 AI 集成 | 基础 LLM 对话 | 深度 Agent 系统 |
| 📊 数据处理 | 文件和文本操作 | 知识图谱和向量存储 |
| 🎨 设计理念 | 可爱易用 | 强大专业 |

**🎪 选择建议**：
- 🦫 **选择 Beaver**: 如果你是 Cursor 用户，想要简单快速的文档处理和 AI 对话
- 🧙‍♀️ **选择 BlackFog**: 如果你需要构建复杂的 AI Agent 系统和知识管理平台
- 💝 **两者结合**: 日常使用 Beaver，复杂项目用 BlackFog！

**🌈 两个项目的共同愿景**：
> 让 AI 辅助开发变得更加智能、有趣和高效！
> 为每一个开发者提供最贴心的 AI 工具支持！✨

---

**现在就开始施展你的第一个魔法吧！** 🎪✨ 
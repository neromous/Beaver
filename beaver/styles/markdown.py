"""
Markdown 专用样式功能模块

提供 Markdown 格式的专用 DSL 函数。
"""

from beaver.core.decorators import bf_element

# === Markdown 标题 ========================================================

@bf_element(
    ':md/h1',
    description='一级标题',
    category='Markdown',
    usage="[':md/h1', '标题文本']")
def h1(*args):
    """创建 Markdown 一级标题"""
    title = ''.join(str(arg) for arg in args)
    return f"# {title}"

@bf_element(
    ':md/h2',
    description='二级标题',
    category='Markdown',
    usage="[':md/h2', '标题文本']")
def h2(*args):
    """创建 Markdown 二级标题"""
    title = ''.join(str(arg) for arg in args)
    return f"## {title}"

@bf_element(
    ':md/h3',
    description='三级标题',
    category='Markdown',
    usage="[':md/h3', '标题文本']")
def h3(*args):
    """创建 Markdown 三级标题"""
    title = ''.join(str(arg) for arg in args)
    return f"### {title}"

@bf_element(
    ':md/h4',
    description='四级标题',
    category='Markdown',
    usage="[':md/h4', '标题文本']")
def h4(*args):
    """创建 Markdown 四级标题"""
    title = ''.join(str(arg) for arg in args)
    return f"#### {title}"

@bf_element(
    ':md/h5',
    description='五级标题',
    category='Markdown',
    usage="[':md/h5', '标题文本']")
def h5(*args):
    """创建 Markdown 五级标题"""
    title = ''.join(str(arg) for arg in args)
    return f"##### {title}"

@bf_element(
    ':md/h6',
    description='六级标题',
    category='Markdown',
    usage="[':md/h6', '标题文本']")
def h6(*args):
    """创建 Markdown 六级标题"""
    title = ''.join(str(arg) for arg in args)
    return f"###### {title}"

# === Markdown 列表 ========================================================

@bf_element(
    ':md/list',
    description='无序列表，将多个元素转换为列表项',
    category='Markdown',
    usage="[':md/list', '项目1', '项目2', '项目3']")
def list_items(*args):
    """创建 Markdown 无序列表"""
    items = [f"- {str(arg)}" for arg in args]
    return '\n'.join(items)

@bf_element(
    ':md/ordered-list',
    description='有序列表，将多个元素转换为编号列表项',
    category='Markdown',
    usage="[':md/ordered-list', '项目1', '项目2', '项目3']")
def ordered_list(*args):
    """创建 Markdown 有序列表"""
    items = [f"{i+1}. {str(arg)}" for i, arg in enumerate(args)]
    return '\n'.join(items)

# === Markdown 链接和图片 ==================================================

@bf_element(
    ':md/link',
    description='链接，第一个参数为文本，第二个参数为URL',
    category='Markdown',
    usage="[':md/link', '链接文本', 'https://example.com']")
def link(text, url):
    """创建 Markdown 链接"""
    return f"[{text}]({url})"

@bf_element(
    ':md/image',
    description='图片，第一个参数为alt文本，第二个参数为图片URL',
    category='Markdown',
    usage="[':md/image', 'alt文本', 'image.jpg']")
def image(alt_text, url, title=None):
    """创建 Markdown 图片"""
    if title:
        return f'![{alt_text}]({url} "{title}")'
    return f"![{alt_text}]({url})"

# === Markdown 表格 ========================================================

@bf_element(
    ':md/table-row',
    description='表格行，用竖线分隔各列',
    category='Markdown',
    usage="[':md/table-row', '列1', '列2', '列3']")
def table_row(*args):
    """创建 Markdown 表格行"""
    cells = [str(arg) for arg in args]
    return '| ' + ' | '.join(cells) + ' |'

@bf_element(
    ':md/table-header',
    description='表格标题行，自动添加分隔线',
    category='Markdown',
    usage="[':md/table-header', '标题1', '标题2', '标题3']")
def table_header(*args):
    """创建 Markdown 表格标题行（包含分隔线）"""
    # 注意：这里调用的是内部函数，不是DSL命令
    cells = [str(arg) for arg in args]
    header = '| ' + ' | '.join(cells) + ' |'
    separator = '| ' + ' | '.join(['---'] * len(args)) + ' |'
    return f"{header}\n{separator}"

# === Markdown 代码块 ======================================================

@bf_element(
    ':md/code-block',
    description='代码块，第一个参数为语言，后续为代码内容',
    category='Markdown',
    usage="[':md/code-block', 'python', 'print(\"Hello\")']")
def code_block(language, *args):
    """创建 Markdown 代码块"""
    code = '\n'.join(str(arg) for arg in args)
    return f"```{language}\n{code}\n```"

@bf_element(
    ':md/blockquote',
    description='多行引用块',
    category='Markdown',
    usage="[':md/blockquote', '引用行1', '引用行2']")
def blockquote(*args):
    """创建 Markdown 多行引用块"""
    lines = [f"> {str(arg)}" for arg in args]
    return '\n'.join(lines)

# === Markdown 其他元素 ====================================================

@bf_element(
    ':md/hr',
    description='水平分隔线',
    category='Markdown',
    usage="[':md/hr']")
def horizontal_rule():
    """创建 Markdown 水平分隔线"""
    return "---"

@bf_element(
    ':md/strikethrough',
    description='删除线文本',
    category='Markdown',
    usage="[':md/strikethrough', '被删除的文本']")
def strikethrough(*args):
    """创建删除线文本（GitHub Flavored Markdown）"""
    text = ''.join(str(arg) for arg in args)
    return f"~~{text}~~"

@bf_element(
    ':md/task-list',
    description='任务列表，参数为 (完成状态, 任务描述) 的元组',
    category='Markdown',
    usage="[':md/task-list', [True, '已完成任务'], [False, '未完成任务']]")
def task_list(*tasks):
    """创建 Markdown 任务列表"""
    items = []
    for task in tasks:
        if isinstance(task, (list, tuple)) and len(task) >= 2:
            completed, description = task[0], task[1]
            checkbox = "[x]" if completed else "[ ]"
            items.append(f"- {checkbox} {description}")
        else:
            # 如果格式不正确，将任务视为未完成
            items.append(f"- [ ] {str(task)}")
    return '\n'.join(items) 
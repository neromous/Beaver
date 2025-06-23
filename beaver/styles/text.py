# beaver/styles/text.py
"""
文本样式功能模块

提供各种文本格式化和样式化的 DSL 函数。
"""

from beaver.core.decorators import bf_element

# === 基础文本样式 ============================================================

@bf_element(
    ':p',
    description='段落，拼接段落中的字符串',
    category='Text',
    usage="[':p', '段落中的字符串']")
def p(*args):
    """创建段落，将所有参数连接成字符串"""
    return ''.join(str(arg) for arg in args)

@bf_element(
    ':row',
    description='行，将多个元素用空格连接成一行',
    category='Text',
    usage="[':row', '元素1', '元素2', '元素3']")
def row(*args):
    """创建行，用空格连接多个元素"""
    return ' '.join(str(arg) for arg in args)

@bf_element(
    ':rows',
    description='多行，将多个元素用换行符连接',
    category='Text',
    usage="[':rows', '行1', '行2', '行3']")
def rows(*args):
    """创建多行，用换行符连接多个元素"""
    return '\n'.join(str(arg) for arg in args)

# === 格式化文本 ============================================================

@bf_element(
    ':bold',
    description='粗体文本',
    category='Text',
    usage="[':bold', '文本内容']")
def bold(*args):
    """创建粗体文本 (Markdown格式)"""
    text = ''.join(str(arg) for arg in args)
    return f"**{text}**"

@bf_element(
    ':italic',
    description='斜体文本',
    category='Text',
    usage="[':italic', '文本内容']")
def italic(*args):
    """创建斜体文本 (Markdown格式)"""
    text = ''.join(str(arg) for arg in args)
    return f"*{text}*"

@bf_element(
    ':code',
    description='行内代码',
    category='Text',
    usage="[':code', '代码内容']")
def code(*args):
    """创建行内代码 (Markdown格式)"""
    text = ''.join(str(arg) for arg in args)
    return f"`{text}`"

@bf_element(
    ':quote',
    description='引用块',
    category='Text',
    usage="[':quote', '引用内容']")
def quote(*args):
    """创建引用块 (Markdown格式)"""
    text = ''.join(str(arg) for arg in args)
    return f"> {text}"

# === 工具函数 ============================================================

@bf_element(
    ':join',
    description='用指定分隔符连接多个元素',
    category='Text',
    usage="[':join', ',', '元素1', '元素2', '元素3']")
def join(separator, *args):
    """用指定分隔符连接多个元素"""
    return separator.join(str(arg) for arg in args)

@bf_element(
    ':indent',
    description='缩进文本，第一个参数为缩进级别，后续为文本内容',
    category='Text',
    usage="[':indent', 2, '缩进的文本']")
def indent(level, *args):
    """缩进文本，支持多级缩进"""
    text = ''.join(str(arg) for arg in args)
    indent_str = '  ' * int(level)  # 每级缩进2个空格
    return f"{indent_str}{text}"

@bf_element(
    ':br',
    description='换行符',
    category='Text',
    usage="[':br']")
def br():
    """返回换行符"""
    return '\n'

@bf_element(
    ':sep',
    description='分隔符，默认为破折号',
    category='Text',
    usage="[':sep'] 或 [':sep', '自定义分隔符']")
def sep(separator='---'):
    """返回分隔符，默认为破折号"""
    return separator 
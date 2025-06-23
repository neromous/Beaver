"""
字符串操作功能模块

提供各种字符串处理的 DSL 函数。
"""

from beaver.core.decorators import bf_element


@bf_element(
    ':str/upper',
    description='将文本转换为大写',
    category='StringOps',
    usage="[':str/upper', '文本内容']")
def upper_case(*args):
    """将文本转换为大写"""
    text = ''.join(str(arg) for arg in args)
    return text.upper()


@bf_element(
    ':str/lower',
    description='将文本转换为小写',
    category='StringOps',
    usage="[':str/lower', '文本内容']")
def lower_case(*args):
    """将文本转换为小写"""
    text = ''.join(str(arg) for arg in args)
    return text.lower()


@bf_element(
    ':str/title',
    description='将文本转换为标题格式（首字母大写）',
    category='StringOps',
    usage="[':str/title', '文本内容']")
def title_case(*args):
    """将文本转换为标题格式"""
    text = ''.join(str(arg) for arg in args)
    return text.title()


@bf_element(
    ':str/reverse',
    description='反转字符串',
    category='StringOps',
    usage="[':str/reverse', '文本内容']")
def reverse_string(*args):
    """反转字符串"""
    text = ''.join(str(arg) for arg in args)
    return text[::-1]


@bf_element(
    ':str/length',
    description='获取字符串长度',
    category='StringOps',
    usage="[':str/length', '文本内容']")
def string_length(*args):
    """获取字符串长度"""
    text = ''.join(str(arg) for arg in args)
    return len(text)


@bf_element(
    ':str/trim',
    description='去除字符串两端空白',
    category='StringOps',
    usage="[':str/trim', '  文本内容  ']")
def trim_string(*args):
    """去除字符串两端空白"""
    text = ''.join(str(arg) for arg in args)
    return text.strip()


@bf_element(
    ':str/replace',
    description='替换字符串中的内容',
    category='StringOps',
    usage="[':str/replace', '原文本', '被替换内容', '新内容']")
def replace_string(text, old, new):
    """替换字符串中的内容"""
    return str(text).replace(str(old), str(new))


@bf_element(
    ':str/split',
    description='分割字符串',
    category='StringOps',
    usage="[':str/split', '文本内容', '分隔符']")
def split_string(text, separator=' '):
    """分割字符串"""
    return str(text).split(str(separator))


@bf_element(
    ':str/contains',
    description='检查字符串是否包含子串',
    category='StringOps',
    usage="[':str/contains', '文本内容', '子串']")
def contains_substring(text, substring):
    """检查字符串是否包含子串"""
    return str(substring) in str(text)


@bf_element(
    ':str/starts-with',
    description='检查字符串是否以指定内容开头',
    category='StringOps',
    usage="[':str/starts-with', '文本内容', '前缀']")
def starts_with(text, prefix):
    """检查字符串是否以指定内容开头"""
    return str(text).startswith(str(prefix))


@bf_element(
    ':str/ends-with',
    description='检查字符串是否以指定内容结尾',
    category='StringOps',
    usage="[':str/ends-with', '文本内容', '后缀']")
def ends_with(text, suffix):
    """检查字符串是否以指定内容结尾"""
    return str(text).endswith(str(suffix)) 
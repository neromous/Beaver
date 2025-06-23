#!/usr/bin/env python3
# examples/basic_usage.py - Beaver 基本用法示例

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import beaver
import beaver.func.utils.string_ops  # 导入字符串操作模块

def demo_basic_text():
    """演示基本文本操作"""
    print("=== 基本文本操作演示 ===")
    
    # 段落拼接
    result = beaver.execute([':p', 'Hello', ' ', 'World', '!'])
    print(f"段落: '{result}'")
    
    # 行拼接（空格分隔）
    result = beaver.execute([':row', '苹果', '香蕉', '橙子'])
    print(f"行: '{result}'")
    
    # 多行拼接
    result = beaver.execute([':rows', '第一行', '第二行', '第三行'])
    print(f"多行:\n{result}")

def demo_markdown():
    """演示 Markdown 样式"""
    print("\n=== Markdown 样式演示 ===")
    
    # 标题
    h1 = beaver.execute([':md/h1', 'Beaver 文档'])
    h2 = beaver.execute([':md/h2', '功能介绍'])
    
    # 格式化文本
    bold_text = beaver.execute([':bold', '重要内容'])
    italic_text = beaver.execute([':italic', '强调内容'])
    code_text = beaver.execute([':code', 'beaver.execute()'])
    
    # 列表
    features = beaver.execute([':md/list', 
                              '简洁的 DSL 语法',
                              '模块化设计',
                              '嵌套表达式支持'])
    
    # 组合输出
    markdown_doc = beaver.execute([':rows',
                                  h1,
                                  '',
                                  h2,
                                  '',
                                  '这是一个演示文档，展示了以下特性：',
                                  '',
                                  features,
                                  '',
                                  beaver.execute([':p', '包含 ', bold_text, '、', italic_text, ' 和 ', code_text]),
                                  ])
    
    print(markdown_doc)

def demo_string_operations():
    """演示字符串操作"""
    print("\n=== 字符串操作演示 ===")
    
    original = "Hello World"
    print(f"原始字符串: '{original}'")
    
    # 大小写转换
    upper = beaver.execute([':str/upper', original])
    lower = beaver.execute([':str/lower', original])
    title = beaver.execute([':str/title', original])
    
    print(f"大写: '{upper}'")
    print(f"小写: '{lower}'")
    print(f"标题格式: '{title}'")
    
    # 字符串信息
    length = beaver.execute([':str/length', original])
    reversed_str = beaver.execute([':str/reverse', original])
    
    print(f"长度: {length}")
    print(f"反转: '{reversed_str}'")
    
    # 字符串操作
    replaced = beaver.execute([':str/replace', original, 'World', 'Beaver'])
    print(f"替换: '{replaced}'")

def demo_nested_expressions():
    """演示嵌套表达式"""
    print("\n=== 嵌套表达式演示 ===")
    
    # 创建一个复杂的文档结构
    document = [
        ':rows',
        [':md/h1', 'Beaver 项目报告'],
        [':md/hr'],
        '',
        [':md/h2', '项目概述'],
        [':p', 'Beaver 是一个基于 DSL 的可扩展功能框架。'],
        '',
        [':md/h2', '主要特性'],
        [':md/list',
         [':row', [':bold', '核心特性:'], '简洁的 DSL 语法'],
         [':row', [':bold', '架构特性:'], '模块化设计'],
         [':row', [':bold', '使用特性:'], '嵌套表达式支持']],
        '',
        [':md/h2', '技术栈'],
        [':md/code-block', 'python', 'import beaver', 'result = beaver.execute([\':p\', \'Hello World\'])'],
        '',
        [':md/h2', '项目状态'],
        [':md/task-list',
         [True, '基础框架完成'],
         [True, '样式模块实现'],
         [False, '扩展系统开发'],
         [False, '文档完善']],
        '',
        [':md/blockquote', '注意：这是一个演示文档，展示了 Beaver 的嵌套 DSL 能力。']
    ]
    
    result = beaver.process_nested(document)
    print(result)

def demo_custom_function():
    """演示自定义函数注册"""
    print("\n=== 自定义函数演示 ===")
    
    # 注册一个自定义函数
    @beaver.bf_element(
        ':demo/greet',
        description='生成个性化问候语',
        category='Demo',
        usage="[':demo/greet', '姓名', '时间']")
    def greet(name, time_of_day=''):
        if time_of_day:
            return f"{time_of_day}好，{name}！欢迎使用 Beaver！"
        return f"你好，{name}！欢迎使用 Beaver！"
    
    # 使用自定义函数
    greeting1 = beaver.execute([':demo/greet', 'Alice'])
    greeting2 = beaver.execute([':demo/greet', 'Bob', '早上'])
    
    print(f"问候语1: {greeting1}")
    print(f"问候语2: {greeting2}")
    
    # 在嵌套表达式中使用
    nested_greeting = beaver.process_nested([
        ':rows',
        [':md/h3', '问候语示例'],
        [':md/list', greeting1, greeting2]
    ])
    
    print(f"嵌套问候:\n{nested_greeting}")

def show_available_commands():
    """显示可用命令"""
    print("\n=== 可用命令列表 ===")
    
    # 按类别显示命令
    categories = ['Text', 'Markdown', 'StringOps']
    
    for category in categories:
        commands = beaver.list_commands_by_category(category)
        if commands:
            print(f"\n{category} 类别:")
            for cmd, meta in commands.items():
                print(f"  {cmd}: {meta['description']}")

def main():
    """主演示函数"""
    print("Beaver DSL 框架演示")
    print("=" * 50)
    
    demo_basic_text()
    demo_markdown()
    demo_string_operations()
    demo_nested_expressions()
    demo_custom_function()
    show_available_commands()
    
    print(f"\n项目版本: {beaver.get_version()}")
    print("演示完成！")

if __name__ == '__main__':
    main() 
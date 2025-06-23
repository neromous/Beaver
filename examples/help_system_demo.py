#!/usr/bin/env python3
"""
帮助系统演示

展示新增的 :help 和 :help/search 功能的使用方法
"""

import beaver

def demo_help_overview():
    """演示帮助概览功能"""
    print("🚀 === :help 功能概览演示 ===\n")
    
    result = beaver.dispatch([':help'])
    print(result)
    print("\n" + "="*50 + "\n")


def demo_specific_help():
    """演示特定命令帮助"""
    print("📖 === :help 特定命令演示 ===\n")
    
    # 查看文件读取命令的帮助
    result = beaver.dispatch([':help', ':file/read'])
    print("查询 ':file/read' 命令:")
    print(result)
    print()
    
    # 查看不存在的命令
    result = beaver.dispatch([':help', ':nonexistent'])
    print("查询不存在的命令:")
    print(result)
    print("\n" + "="*50 + "\n")


def demo_search_functionality():
    """演示搜索功能"""
    print("🔍 === :help/search 搜索功能演示 ===\n")
    
    # 搜索文件相关命令
    print("搜索 'file' 相关命令:")
    result = beaver.dispatch([':help/search', 'file'])
    print(result[:800] + "..." if len(result) > 800 else result)
    print()
    
    # 搜索文本相关命令
    print("搜索 'markdown' 相关命令:")
    result = beaver.dispatch([':help/search', 'markdown'])
    print(result[:600] + "..." if len(result) > 600 else result)
    print()
    
    # 空搜索测试
    print("空搜索测试:")
    result = beaver.dispatch([':help/search', ''])
    print(result)
    print("\n" + "="*50 + "\n")


def demo_integration_example():
    """演示与其他功能的集成使用"""
    print("🔧 === 集成使用示例 ===\n")
    
    # 使用嵌套处理：搜索然后格式化输出
    print("使用嵌套处理搜索系统命令:")
    from beaver import process_nested
    
    # 创建一个包含搜索和格式化的嵌套结构
    nested_expr = [
        ':rows',
        [':bold', '搜索结果：'],
        [':help/search', 'system'],
        [':br'],
        [':italic', '搜索完成']
    ]
    
    result = process_nested(nested_expr)
    print(result[:500] + "..." if len(result) > 500 else result)
    print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    print("🎯 Beaver Help System Demo")
    print("演示新增的 :help 和 :help/search 功能\n")
    
    try:
        demo_help_overview()
        demo_specific_help()
        demo_search_functionality()
        demo_integration_example()
        
        print("✅ 所有演示完成！")
        print("\n💡 提示：")
        print("- 使用 [:help] 查看所有可用命令")
        print("- 使用 [:help, '命令名'] 查看特定命令详情")
        print("- 使用 [:help/search, '关键词'] 搜索相关命令")
        
    except Exception as e:
        print(f"❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc() 
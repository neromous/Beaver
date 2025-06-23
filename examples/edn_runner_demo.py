#!/usr/bin/env python3
"""
Beaver DSL EDN 文件执行器演示

展示如何使用 EDN 文件执行功能：
1. 创建示例 EDN 文件
2. 通过 DSL 命令执行
3. 通过命令行工具执行
4. 批量执行多个脚本
"""

import os
import sys
from pathlib import Path
import tempfile

# 添加 beaver 到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import beaver
from beaver.cli.edn_runner import run_edn_file, create_sample_edn_files


def demo_create_samples():
    """演示创建示例文件"""
    print("=" * 60)
    print("🎯 演示1: 创建示例 EDN 文件")
    print("=" * 60)
    
    # 使用 DSL 命令创建示例
    result = beaver.execute([":edn/create-samples"])
    print(result)
    
    return True


def demo_dsl_commands():
    """演示 DSL 命令方式执行 EDN 文件"""
    print("\n" + "=" * 60)
    print("🎯 演示2: 使用 DSL 命令执行 EDN 文件")
    print("=" * 60)
    
    # 确保示例文件存在
    samples_dir = Path("examples/edn_scripts")
    if not samples_dir.exists():
        create_sample_edn_files()
    
    # 测试加载文件（不执行）
    print("\n📋 测试1: 加载 EDN 文件")
    result = beaver.execute([":edn/load", "examples/edn_scripts/simple_text.edn"])
    print(result)
    
    # 测试执行简单文本
    print("\n📋 测试2: 执行简单文本操作")
    result = beaver.execute([":edn/run", "examples/edn_scripts/simple_text.edn"])
    print(result)
    
    # 测试执行多命令
    print("\n📋 测试3: 执行多命令脚本")
    result = beaver.execute([":edn/run", "examples/edn_scripts/multiple_commands.edn"])
    print(result)
    
    # 测试执行消息处理
    print("\n📋 测试4: 执行消息处理脚本")
    result = beaver.execute([":edn/run", "examples/edn_scripts/message_processing.edn"])
    print(result)
    
    return True


def demo_programmatic_execution():
    """演示编程方式执行 EDN 文件"""
    print("\n" + "=" * 60)
    print("🎯 演示3: 编程方式执行 EDN 文件")
    print("=" * 60)
    
    # 测试各种示例文件
    samples_dir = Path("examples/edn_scripts")
    sample_files = list(samples_dir.glob("*.edn"))
    
    for i, sample_file in enumerate(sample_files, 1):
        print(f"\n📋 测试 {i}: 执行 {sample_file.name}")
        
        try:
            result = run_edn_file(str(sample_file), verbose=True)
            
            if result["load_success"] and result["execution"]["success"]:
                print(f"✅ 执行成功，耗时: {result['total_time']}s")
            else:
                error_msg = result.get('error') or result.get('execution', {}).get('error', '未知错误')
                print(f"❌ 执行失败: {error_msg}")
                
        except Exception as e:
            print(f"❌ 程序异常: {e}")
    
    return True


def demo_custom_edn_scripts():
    """演示自定义 EDN 脚本执行"""
    print("\n" + "=" * 60)
    print("🎯 演示4: 自定义 EDN 脚本执行")
    print("=" * 60)
    
    # 创建临时 EDN 脚本
    with tempfile.NamedTemporaryFile(mode='w', suffix='.edn', delete=False, encoding='utf-8') as f:
        # 复杂的多媒体处理示例（注释掉实际文件操作）
        edn_content = '''[
  [:p "开始自定义脚本演示"]
  [:str/upper "hello beaver dsl"]
  [:str/lower "WORLD"]
  [:md/h2 "自定义标题"]
  [:md/list ["功能1" "功能2" "功能3"]]
  [:user "这是一个用户消息"]
  [:system "这是一个系统消息"]
  [:p "脚本执行完成"]
]'''
        f.write(edn_content)
        temp_edn_path = f.name
    
    try:
        print(f"📄 临时脚本: {temp_edn_path}")
        
        # 1. 先加载查看内容
        print("\n📋 步骤1: 加载脚本内容")
        result = beaver.execute([":edn/load", temp_edn_path])
        print(result)
        
        # 2. 执行脚本
        print("\n📋 步骤2: 执行脚本")
        result = beaver.execute([":edn/run", temp_edn_path])
        print(result)
        
        # 3. 编程方式执行并保存结果
        print("\n📋 步骤3: 编程方式执行并保存结果")
        output_file = temp_edn_path.replace('.edn', '_result.json')
        result = run_edn_file(temp_edn_path, output_file=output_file, verbose=True)
        
        if os.path.exists(output_file):
            print(f"💾 结果已保存到: {output_file}")
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_edn_path):
            os.unlink(temp_edn_path)
        output_file = temp_edn_path.replace('.edn', '_result.json')
        if os.path.exists(output_file):
            os.unlink(output_file)
    
    return True


def demo_error_handling():
    """演示错误处理"""
    print("\n" + "=" * 60)
    print("🎯 演示5: 错误处理测试")
    print("=" * 60)
    
    # 测试不存在的文件
    print("\n📋 测试1: 不存在的文件")
    result = beaver.execute([":edn/run", "nonexistent.edn"])
    print(result)
    
    # 测试无效的 EDN 内容
    print("\n📋 测试2: 无效的 EDN 内容")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.edn', delete=False, encoding='utf-8') as f:
        f.write('invalid edn content [[[')
        invalid_edn_path = f.name
    
    try:
        result = beaver.execute([":edn/run", invalid_edn_path])
        print(result)
    finally:
        os.unlink(invalid_edn_path)
    
    # 测试空文件
    print("\n📋 测试3: 空文件")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.edn', delete=False, encoding='utf-8') as f:
        f.write('')
        empty_edn_path = f.name
    
    try:
        result = beaver.execute([":edn/run", empty_edn_path])
        print(result)
    finally:
        os.unlink(empty_edn_path)
    
    return True


def demo_command_help():
    """演示命令帮助信息"""
    print("\n" + "=" * 60)
    print("🎯 演示6: EDN 命令帮助信息")
    print("=" * 60)
    
    # 查看 EDN 相关命令
    print("📋 EDN 文件执行相关命令:")
    edn_commands = [cmd for cmd in beaver.list_all_commands() if 'edn' in cmd]
    for cmd in edn_commands:
        print(f"  🔧 {cmd}")
    
    # 查看帮助信息
    print("\n📋 命令详细帮助:")
    help_result = beaver.execute([":help", "edn"])
    print(help_result)
    
    return True


def main():
    """主演示函数"""
    print("🦫 Beaver DSL EDN 文件执行器功能演示")
    print("此演示展示了 EDN 脚本文件的加载和执行功能")
    
    # 运行所有演示
    demos = [
        demo_create_samples,
        demo_dsl_commands,
        demo_programmatic_execution,
        demo_custom_edn_scripts,
        demo_error_handling,
        demo_command_help
    ]
    
    success_count = 0
    for demo in demos:
        try:
            if demo():
                success_count += 1
        except Exception as e:
            print(f"❌ 演示失败: {e}")
    
    print("\n" + "=" * 60)
    print("📊 演示总结")
    print("=" * 60)
    print(f"✅ 成功演示: {success_count}/{len(demos)}")
    print(f"📋 演示的功能:")
    print(f"  🔧 EDN 文件创建和加载")
    print(f"  🚀 DSL 命令方式执行")
    print(f"  💻 编程方式执行")
    print(f"  📝 自定义脚本执行")
    print(f"  🛡️  错误处理机制")
    print(f"  📚 命令帮助系统")
    
    print(f"\n💡 使用提示:")
    print(f"  命令行方式: python -m beaver.cli.edn_runner script.edn")
    print(f"  DSL 方式: beaver.execute([':edn/run', 'script.edn'])")
    print(f"  编程方式: from beaver.cli import run_edn_file")
    
    return success_count == len(demos)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
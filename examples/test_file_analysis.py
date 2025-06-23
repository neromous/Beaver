#!/usr/bin/env python3
"""
Beaver DSL 文件分析功能演示

展示如何使用 EDN 脚本进行本地文件的 AI 分析
"""

import sys
from pathlib import Path

# 添加 beaver 到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import beaver

def demo_file_analysis():
    """演示文件分析功能"""
    
    print("🦫 Beaver DSL 文件分析功能演示")
    print("=" * 60)
    
    # 1. 基础文件分析
    print("\n🎯 演示1: 基础文件分析")
    print("-" * 40)
    result = beaver.execute([":edn/run", "examples/edn_scripts/file_analysis_llm.edn"])
    print("✅ 基础文件分析完成")
    
    # 2. 通用文件分析
    print("\n🎯 演示2: 通用智能文件分析")
    print("-" * 40)
    result = beaver.execute([":edn/run", "examples/edn_scripts/analyze_any_file.edn"])
    print("✅ 通用文件分析完成")
    
    # 3. 智能文件分析
    print("\n🎯 演示3: 智能自适应分析")  
    print("-" * 40)
    result = beaver.execute([":edn/run", "examples/edn_scripts/smart_file_analyzer.edn"])
    print("✅ 智能分析完成")
    
    # 4. 代码文件分析
    print("\n🎯 演示4: 专业代码分析")
    print("-" * 40)
    result = beaver.execute([":edn/run", "examples/edn_scripts/analyze_code_file.edn"])
    print("✅ 代码分析完成")
    
    # 5. 展示生成的文件
    print("\n📁 生成的分析报告:")
    print("-" * 40)
    
    analysis_dir = Path("analysis_results")
    if analysis_dir.exists():
        for file in analysis_dir.glob("*"):
            file_size = file.stat().st_size
            print(f"  📄 {file.name} ({file_size} bytes)")
    
    print(f"\n💡 使用提示:")
    print(f"  1. 修改 EDN 脚本中的文件路径可分析其他文件")
    print(f"  2. 支持分析 Markdown、Python、JSON、文本等各种文件")
    print(f"  3. AI 会根据文件类型自动选择最佳分析策略")
    print(f"  4. 生成多种格式的分析报告：详细分析、结构化摘要、关键词等")
    
    return True

def demo_dsl_commands():
    """演示 DSL 命令"""
    
    print("\n🔧 EDN 文件执行相关命令:")
    print("-" * 40)
    
    # 创建示例文件
    result = beaver.execute([":edn/create-samples"])
    print(result)
    
    # 加载文件信息
    print("\n📋 文件加载示例:")
    result = beaver.execute([":edn/load", "examples/edn_scripts/simple_text.edn"])
    print(result)
    
    return True

def main():
    """主函数"""
    
    try:
        print("🚀 开始演示...")
        
        # 确保分析结果目录存在
        Path("analysis_results").mkdir(exist_ok=True)
        
        # 演示文件分析功能
        demo_file_analysis()
        
        # 演示 DSL 命令
        demo_dsl_commands()
        
        print("\n✅ 所有演示完成!")
        print("\n📊 总结:")
        print("  🎯 展示了4种不同的文件分析策略")
        print("  🤖 集成了 AI 深度分析能力")
        print("  📝 生成了多种格式的分析报告")
        print("  🔧 演示了 EDN 脚本的强大功能")
        
        return True
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
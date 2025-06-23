#!/usr/bin/env python3
"""
Beaver DSL EDN 文件执行器

支持加载和执行 EDN 格式的 DSL 脚本文件
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import argparse
import time


def load_edn_file(file_path: str) -> Any:
    """
    加载 EDN 文件并解析
    
    参数:
        file_path: EDN 文件路径
    
    返回:
        Any: 解析后的 EDN 数据结构
    
    异常:
        FileNotFoundError: 文件不存在
        ValueError: EDN 解析失败
    """
    try:
        from beaver.inference.action_stream import parse_edn
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"EDN 文件不存在: {file_path}")
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        if not content:
            raise ValueError("EDN 文件为空")
        
        # 解析 EDN 内容
        parsed = parse_edn(content)
        return parsed
        
    except ImportError:
        raise ImportError("需要安装 edn-format 库: pip install edn-format")
    except Exception as e:
        raise ValueError(f"EDN 文件解析失败: {e}")


def execute_edn_data(edn_data: Any, verbose: bool = True) -> Dict[str, Any]:
    """
    执行 EDN 数据结构
    
    参数:
        edn_data: 解析后的 EDN 数据
        verbose: 是否显示详细执行信息
    
    返回:
        Dict: 执行结果统计
    """
    try:
        from beaver.inference.action_stream import edn_to_python
        from beaver import execute
        
        # 转换为 Python 数据结构
        python_data = edn_to_python(edn_data)
        
        start_time = time.time()
        
        if verbose:
            print(f"🚀 开始执行 EDN 数据...")
            print(f"📊 数据类型: {type(python_data).__name__}")
        
        # 执行数据
        if isinstance(python_data, list) and len(python_data) > 0:
            # 检查是否是单个命令还是命令列表
            if isinstance(python_data[0], str) and python_data[0].startswith(':'):
                # 单个命令 - 使用嵌套处理
                from beaver import process_nested
                result = process_nested(python_data)
                execution_count = 1
            else:
                # 命令列表，逐个执行
                results = []
                execution_count = 0
                
                for i, item in enumerate(python_data):
                    if verbose:
                        print(f"\n📋 执行第 {i+1} 个命令...")
                    
                    try:
                        # 使用嵌套处理来支持复杂的嵌套结构
                        from beaver import process_nested
                        result = process_nested(item)
                        results.append({
                            "index": i,
                            "success": True,
                            "result": result
                        })
                        execution_count += 1
                        
                        if verbose:
                            print(f"✅ 命令 {i+1} 执行成功")
                    except Exception as e:
                        results.append({
                            "index": i,
                            "success": False,
                            "error": str(e)
                        })
                        if verbose:
                            print(f"❌ 命令 {i+1} 执行失败: {e}")
                
                result = results
        else:
            # 直接执行
            from beaver import process_nested
            result = process_nested(python_data)
            execution_count = 1
        
        execution_time = round(time.time() - start_time, 3)
        
        return {
            "success": True,
            "result": result,
            "execution_count": execution_count,
            "execution_time": execution_time
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "execution_count": 0,
            "execution_time": 0
        }


def run_edn_file(
    file_path: str, 
    output_file: Optional[str] = None,
    verbose: bool = True,
    format_json: bool = False
) -> Dict[str, Any]:
    """
    运行 EDN 文件的完整流程
    
    参数:
        file_path: EDN 文件路径
        output_file: 输出文件路径（可选）
        verbose: 是否显示详细信息
        format_json: 是否格式化 JSON 输出
    
    返回:
        Dict: 完整的执行结果
    """
    start_time = time.time()
    
    try:
        if verbose:
            print(f"📂 加载 EDN 文件: {file_path}")
        
        # 加载和解析 EDN 文件
        edn_data = load_edn_file(file_path)
        
        if verbose:
            print(f"✅ EDN 文件解析成功")
        
        # 执行 EDN 数据
        execution_result = execute_edn_data(edn_data, verbose)
        
        # 构建完整结果
        total_time = round(time.time() - start_time, 3)
        
        full_result = {
            "file_path": file_path,
            "load_success": True,
            "execution": execution_result,
            "total_time": total_time,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if verbose:
            print(f"\n📈 执行统计:")
            print(f"⏱️  总用时: {total_time}s")
            print(f"🎯 执行命令数: {execution_result.get('execution_count', 0)}")
            print(f"✅ 执行状态: {'成功' if execution_result['success'] else '失败'}")
        
        # 输出结果
        if execution_result['success']:
            result_data = execution_result['result']
            
            if verbose:
                print(f"\n💡 执行结果:")
            
            if isinstance(result_data, list):
                # 多命令结果
                for item in result_data:
                    if item['success']:
                        print(f"✅ 命令 {item['index']+1}: {item['result']}")
                    else:
                        print(f"❌ 命令 {item['index']+1}: {item['error']}")
            else:
                # 单命令结果
                if format_json and isinstance(result_data, str):
                    try:
                        parsed = json.loads(result_data)
                        formatted = json.dumps(parsed, ensure_ascii=False, indent=2)
                        print(formatted)
                    except:
                        print(result_data)
                else:
                    print(result_data)
        else:
            if verbose:
                print(f"\n❌ 执行失败: {execution_result['error']}")
        
        # 保存到输出文件
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(full_result, f, ensure_ascii=False, indent=2, default=str)
            
            if verbose:
                print(f"\n💾 结果已保存到: {output_file}")
        
        return full_result
        
    except Exception as e:
        error_result = {
            "file_path": file_path,
            "load_success": False,
            "error": str(e),
            "total_time": round(time.time() - start_time, 3),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if verbose:
            print(f"❌ EDN 文件处理失败: {e}")
        
        return error_result


def create_sample_edn_files():
    """创建示例 EDN 文件用于演示"""
    
    samples_dir = Path("examples/edn_scripts")
    samples_dir.mkdir(parents=True, exist_ok=True)
    
    # 示例1：简单的文本操作
    sample1 = '''[:p "Hello" "World" "!"]'''
    
    with open(samples_dir / "simple_text.edn", "w", encoding="utf-8") as f:
        f.write(sample1)
    
    # 示例2：多个命令序列
    sample2 = '''[
  [:p "第一行文本"]
  [:str/upper "hello world"]
  [:md/h1 "标题"]
  [:md/list ["项目1" "项目2" "项目3"]]
]'''
    
    with open(samples_dir / "multiple_commands.edn", "w", encoding="utf-8") as f:
        f.write(sample2)
    
    # 示例3：消息处理
    sample3 = '''[
  [:user "Hello, AI assistant"]
  [:system "You are a helpful AI"]
  [:msg/batch [
    [":user" "第一条消息"]
    [":assistant" "AI 回复"]
    [":user" "第二条消息"]
  ]]
]'''
    
    with open(samples_dir / "message_processing.edn", "w", encoding="utf-8") as f:
        f.write(sample3)
    
    # 示例4：文件操作（注释版，避免实际执行）
    sample4 = ''';; 文件操作示例（注释掉避免实际执行）
;; [:file/write "test.txt" "Hello World"]
;; [:file/read "test.txt"]  
;; [:file/info "test.txt"]

;; 替代示例：字符串操作
[
  [:str/lower "HELLO WORLD"]
  [:str/upper "hello world"] 
  [:p "文件操作示例（已注释）"]
]'''
    
    with open(samples_dir / "file_operations.edn", "w", encoding="utf-8") as f:
        f.write(sample4)
    
    return samples_dir


def main():
    """命令行主函数"""
    parser = argparse.ArgumentParser(
        description="Beaver DSL EDN 文件执行器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python -m beaver.cli.edn_runner script.edn
  python -m beaver.cli.edn_runner script.edn -o result.json
  python -m beaver.cli.edn_runner script.edn --quiet --json
  python -m beaver.cli.edn_runner --create-samples
        """
    )
    
    parser.add_argument(
        "file", 
        nargs="?",
        help="要执行的 EDN 文件路径"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="输出结果到指定的 JSON 文件"
    )
    
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="静默模式，减少输出信息"
    )
    
    parser.add_argument(
        "-j", "--json",
        action="store_true", 
        help="格式化 JSON 输出"
    )
    
    parser.add_argument(
        "--create-samples",
        action="store_true",
        help="创建示例 EDN 文件"
    )
    
    args = parser.parse_args()
    
    # 创建示例文件
    if args.create_samples:
        samples_dir = create_sample_edn_files()
        print(f"✅ 示例 EDN 文件已创建在: {samples_dir}")
        print(f"📁 包含的示例文件:")
        for edn_file in samples_dir.glob("*.edn"):
            print(f"  - {edn_file.name}")
        return 0
    
    # 检查文件参数
    if not args.file:
        parser.error("需要指定 EDN 文件路径，或使用 --create-samples 创建示例")
    
    try:
        # 执行 EDN 文件
        result = run_edn_file(
            file_path=args.file,
            output_file=args.output,
            verbose=not args.quiet,
            format_json=args.json
        )
        
        # 返回适当的退出码
        if result.get("load_success", False) and result.get("execution", {}).get("success", False):
            return 0
        else:
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️  执行被用户中断")
        return 130
    except Exception as e:
        print(f"❌ 程序执行失败: {e}")
        return 1


# DSL 命令注册
from beaver.core.decorators import bf_element

@bf_element(':edn/run', 
    description='执行 EDN 脚本文件',
    category='文件执行',
    usage=':edn/run "script.edn"'
)
def edn_run_command(file_path: str):
    """
    DSL 命令：执行 EDN 脚本文件
    
    参数:
        file_path: EDN 脚本文件路径
    
    返回:
        str: 格式化的执行结果
    """
    try:
        # 执行 EDN 文件
        result = run_edn_file(file_path, verbose=False)
        
        if result["load_success"] and result["execution"]["success"]:
            execution = result["execution"]
            return f"""✅ EDN 脚本执行成功
📂 文件: {file_path}
⏱️  执行时间: {result['total_time']}s
🎯 命令数: {execution['execution_count']}

💡 执行结果:
{execution['result']}"""
        else:
            error_msg = result.get('error') or result.get('execution', {}).get('error', '未知错误')
            return f"""❌ EDN 脚本执行失败
📂 文件: {file_path}
🚨 错误: {error_msg}"""
            
    except Exception as e:
        return f"❌ EDN 命令执行失败: {str(e)}"


@bf_element(':edn/create-samples',
    description='创建 EDN 脚本示例文件',
    category='文件执行',
    usage=':edn/create-samples'
)
def edn_create_samples_command():
    """
    DSL 命令：创建示例 EDN 脚本文件
    
    返回:
        str: 示例文件创建结果
    """
    try:
        samples_dir = create_sample_edn_files()
        
        # 列出创建的文件
        sample_files = list(samples_dir.glob("*.edn"))
        file_list = "\n".join([f"  📄 {f.name}" for f in sample_files])
        
        return f"""✅ EDN 示例脚本创建成功
📁 目录: {samples_dir}
📊 文件数量: {len(sample_files)}

📋 示例文件:
{file_list}

💡 使用方法:
  :edn/run "examples/edn_scripts/simple_text.edn"
  :edn/run "examples/edn_scripts/multiple_commands.edn"
"""
        
    except Exception as e:
        return f"❌ 示例文件创建失败: {str(e)}"


@bf_element(':edn/load',
    description='加载并解析 EDN 文件（不执行）',
    category='文件执行', 
    usage=':edn/load "script.edn"'
)
def edn_load_command(file_path: str):
    """
    DSL 命令：加载并显示 EDN 文件内容
    
    参数:
        file_path: EDN 文件路径
        
    返回:
        str: EDN 文件内容信息
    """
    try:
        from beaver.inference.action_stream import edn_to_python
        
        # 加载 EDN 文件
        edn_data = load_edn_file(file_path)
        python_data = edn_to_python(edn_data)
        
        # 分析数据结构
        if isinstance(python_data, list):
            if len(python_data) > 0 and isinstance(python_data[0], str) and python_data[0].startswith(':'):
                data_type = "单个 DSL 命令"
                command_count = 1
            else:
                data_type = "多个 DSL 命令"
                command_count = len(python_data)
        else:
            data_type = "其他数据结构"
            command_count = 1
            
        # 格式化显示前几个命令
        preview = str(python_data)
        if len(preview) > 200:
            preview = preview[:200] + "..."
            
        return f"""📂 EDN 文件加载成功
📄 文件: {file_path}
📊 数据类型: {data_type}
🎯 命令数量: {command_count}

💡 内容预览:
{preview}

🚀 执行命令: :edn/run "{file_path}"
"""
        
    except Exception as e:
        return f"❌ EDN 文件加载失败: {str(e)}" 
    


if __name__ == "__main__":
    sys.exit(main())


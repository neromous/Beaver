#!/usr/bin/env python3
"""
Beaver DSL 命令行工具

使用方法:
    ./bf '[:p "hello" "world"]'
    ./bf '[:md/h1 "标题"]'
    ./bf '[:str/upper "text"]'
"""

import sys
import os

# 添加当前目录到Python路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# 初始化路径解析器
def init_path_resolver():
    """初始化路径解析器，设置当前工作目录和脚本目录"""
    try:
        from beaver.func.io.path_resolver import set_script_directory
        # 设置脚本目录为bf脚本所在目录
        set_script_directory(__file__)
    except ImportError:
        # 如果路径解析器模块不存在，忽略
        pass

def main():
    """主函数"""
    # 初始化路径解析器
    init_path_resolver()
    
    # 支持多种输入方式
    if len(sys.argv) == 1:
        # 没有参数，从标准输入读取
        print("请输入EDN命令（支持多行，按Ctrl+D结束）:", file=sys.stderr)
        try:
            edn_command = sys.stdin.read().strip()
            if not edn_command:
                print("错误: 未输入任何内容", file=sys.stderr)
                sys.exit(1)
        except KeyboardInterrupt:
            print("\n已取消", file=sys.stderr)
            sys.exit(1)
        except EOFError:
            print("错误: 输入被中断", file=sys.stderr)
            sys.exit(1)
    elif len(sys.argv) == 2:
        # 从命令行参数读取
        edn_command = sys.argv[1]
    else:
        print("使用方法: ./bf '<EDN命令>' 或 ./bf (从标准输入读取)", file=sys.stderr)
        print("", file=sys.stderr)
        print("示例:", file=sys.stderr)
        print("  # 单行命令", file=sys.stderr)
        print("  ./bf '[:p \"hello\" \"world\"]'", file=sys.stderr)
        print("  ./bf '[:md/h1 \"标题\"]'", file=sys.stderr)
        print("  ./bf '[:str/upper \"text\"]'", file=sys.stderr)
        print("  ./bf '[:file/write \"test.txt\" \"Hello World\"]'", file=sys.stderr)
        print("", file=sys.stderr)
        print("  # 多行命令（从标准输入）", file=sys.stderr)
        print("  ./bf", file=sys.stderr)
        print("  然后输入多行DSL，最后按Ctrl+D", file=sys.stderr)
        print("", file=sys.stderr)
        print("  # 从文件读取", file=sys.stderr)
        print("  ./bf < script.edn", file=sys.stderr)
        print("  cat script.edn | ./bf", file=sys.stderr)
        print("", file=sys.stderr)
        print("  # Here Document", file=sys.stderr)
        print("  ./bf << 'EOF'", file=sys.stderr)
        print("  [:rows", file=sys.stderr)
        print("    [:md/h1 \"标题\"]", file=sys.stderr)
        print("    [:p \"内容\"]]", file=sys.stderr)
        print("  EOF", file=sys.stderr)
        sys.exit(1)
    
    # 处理换行符：保留原始换行但去除首尾空白
    edn_command = edn_command.strip()
    
    try:
        # 导入需要的模块
        from beaver.inference import parse_action_syntax, execute_action
        
        # 解析EDN命令
        parsed_command = parse_action_syntax(edn_command)
        
        if parsed_command is None:
            print(f"错误: 无法解析EDN命令 '{edn_command}'", file=sys.stderr)
            print("请检查语法格式，确保使用正确的EDN语法", file=sys.stderr)
            sys.exit(1)
        
        # 执行命令
        result = execute_action(parsed_command)
        
        if result.success:
            # 输出结果
            print(result.rendered_output)
        else:
            print(f"错误: 命令执行失败 - {result.error}", file=sys.stderr)
            sys.exit(1)
            
    except ImportError as e:
        print(f"错误: 缺少依赖模块 - {e}", file=sys.stderr)
        print("请确保Beaver DSL系统已正确安装", file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 
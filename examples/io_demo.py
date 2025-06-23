#!/usr/bin/env python3
# examples/io_demo.py - IO 功能演示

import sys
import os
import tempfile
import shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import beaver

def io_demo():
    """IO 功能演示"""
    print("Beaver IO 功能演示")
    print("=" * 50)
    
    # 使用临时目录进行演示
    demo_dir = tempfile.mkdtemp(prefix='beaver_io_demo_')
    print(f"演示目录: {demo_dir}")
    
    try:
        # === 基础文件操作 ===
        print("\n=== 基础文件操作 ===")
        
        demo_file = os.path.join(demo_dir, 'demo.txt')
        
        # 写入文件
        result = beaver.execute([':file/write', demo_file, 'Hello, Beaver IO!'])
        print(f"写入文件: {result}")
        
        # 读取文件
        content = beaver.execute([':file/read', demo_file])
        print(f"读取内容: '{content}'")
        
        # 追加内容
        result = beaver.execute([':file/append', demo_file, '\nThis is appended content.'])
        print(f"追加内容: {result}")
        
        # 再次读取
        content = beaver.execute([':file/read', demo_file])
        print(f"追加后内容:\n{content}")
        
        # 文件信息
        info = beaver.execute([':file/info', demo_file])
        print(f"文件信息:\n{info}")
        
        # === 目录操作 ===
        print("\n=== 目录操作 ===")
        
        sub_dir = os.path.join(demo_dir, 'subdirectory')
        
        # 创建目录
        result = beaver.execute([':dir/create', sub_dir])
        print(f"创建目录: {result}")
        
        # 在子目录中创建文件
        sub_file = os.path.join(sub_dir, 'subfile.txt')
        result = beaver.execute([':file/write', sub_file, 'File in subdirectory'])
        print(f"子目录文件: {result}")
        
        # 列出目录内容
        listing = beaver.execute([':dir/list', demo_dir])
        print(f"目录内容:\n{listing}")
        
        # === 文件复制和移动 ===
        print("\n=== 文件复制和移动 ===")
        
        copy_file = os.path.join(demo_dir, 'demo_copy.txt')
        move_file = os.path.join(demo_dir, 'demo_moved.txt')
        
        # 复制文件
        result = beaver.execute([':file/copy', demo_file, copy_file])
        print(f"复制文件: {result}")
        
        # 移动文件
        result = beaver.execute([':file/move', copy_file, move_file])
        print(f"移动文件: {result}")
        
        # 再次列出目录
        listing = beaver.execute([':dir/list', demo_dir])
        print(f"操作后目录内容:\n{listing}")
        
        # === 生成报告文档 ===
        print("\n=== 生成报告文档 ===")
        
        # 使用嵌套 DSL 创建报告
        report = beaver.process_nested([
            ':rows',
            [':md/h1', 'Beaver IO 演示报告'],
            [':md/hr'],
            '',
            [':md/h2', '操作摘要'],
            [':p', '本次演示执行了以下操作：'],
            '',
            [':md/list',
             '创建演示文件',
             '写入和读取内容',
             '追加内容',
             '创建子目录',
             '复制和移动文件'],
            '',
            [':md/h2', '技术细节'],
            [':md/code-block', 'python',
             '# 基础用法示例',
             'import beaver',
             '',
             '# 写入文件',
             'beaver.execute([\':file/write\', \'demo.txt\', \'Hello World\'])',
             '',
             '# 读取文件',
             'content = beaver.execute([\':file/read\', \'demo.txt\'])',
             '',
             '# 创建目录',
             'beaver.execute([\':dir/create\', \'new_directory\'])'],
            '',
            [':md/blockquote', '这是一个自动生成的演示报告，展示了 Beaver 的 IO 功能。'],
            '',
                         [':md/h3', '命令统计'],
             [':p', '本次演示使用的 IO 命令：'],
             [':md/list',
              [':row', [':code', ':file/write'], ' - 写入文件内容'],
              [':row', [':code', ':file/read'], ' - 读取文件内容'],
              [':row', [':code', ':file/append'], ' - 追加文件内容'],
              [':row', [':code', ':file/info'], ' - 获取文件信息'],
              [':row', [':code', ':file/copy'], ' - 复制文件'],
              [':row', [':code', ':file/move'], ' - 移动文件'],
              [':row', [':code', ':dir/create'], ' - 创建目录'],
              [':row', [':code', ':dir/list'], ' - 列出目录内容']]
        ])
        
        # 保存报告
        report_file = os.path.join(demo_dir, 'demo_report.md')
        result = beaver.execute([':file/write', report_file, report])
        print(f"报告生成: {result}")
        
        print("\n生成的报告内容:")
        print("-" * 40)
        print(report)
        print("-" * 40)
        
        # === 展示所有IO命令 ===
        print("\n=== 可用的 IO 命令 ===")
        
        commands = beaver.list_all_commands()
        io_commands = {k: v for k, v in commands.items() if 'FileIO' in v.get('category', '')}
        
        print("文件操作命令:")
        file_commands = {k: v for k, v in io_commands.items() if k.startswith(':file/')}
        for cmd, meta in sorted(file_commands.items()):
            print(f"  {cmd}: {meta['description']}")
            print(f"    用法: {meta['usage']}")
        
        print("\n目录操作命令:")
        dir_commands = {k: v for k, v in io_commands.items() if k.startswith(':dir/')}
        for cmd, meta in sorted(dir_commands.items()):
            print(f"  {cmd}: {meta['description']}")
            print(f"    用法: {meta['usage']}")
        
        print(f"\n总计: {len(io_commands)} 个 IO 命令")
        
    finally:
        # 清理演示目录
        print(f"\n清理演示目录: {demo_dir}")
        shutil.rmtree(demo_dir, ignore_errors=True)
        print("清理完成")

if __name__ == '__main__':
    io_demo() 
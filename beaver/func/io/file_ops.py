"""
文件操作模块

开发流程：
1. 原始功能函数 -> 具体的文件操作
2. wrapper -> 文本化结果  
3. 注册函数 -> :file/命令

支持跨目录使用和路径解析。
"""

import os
import shutil
import json
from pathlib import Path
from typing import Union, List, Dict, Any
from beaver.core.decorators import bf_element
from .path_resolver import resolve_file_path, get_current_directory, get_path_resolver

# =============================================================================
# 1. 原始功能函数 - 具体的文件操作
# =============================================================================

def file_reader(file_path: Union[str, Path], encoding: str = 'utf-8') -> str:
    """读取文件内容"""
    # 解析路径为绝对路径
    resolved_path = resolve_file_path(file_path)
    try:
        with open(resolved_path, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {file_path} (解析为: {resolved_path})")
    except PermissionError:
        raise PermissionError(f"没有读取权限: {file_path} (解析为: {resolved_path})")
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"编码错误，无法使用 {encoding} 读取文件: {file_path} (解析为: {resolved_path})")

def file_writer(file_path: Union[str, Path], content: str, encoding: str = 'utf-8', append: bool = False) -> bool:
    """写入文件内容"""
    # 解析路径为绝对路径
    resolved_path = resolve_file_path(file_path)
    try:
        mode = 'a' if append else 'w'
        # 确保目录存在（避免空目录路径）
        dir_path = os.path.dirname(resolved_path)
        if dir_path:  # 只有当目录路径非空时才创建
            os.makedirs(dir_path, exist_ok=True)
        with open(resolved_path, mode, encoding=encoding) as f:
            f.write(content)
        return True
    except PermissionError:
        raise PermissionError(f"没有写入权限: {file_path} (解析为: {resolved_path})")
    except Exception as e:
        raise Exception(f"写入文件失败: {file_path} (解析为: {resolved_path}), 错误: {str(e)}")

def file_exists_checker(file_path: Union[str, Path]) -> bool:
    """检查文件是否存在"""
    resolved_path = resolve_file_path(file_path)
    return os.path.exists(resolved_path) and os.path.isfile(resolved_path)

def file_info_getter(file_path: Union[str, Path]) -> Dict[str, Any]:
    """获取文件信息"""
    if not file_exists_checker(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    stat = os.stat(file_path)
    return {
        'path': str(file_path),
        'name': os.path.basename(file_path),
        'size': stat.st_size,
        'modified': stat.st_mtime,
        'created': stat.st_ctime,
        'is_file': True,
        'is_directory': False,
        'extension': os.path.splitext(file_path)[1]
    }

def file_deleter(file_path: Union[str, Path]) -> bool:
    """删除文件"""
    try:
        if file_exists_checker(file_path):
            os.remove(file_path)
            return True
        return False
    except PermissionError:
        raise PermissionError(f"没有删除权限: {file_path}")
    except Exception as e:
        raise Exception(f"删除文件失败: {file_path}, 错误: {str(e)}")

def file_copier(src_path: Union[str, Path], dst_path: Union[str, Path]) -> bool:
    """复制文件"""
    try:
        # 确保目标目录存在（避免空目录路径）
        dir_path = os.path.dirname(dst_path)
        if dir_path:  # 只有当目录路径非空时才创建
            os.makedirs(dir_path, exist_ok=True)
        shutil.copy2(src_path, dst_path)
        return True
    except FileNotFoundError:
        raise FileNotFoundError(f"源文件不存在: {src_path}")
    except PermissionError:
        raise PermissionError(f"没有复制权限")
    except Exception as e:
        raise Exception(f"复制文件失败: {src_path} -> {dst_path}, 错误: {str(e)}")

def file_mover(src_path: Union[str, Path], dst_path: Union[str, Path]) -> bool:
    """移动/重命名文件"""
    try:
        # 确保目标目录存在（避免空目录路径）
        dir_path = os.path.dirname(dst_path)
        if dir_path:  # 只有当目录路径非空时才创建
            os.makedirs(dir_path, exist_ok=True)
        shutil.move(src_path, dst_path)
        return True
    except FileNotFoundError:
        raise FileNotFoundError(f"源文件不存在: {src_path}")
    except PermissionError:
        raise PermissionError(f"没有移动权限")
    except Exception as e:
        raise Exception(f"移动文件失败: {src_path} -> {dst_path}, 错误: {str(e)}")

# =============================================================================
# 目录操作的原始功能函数
# =============================================================================

def dir_exists_checker(dir_path: Union[str, Path]) -> bool:
    """检查目录是否存在"""
    return os.path.exists(dir_path) and os.path.isdir(dir_path)

def dir_creator(dir_path: Union[str, Path]) -> bool:
    """创建目录"""
    try:
        os.makedirs(dir_path, exist_ok=True)
        return True
    except PermissionError:
        raise PermissionError(f"没有创建目录权限: {dir_path}")
    except Exception as e:
        raise Exception(f"创建目录失败: {dir_path}, 错误: {str(e)}")

def dir_lister(dir_path: Union[str, Path], pattern: str = "*") -> List[str]:
    """列出目录内容"""
    if not dir_exists_checker(dir_path):
        raise FileNotFoundError(f"目录不存在: {dir_path}")
    
    try:
        path_obj = Path(dir_path)
        items = list(path_obj.glob(pattern))
        return [str(item) for item in sorted(items)]
    except PermissionError:
        raise PermissionError(f"没有访问目录权限: {dir_path}")

def dir_deleter(dir_path: Union[str, Path], recursive: bool = False) -> bool:
    """删除目录"""
    try:
        if not dir_exists_checker(dir_path):
            return False
        
        if recursive:
            shutil.rmtree(dir_path)
        else:
            os.rmdir(dir_path)  # 只能删除空目录
        return True
    except OSError as e:
        if "not empty" in str(e).lower():
            raise Exception(f"目录不为空，需要使用递归删除: {dir_path}")
        raise Exception(f"删除目录失败: {dir_path}, 错误: {str(e)}")

# =============================================================================
# 2. Wrapper 函数 - 文本化结果
# =============================================================================

def file_reader_wrapper(file_path: str, encoding: str = 'utf-8') -> str:
    """文件读取的文本化wrapper"""
    try:
        content = file_reader(file_path, encoding)
        return content
    except Exception as e:
        return f"错误: {str(e)}"

def file_writer_wrapper(file_path: str, content: str, encoding: str = 'utf-8', append: bool = False) -> str:
    """文件写入的文本化wrapper"""
    try:
        success = file_writer(file_path, content, encoding, append)
        if success:
            action = "追加" if append else "写入"
            return f"✓ 成功{action}文件: {file_path}"
        return f"✗ 写入失败: {file_path}"
    except Exception as e:
        return f"错误: {str(e)}"

def file_exists_wrapper(file_path: str) -> str:
    """文件存在性检查的文本化wrapper"""
    exists = file_exists_checker(file_path)
    return f"文件 {file_path}: {'存在' if exists else '不存在'}"

def file_info_wrapper(file_path: str) -> str:
    """文件信息的文本化wrapper"""
    try:
        info = file_info_getter(file_path)
        return f"""文件信息: {info['name']}
路径: {info['path']}
大小: {info['size']} 字节
扩展名: {info['extension']}
修改时间: {info['modified']}
创建时间: {info['created']}"""
    except Exception as e:
        return f"错误: {str(e)}"

def file_delete_wrapper(file_path: str) -> str:
    """文件删除的文本化wrapper"""
    try:
        success = file_deleter(file_path)
        if success:
            return f"✓ 成功删除文件: {file_path}"
        return f"✗ 文件不存在: {file_path}"
    except Exception as e:
        return f"错误: {str(e)}"

def file_copy_wrapper(src_path: str, dst_path: str) -> str:
    """文件复制的文本化wrapper"""
    try:
        success = file_copier(src_path, dst_path)
        if success:
            return f"✓ 成功复制文件: {src_path} -> {dst_path}"
        return f"✗ 复制失败: {src_path} -> {dst_path}"
    except Exception as e:
        return f"错误: {str(e)}"

def file_move_wrapper(src_path: str, dst_path: str) -> str:
    """文件移动的文本化wrapper"""
    try:
        success = file_mover(src_path, dst_path)
        if success:
            return f"✓ 成功移动文件: {src_path} -> {dst_path}"
        return f"✗ 移动失败: {src_path} -> {dst_path}"
    except Exception as e:
        return f"错误: {str(e)}"

def dir_exists_wrapper(dir_path: str) -> str:
    """目录存在性检查的文本化wrapper"""
    exists = dir_exists_checker(dir_path)
    return f"目录 {dir_path}: {'存在' if exists else '不存在'}"

def dir_create_wrapper(dir_path: str) -> str:
    """目录创建的文本化wrapper"""
    try:
        success = dir_creator(dir_path)
        if success:
            return f"✓ 成功创建目录: {dir_path}"
        return f"✗ 创建目录失败: {dir_path}"
    except Exception as e:
        return f"错误: {str(e)}"

def dir_list_wrapper(dir_path: str, pattern: str = "*") -> str:
    """目录列表的文本化wrapper"""
    try:
        items = dir_lister(dir_path, pattern)
        if not items:
            return f"目录 {dir_path} 为空"
        
        result = [f"目录内容: {dir_path}"]
        for item in items:
            item_type = "📁" if os.path.isdir(item) else "📄"
            result.append(f"  {item_type} {os.path.basename(item)}")
        return "\n".join(result)
    except Exception as e:
        return f"错误: {str(e)}"

def dir_delete_wrapper(dir_path: str, recursive: bool = False) -> str:
    """目录删除的文本化wrapper"""
    try:
        success = dir_deleter(dir_path, recursive)
        if success:
            action = "递归删除" if recursive else "删除"
            return f"✓ 成功{action}目录: {dir_path}"
        return f"✗ 目录不存在: {dir_path}"
    except Exception as e:
        return f"错误: {str(e)}"

# =============================================================================
# 3. 注册函数 - :file/ 和 :dir/ 命令
# =============================================================================

@bf_element(
    ':file/read',
    description='读取文件内容',
    category='FileIO',
    usage="[':file/read', '文件路径', '编码(可选)']")
def file_read_command(file_path: str, encoding: str = 'utf-8'):
    """读取文件内容的DSL命令"""
    return file_reader_wrapper(file_path, encoding)

@bf_element(
    ':file/write',
    description='写入文件内容',
    category='FileIO',
    usage="[':file/write', '文件路径', '内容', '编码(可选)', '是否追加(可选)']")
def file_write_command(file_path: str, content: str, encoding: str = 'utf-8', append: bool = False):
    """写入文件内容的DSL命令"""
    return file_writer_wrapper(file_path, content, encoding, append)

@bf_element(
    ':file/append',
    description='追加文件内容',
    category='FileIO',
    usage="[':file/append', '文件路径', '内容', '编码(可选)']")
def file_append_command(file_path: str, content: str, encoding: str = 'utf-8'):
    """追加文件内容的DSL命令"""
    return file_writer_wrapper(file_path, content, encoding, append=True)

@bf_element(
    ':file/exists',
    description='检查文件是否存在',
    category='FileIO',
    usage="[':file/exists', '文件路径']")
def file_exists_command(file_path: str):
    """检查文件是否存在的DSL命令"""
    return file_exists_wrapper(file_path)

@bf_element(
    ':file/info',
    description='获取文件信息',
    category='FileIO',
    usage="[':file/info', '文件路径']")
def file_info_command(file_path: str):
    """获取文件信息的DSL命令"""
    return file_info_wrapper(file_path)

@bf_element(
    ':file/delete',
    description='删除文件',
    category='FileIO',
    usage="[':file/delete', '文件路径']")
def file_delete_command(file_path: str):
    """删除文件的DSL命令"""
    return file_delete_wrapper(file_path)

@bf_element(
    ':file/copy',
    description='复制文件',
    category='FileIO',
    usage="[':file/copy', '源路径', '目标路径']")
def file_copy_command(src_path: str, dst_path: str):
    """复制文件的DSL命令"""
    return file_copy_wrapper(src_path, dst_path)

@bf_element(
    ':file/move',
    description='移动/重命名文件',
    category='FileIO',
    usage="[':file/move', '源路径', '目标路径']")
def file_move_command(src_path: str, dst_path: str):
    """移动/重命名文件的DSL命令"""
    return file_move_wrapper(src_path, dst_path)

# 目录操作命令

@bf_element(
    ':dir/exists',
    description='检查目录是否存在',
    category='FileIO',
    usage="[':dir/exists', '目录路径']")
def dir_exists_command(dir_path: str):
    """检查目录是否存在的DSL命令"""
    return dir_exists_wrapper(dir_path)

@bf_element(
    ':dir/create',
    description='创建目录',
    category='FileIO',
    usage="[':dir/create', '目录路径']")
def dir_create_command(dir_path: str):
    """创建目录的DSL命令"""
    return dir_create_wrapper(dir_path)

@bf_element(
    ':dir/list',
    description='列出目录内容',
    category='FileIO',
    usage="[':dir/list', '目录路径', '模式(可选)']")
def dir_list_command(dir_path: str, pattern: str = "*"):
    """列出目录内容的DSL命令"""
    return dir_list_wrapper(dir_path, pattern)

@bf_element(
    ':dir/delete',
    description='删除目录',
    category='FileIO',
    usage="[':dir/delete', '目录路径', '是否递归(可选)']")
def dir_delete_command(dir_path: str, recursive: bool = False):
    """删除目录的DSL命令"""
    return dir_delete_wrapper(dir_path, recursive)

# 路径信息命令

@bf_element(
    ':path/info',
    description='显示路径信息',
    category='FileIO',
    usage="[':path/info', '文件路径']")
def path_info_command(file_path: str):
    """显示路径信息的DSL命令"""
    resolver = get_path_resolver()
    path_info = resolver.create_path_info(file_path)
    
    result = [f"路径信息: {file_path}"]
    result.append(f"  原始路径: {path_info['original']}")
    result.append(f"  解析路径: {path_info['resolved']}")
    result.append(f"  标准化路径: {path_info['normalized']}")
    result.append(f"  相对路径: {path_info['relative_to_cwd']}")
    result.append(f"  是否绝对路径: {'是' if path_info['is_absolute'] else '否'}")
    result.append(f"  文件存在: {'是' if path_info['exists'] else '否'}")
    if path_info['exists']:
        result.append(f"  文件类型: {'文件' if path_info['is_file'] else '目录' if path_info['is_directory'] else '其他'}")
    result.append(f"  目录部分: {path_info['dirname']}")
    result.append(f"  文件名部分: {path_info['basename']}")
    result.append(f"  当前工作目录: {path_info['current_directory']}")
    if path_info['script_directory']:
        result.append(f"  脚本目录: {path_info['script_directory']}")
    
    return "\n".join(result)

@bf_element(
    ':path/cwd',
    description='显示当前工作目录',
    category='FileIO',
    usage="[':path/cwd']")
def current_directory_command():
    """显示当前工作目录的DSL命令"""
    cwd = get_current_directory()
    return f"当前工作目录: {cwd}"

@bf_element(
    ':path/resolve',
    description='解析文件路径为绝对路径',
    category='FileIO',
    usage="[':path/resolve', '文件路径']")
def resolve_path_command(file_path: str):
    """解析文件路径的DSL命令"""
    resolved = resolve_file_path(file_path)
    return f"{file_path} → {resolved}"

# 导出所有公开的函数
__all__ = [
    # 原始功能函数
    'file_reader', 'file_writer', 'file_exists_checker', 'file_info_getter',
    'file_deleter', 'file_copier', 'file_mover',
    'dir_exists_checker', 'dir_creator', 'dir_lister', 'dir_deleter',
    
    # Wrapper函数
    'file_reader_wrapper', 'file_writer_wrapper', 'file_exists_wrapper',
    'file_info_wrapper', 'file_delete_wrapper', 'file_copy_wrapper',
    'file_move_wrapper', 'dir_exists_wrapper', 'dir_create_wrapper',
    'dir_list_wrapper', 'dir_delete_wrapper',
    
    # DSL命令函数
    'file_read_command', 'file_write_command', 'file_append_command',
    'file_exists_command', 'file_info_command', 'file_delete_command',
    'file_copy_command', 'file_move_command', 'dir_exists_command',
    'dir_create_command', 'dir_list_command', 'dir_delete_command'
]
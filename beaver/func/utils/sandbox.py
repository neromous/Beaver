from __future__ import annotations

"""
沙箱白名单管理命令

提供以下 DSL 命令：
  - :sandbox/allow  (追加一个目录到白名单)
  - :sandbox/set    (重置并设置白名单，为空代表无限制)
  - :sandbox/list   (查看当前白名单)
  - :sandbox/clear  (清空白名单，恢复无限制)

所有命令位于 Security 分类。
"""

import os
from typing import List
from beaver.core.decorators import bf_element
from beaver.func.io.path_resolver import get_path_resolver

resolver = get_path_resolver()


@bf_element(
    ':sandbox/allow',
    description='向白名单追加一个目录',
    category='Security',
    usage="[':sandbox/allow', '目录路径']"
)
def sandbox_allow(dir_path: str) -> str:
    abs_dir = os.path.abspath(dir_path)
    resolver.add_allowed_directory(abs_dir)
    return f"✓ 已加入白名单: {abs_dir}"


@bf_element(
    ':sandbox/set',
    description='重新设置白名单，将覆盖现有设置；不传参数视为无限制',
    category='Security',
    usage="[':sandbox/set', '目录1', '目录2', ...]"
)
def sandbox_set(*dirs: str) -> str:
    abs_dirs: List[str] = [os.path.abspath(d) for d in dirs]
    resolver.set_allowed_directories(abs_dirs)
    if abs_dirs:
        return f"✓ 白名单已设置为: {abs_dirs}"
    return '✓ 已取消所有目录限制（无限制）'


@bf_element(
    ':sandbox/list',
    description='查看当前白名单目录列表',
    category='Security',
    usage="[':sandbox/list']"
)
def sandbox_list() -> List[str]:
    return resolver.list_allowed_directories()


@bf_element(
    ':sandbox/clear',
    description='清空白名单，恢复无限制',
    category='Security',
    usage="[':sandbox/clear']"
)
def sandbox_clear() -> str:
    resolver.clear_allowed_directories()
    return '✓ 已清空白名单，当前无限制访问' 
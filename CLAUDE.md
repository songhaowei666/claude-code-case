# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 技术栈

- 语言：Python
- 项目阶段：初始化阶段，尚未添加代码

## 常用命令

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# 安装依赖（使用 pip）
pip install -r requirements.txt

# 安装依赖（使用 Poetry）
poetry install

# 运行测试（pytest）
pytest
pytest tests/ -v
pytest tests/test_xxx.py::test_func_name -v  # 运行单个测试

# 代码格式化
black .
ruff format .

# 代码检查
ruff check .
mypy src/

# 构建发布包
python -m build
```

## 架构

_TODO: 待代码添加后补充项目架构说明。_

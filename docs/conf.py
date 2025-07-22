# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

# Add a default value so it won't break when not provided
platform = 'default'

project = 'My Docs'
copyright = '2025, hearR'
author = 'hearR'
release = '0.1'

def setup(app):
    app.add_config_value('platform', default='default', rebuild='env')

    def on_builder_inited(app):
        platform = app.config.platform
        print(f"[DEBUG] 当前构建平台: {platform}")

        if platform == 'eigen_718p':
            app.tags.add('EIGEN_718P')
            quecos_name = 'EIGEN_718P'
        elif platform == 'eigen_718pm':
            app.tags.add('EIGEN_718PM')
            quecos_name = 'EIGEN_718PM'
        else:
            print(f"[WARNING] 未识别的平台: {platform}")
            quecos_name = 'default'

        # 💡 关键：在运行时动态设置 rst_epilog
        app.config.rst_epilog = f"""
.. |QUECOS_TARGET_PATH_NAME| replace:: {quecos_name}
"""
    print("[DEBUG] rst_epilog 设置为:\n", app.config.rst_epilog)

    app.connect("builder-inited", on_builder_inited)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",      # 自动从 docstring 生成文档（适用于 Python 项目）
    "sphinx.ext.todo",         # 支持 TODO 标签
    "sphinx.ext.ifconfig",     # 支持 if/only 条件构建
    "sphinx.ext.viewcode",     # 添加源代码查看链接（Python）
    "sphinx.ext.intersphinx",  # 支持跨项目引用
    "sphinx.ext.autosectionlabel",  # 支持自动生成标题引用标签
]


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

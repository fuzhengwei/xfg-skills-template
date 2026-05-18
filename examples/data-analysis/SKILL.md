---
name: data-analysis
description: 分析 CSV、TSV、Excel 等表格数据文件，计算统计摘要、生成图表、清洗脏数据。当用户有数据文件需要探索、转换、可视化，或提到数据分析、统计、图表时使用此技能。
license: Apache-2.0
compatibility: 需要 Python 3.10+
metadata:
  author: xfg-studio
  version: "1.0.0"
  category: analytics
---

# 数据分析技能

对表格数据文件进行探索、分析和可视化。

## 支持的文件格式

- CSV / TSV
- Excel (.xlsx, .xls)

## 核心功能

### 1. 探索性分析
```python
import pandas as pd

df = pd.read_csv("data.csv")
print(df.shape)           # 行数和列数
print(df.dtypes)          # 列类型
print(df.describe())      # 统计摘要
print(df.isnull().sum())  # 缺失值统计
```

### 2. 数据清洗
- 处理缺失值：填充或删除
- 去除重复行
- 类型转换
- 异常值检测

### 3. 数据可视化
使用 matplotlib 生成图表：
- 柱状图：分类数据对比
- 折线图：趋势分析
- 散点图：相关性分析
- 直方图：分布分析

### 4. 统计分析
- 描述统计（均值、中位数、标准差）
- 分组聚合
- 相关性分析

## 工作流

1. 读取数据文件，检查格式和编码
2. 输出基本统计摘要
3. 根据用户需求进行特定分析
4. 生成图表时保存到文件并报告路径

## 输出规范

- 统计结果使用 Markdown 表格
- 图表保存为 PNG 文件
- 清洗后的数据保存为新文件，不覆盖原始数据

## Gotchas

- 读取文件时始终指定 `encoding='utf-8'`，中文数据可能需要 `encoding='gbk'`
- Excel 文件使用 `openpyxl` 引擎：`pd.read_excel(file, engine='openpyxl')`
- 生成图表后必须调用 `plt.tight_layout()` 避免标签截断
- 中文字体设置：`plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']`

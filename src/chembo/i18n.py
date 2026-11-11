"""Small, offline Chinese/English catalog for the desktop interface.

Only presentation strings pass through this module. Project values and scientific
engine identifiers never depend on the displayed language.
"""
from collections import OrderedDict
import os
import re
from string import Formatter

from PySide6.QtCore import QObject, QSettings, QSignalBlocker, QTranslator, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication, QComboBox, QLabel, QMenu, QPlainTextEdit, QPushButton,
    QTableWidget, QTabWidget, QWidget,
)

EN = {
    '确定': 'OK', '取消': 'Cancel', '关闭': 'Close', '不保存': 'Discard',
    '应用': 'Apply', '重置': 'Reset',
    'Gryffin · 类别与连续变量': 'Gryffin · categorical / continuous',
    'Atlas · 高斯过程': 'Atlas · Gaussian process',
    'BoTorch · 优化与分类': 'BoTorch · optimization / classification',
    '数值优化 / 优先级': 'Numeric / priority optimization',
    '连续': 'Continuous', '整数': 'Integer', '类别': 'Categorical',
    '最大化': 'Maximize', '最小化': 'Minimize',
    '首个优化目标的历史最佳值': 'Best measured value of the first objective',
    '首个目标 · 历史最佳实测值': 'First objective · best measured value',
    '录入实验结果后显示趋势': 'Add measured results to display the trend',
    '化学实验规划  /  本地计算': 'Plan chemistry experiments / compute locally',
    '新项目': 'New', '教学示例': 'Examples', '打开': 'Open', '保存': 'Save',
    '使用教程': 'Guide', '关于 / 许可': 'About / licenses',
    '定义变量 → 录入已有结果 → 生成下一批 → 实验后回填': 'Define variables → add measured results → suggest a batch → measure and import results',
    '分类标签用 | 分隔；结果表目标列填写其中一个标签。': 'Separate class labels with |. Enter one of these labels in the result column.',
    '项目名称': 'Project name', '任务类型': 'Task', '推荐引擎': 'Engine',
    '分类标签': 'Class labels', '本批实验数': 'Experiments per batch', '随机种子': 'Random seed',
    '1  定义实验空间': '1  Define the experiment space',
    '变量名': 'Variable', '类型': 'Type', '下限': 'Lower', '上限': 'Upper',
    '类别（| 分隔）': 'Categories (|)', '单位': 'Unit', '步长': 'Step',
    '＋ 变量': '+ Variable', '删除选中变量': 'Remove selected',
    '配方约束 / 候选表…': 'Constraints / candidates…', '清除联合限制': 'Clear constraints',
    '数值目标可最大化或最小化；分类只保留一个标签列。': 'Maximize or minimize numeric objectives. Classification uses a single label column.',
    '目标名称': 'Objective', '方向': 'Goal', '容忍比例 (0–1)': 'Tolerance (0–1)',
    '＋ 目标': '+ Objective', '删除选中目标': 'Remove selected',
    '项目备注、实验单位、数据来源……': 'Project notes, units, data sources…',
    'BoTorch 支持步长、合法候选表、总量／配比约束、Pareto、分类与模型验证。步长从下限起算，留空表示连续。': 'BoTorch supports steps, candidate lists, total / ratio constraints, Pareto, classification and validation. Steps start at the lower bound; leave blank for continuous values.',
    '2  已完成实验 · 每行填写全部变量和目标值': '2  Completed experiments · enter every variable and objective in each row',
    '＋ 录入一行': '+ Row', '导入 Excel / CSV': 'Import Excel / CSV',
    '导出结果': 'Export results', '删除选中行': 'Remove selected',
    '已完成实验': 'Completed experiments',
    '3  待实验条件 · 回填结果前保持在此列表，避免重复推荐': '3  Pending experiments · keep conditions here until measured to avoid repeated suggestions',
    '导出待回填 CSV': 'Export pending CSV', '将选中条件转入结果表': 'Move selected to results',
    '撤回选中条件': 'Withdraw selected',
    '导出 CSV 后填写目标列，再从“已完成实验”导入；匹配的待实验条件会自动移除。': 'Export CSV, fill in the objective columns, then import under Completed experiments. Matching pending conditions are removed automatically.',
    '下一批 / 待实验': 'Next batch / pending', '运行日志': 'Run log',
    '模型与可视化': 'Models and plots', '取消计算': 'Cancel',
    '生成下一批实验  →': 'Suggest next experiments  →', '分析与交叉验证': 'Analyze / validate',
    '文件': 'File', '打开项目…': 'Open project…', '保存项目': 'Save project',
    '项目另存为…': 'Save project as…', '帮助': 'Help',
    '中文使用教程': 'Chinese tutorial', '导出教程练习数据…': 'Export practice data…',
    '关于 SynthBO': 'About SynthBO',
    '任务已切换。已有数据保留；请检查目标列和分类标签，或载入相应教学示例。': 'Task changed. Data are preserved; check the objective columns and class labels, or load the corresponding example.',
    '使用与推荐相同的 BoTorch / 分类模型重新拟合并进行留一验证。': 'Refit and run leave-one-out validation with the same BoTorch / classification model used for suggestions.',
    '当前引擎保留原生推荐；模型诊断请使用 BoTorch 工作流。': 'This engine uses its native suggestions. Use the BoTorch workflow for model diagnostics.',
    '联合约束 {v0} 条  ·  合法候选表 {v1} 行': '{v0} joint constraints  ·  {v1} candidate rows',
    '已清除联合约束和候选表；变量步长仍在变量表中，可单独修改。': 'Joint constraints and the candidate list were cleared. Variable steps remain in the variable table.',
    '已完成 {v0} 个实验   ·   待实验 {v1} 个   ·   {v2}': '{v0} completed experiments   ·   {v1} pending   ·   {v2}',
    '尚未保存项目': 'Unsaved project', '请检查输入': 'Check the input',
    '请先等待计算完成，或取消计算。': 'Wait for the calculation to finish, or cancel it first.',
    '当前项目有未保存的修改。': 'This project has unsaved changes.',
    '我的实验项目': 'My experiment project', '数值优化': 'Numeric optimization',
    '总量与步长': 'Total constraints & steps', 'Pareto 多目标': 'Pareto optimization',
    '分类主动学习': 'Classification active learning',
    '教学示例（全部为模拟数据）': 'Examples (all data are simulated)',
    '选择工作流': 'Choose a workflow', '打开项目': 'Open project',
    'ChemBO 项目 (*.json)': 'SynthBO project (*.json)',
    '导入完成的实验结果': 'Import measured results',
    '实验数据 (*.xlsx *.xls *.csv)': 'Experiment data (*.xlsx *.xls *.csv)',
    '导出 CSV': 'Export CSV', '已导出：{v0}': 'Exported: {v0}',
    '无法创建计算临时目录。': 'Could not create a temporary calculation folder.',
    '正在运行 {v0}；首次启动可能需要较长时间。': 'Running {v0}; the first launch may take longer.',
    '当前安装包未包含 BoTorch 引擎。请安装完整版。': 'This package does not contain the BoTorch engine. Install the full package.',
    '模型计算中；可切换到运行日志查看进度。': 'Calculating. Open Run log to view progress.',
    '计算结束。项目保存在本机。': 'Calculation finished. Projects are stored locally.',
    '已取消计算，实验记录已保留。': 'Calculation cancelled. Experiment records are preserved.',
    '引擎未返回结果。请查看运行日志。': 'The engine did not return a result. Check Run log.',
    '模型计算失败': 'Model calculation failed',
    '模型分析与验证已完成；结果见“模型与可视化”，请保存项目。': 'Analysis and validation finished. See Models & plots, then save the project.',
    '已生成 {v0} 个待实验条件。可查看预测与排序、导出配方后回填结果。': '{v0} pending experiments generated. Inspect predictions and rankings, export conditions, then add measured results.',
    '未找到随附教程，请重新安装包含教程的完整 SynthBO 安装包。': 'The offline tutorial is missing. Reinstall the full SynthBO package.',
    '系统未能打开教程。可从 GitHub 项目的中英文 README 进入使用指南。': 'The system could not open the tutorial. The Chinese and English READMEs on GitHub link to the guides.',
    '未找到教程练习数据，请重新安装完整 SynthBO 安装包。': 'Practice data are missing. Reinstall the full SynthBO package.',
    '选择练习数据的保存位置': 'Choose where to save practice data',
    '练习数据已导出到 {v0}。点击“打开”选择练习文件夹中的 project.chembo.json；数据均为模拟数据。': 'Practice data exported to {v0}. Click Open and select project.chembo.json in a practice folder. All practice data are simulated.',
    'SynthBO {v0}\n\n独立开发的本地实验规划界面，并非上游团队官方桌面产品。\n\nGryffin — Apache-2.0，Copyright (C) 2020 Harvard University\nAtlas — MIT，Copyright (c) 2022 rileyhickman\nBO-MCP — MIT，Copyright (c) 2026 Willi Gottstein\nChimera / Olympus / Golem — 见随附上游许可证\nQt / PySide6 — LGPLv3，动态链接；可重建、替换相容库。\n\n初始点属于实验设计；有足够实测数据后才由模型指导推荐。\n推荐值不是已验证的实验结果，也不保证最优。\n\n源代码、依赖锁定、重建说明及完整第三方声明随项目提供。\n发表科研结果时请引用实际使用的算法论文。': 'SynthBO {v0}\n\nAn independently developed, local experiment-planning interface; not an official desktop product of the upstream research teams.\n\nGryffin — Apache-2.0, Copyright (C) 2020 Harvard University\nAtlas — MIT, Copyright (c) 2022 rileyhickman\nBO-MCP — MIT, Copyright (c) 2026 Willi Gottstein\nChimera / Olympus / Golem — see bundled upstream licenses\nQt / PySide6 — LGPLv3, dynamically linked; compatible libraries can be rebuilt and replaced.\n\nInitial points are an experimental design. Model-guided suggestions require enough measured data.\nSuggestions are not verified experimental results and do not guarantee an optimum.\n\nSource code, pinned dependencies, rebuild instructions and full third-party notices accompany the project.\nCite the algorithm papers actually used when publishing research results.',
    '打开随附许可证文件夹': 'Open bundled licenses',
    '尚未分析；生成建议或运行模型分析后，在这里查看结果。': 'No analysis yet. Generate suggestions or run analysis to view results here.',
    '图表目标': 'Chart objective', '查看目标': 'Objective',
    '导出当前图…': 'Export chart…',
    '导出当前图表；在预测表页时导出候选预测图。': 'Export the displayed chart. On the prediction table tab, export the candidate prediction chart.',
    '导出预测表 CSV…': 'Export predictions CSV…', '候选预测表': 'Prediction table',
    '候选预测与区间': 'Predictions & intervals', '预测均值与不确定性': 'Mean & uncertainty',
    '采集分值排序': 'Acquisition ranking', '预测与实测': 'Predicted vs measured',
    '验证误差': 'Validation residuals', '观测分布': 'Measured distribution',
    '实测历史': 'Measurement history', '分布变量': 'Distribution variable',
    '二维 Pareto': '2D Pareto', '三维 Pareto': '3D Pareto',
    '超体积历史': 'Hypervolume history', 'Pareto {v0}轴': 'Pareto {v0} axis',
    '候选类别概率': 'Candidate class probabilities', '分类不确定性': 'Classification uncertainty',
    '已测类别分布': 'Measured class counts', '混淆矩阵': 'Confusion matrix',
    '预测与探索': 'Predictions', '模型验证': 'Model validation',
    '数据分布': 'Data distribution', '分类分析': 'Classification',
    '点击图中的候选点可查看对应条件；工具栏支持平移、缩放和还原。': 'Click a candidate point to inspect its conditions. Use the toolbar to pan, zoom and reset.',
    '尚未拟合模型': 'Model not fitted', '尚无分析结果': 'No analysis yet',
    '已拟合': 'Fitted', '初始设计': 'Initial design',
    '候选编号': 'Candidate ID', '本批推荐': 'Selected for batch', '熵': 'Entropy',
    '采集分值': 'Acquisition score', '是': 'Yes', '否': 'No',
    '{v0} · 预测': '{v0} · prediction', '{v0} · 标准差': '{v0} · standard deviation',
    '数值预测': 'Numeric predictions',
    '当前任务为分类；请查看“分类分析”中的类别概率与熵。': 'This is a classification task. See Classification for class probabilities and entropy.',
    '候选预测': 'Candidate predictions',
    '当前没有已拟合模型的候选预测。初始设计阶段尚未训练模型；完成模型分析后显示预测值与区间。': 'No fitted candidate predictions yet. Initial design does not train a model; predictions and intervals appear after model analysis.',
    ' · 候选模型预测': ' · candidate model predictions', '候选 {v0}: ': 'Candidate {v0}: ',
    '当前引擎没有返回可用的候选模型标准差。': 'The engine did not return usable candidate model standard deviations.',
    '预测均值': 'Predicted mean', '模型标准差': 'Model standard deviation',
    '当前引擎未返回可用的采集分值。': 'The engine did not return usable acquisition scores.',
    '按采集分值排序的位置': 'Rank by acquisition score',
    '（同次分析内比较）': ' (compare within this analysis only)',
    '均值 ± 1.96 × 模型标准差': 'Mean ± 1.96 × model standard deviation',
    '模型均值': 'Model mean', '候选编号（对应预测表）': 'Candidate ID (see prediction table)',
    '{v0} 个未测候选。图中为模型预测，不是实测结果；区间未作额外覆盖率校准，不表示实验误差。采集分值仅供本次分析内比较。': '{v0} unmeasured candidates. These are model predictions. Intervals have no additional coverage calibration and do not represent experimental error. Compare acquisition scores only within this analysis. ',
    '分类验证请查看“分类分析 → 混淆矩阵”。': 'See Classification → Confusion matrix for classification validation.',
    '尚无交叉验证结果。完成模型验证后显示；样本不足或模型尚未拟合时暂不计算。': 'No cross-validation results yet. Run validation with sufficient data and a fitted model.',
    '交叉验证': 'Cross-validation', '被留出实验的序号': 'Held-out experiment index',
    '预测 − 实测': 'Predicted − measured',
    '实测值（验证时未参与训练）': 'Measured value (held out of training)',
    '留出预测值': 'Held-out prediction',
    '实际使用模型的 {v0}；验证 {v1} 行。': '{v0} with the actual model; {v1} rows evaluated. ',
    '观测数据': 'Measured data',
    '录入已完成实验后显示分布；待实验条件不计入统计。': 'Add completed experiments to view distributions. Pending conditions are excluded.',
    '该变量尚无完整的实测数据。': 'No complete measurements for this variable yet.',
    ' · 已完成实验': ' · completed experiments', '实测': 'Measured',
    '历史最佳实测': 'Best measured so far', '实验记录序号': 'Experiment record index',
    '实测记录数': 'Measured record count',
    '该变量有 {v0} 条完整实测记录，包含重复实验；记录顺序不等于真实时间间隔。': '{v0} complete measurements, including replicates. Record order does not represent elapsed time.',
    '至少两个数值目标，并运行 Pareto 分析后显示；Chimera 优先级优化不等同于 Pareto 搜索。': 'Set at least two numeric objectives and run Pareto analysis. Chimera priority optimization and Pareto search use different objective strategies.',
    '当前没有在共同参考点下计算的超体积记录。': 'No hypervolume history calculated with a common reference point.',
    '已测 Pareto 前沿 · 超体积历史': 'Measured Pareto front · hypervolume history',
    '超体积（共同参考点）': 'Hypervolume (common reference point)',
    'Pareto 目标投影': 'Pareto objective projection',
    '请选择 {v0} 个不同目标。': 'Select {v0} different objectives.',
    'Pareto 前沿': 'Pareto front', '尚无完整的多目标实测数据。': 'No complete multi-objective measurements yet.',
    '已测结果 · ': 'Measured results · ', 'Pareto 投影': 'Pareto projection',
    '其他实测': 'Other measurements', '全目标非支配实测': 'Non-dominated over all objectives',
    '只绘制已测结果，未测预测与 pending 不进入实测 Pareto 前沿。参考点：': 'Only measurements enter the measured Pareto front; predictions and pending conditions are excluded. Reference point: ',
    ' 多于两个目标时，二维投影不保证形成有序曲线。': ' With more than two objectives, a 2D projection need not form an ordered curve.',
    '当前任务为数值优化。切换分类任务后显示类别概率、熵和分类验证。': 'This is numeric optimization. Switch to classification to view class probabilities, entropy and classification validation.',
    '未测候选 · 类别概率': 'Unmeasured candidates · class probabilities',
    '未测候选 · 分类熵': 'Unmeasured candidates · class entropy',
    '已完成实验 · 类别分布': 'Completed experiments · class counts',
    '留出验证 · 混淆矩阵': 'Held-out validation · confusion matrix',
    '类别概率': 'Class probability',
    '尚未具备可训练的类别数据。初始探索阶段尚无模型类别概率。': 'Not enough class data to train a model. Initial exploration has no model class probabilities.',
    '模型没有返回所设类别的概率；请查看模型状态与警告。': 'The model did not return probabilities for the configured classes. Check model status and warnings.',
    '模型返回的类别概率不完整，无法绘制堆积概率图。': 'Class probabilities are incomplete; a stacked probability chart cannot be drawn.',
    '候选编号（前 40 个；完整数据见表格）': 'Candidate ID (first 40; full data in table)',
    '当前没有已拟合分类器的熵。': 'No entropy from a fitted classifier yet.',
    '预测类别熵（越大越不确定）': 'Class entropy (higher = more uncertain)',
    '尚无留出分类验证；样本或类别不足时暂不计算准确率。': 'No held-out classification validation. Accuracy requires sufficient samples and classes.',
    '留出预测类别': 'Held-out predicted class', '实测类别': 'Measured class',
    '固定分类模型的概率/熵仅用于分类主动学习；它不等于化学性能预测。未返回的类别概率保持缺失，不补零。': 'Probabilities / entropy from the fixed classifier support active learning, not numeric chemical performance prediction. Unreturned class probabilities remain missing.',
    ' 留出准确率={v0}。': ' Held-out accuracy={v0}.',
    '图像格式必须是 PNG、PDF 或 SVG。': 'Choose PNG, PDF or SVG for the chart.',
    '没有可导出的候选预测。': 'No candidate predictions to export.',
    '导出当前分析图': 'Export current analysis chart', '导图失败': 'Chart export failed',
    '导出候选预测表': 'Export candidate predictions', '导出失败': 'Export failed',
    '选择工作表': 'Choose a worksheet', '读取工作表': 'Worksheet to import',
    '可执行配方空间': 'Executable recipe space',
    '步长在变量表中设置。这里设置总量／线性约束、配比和合法候选配方。\n应用后使用 BoTorch；生成条件必须同时满足全部规则。': 'Set steps in the variable table. Define total / linear constraints, ratios and allowed recipes here.\nApplying these settings uses BoTorch. Suggested conditions must satisfy every rule.',
    '已启用的联合约束': 'Enabled joint constraints', '＋ 总量／线性': '+ Total / linear',
    '＋ 配比': '+ Ratio', '删除选中规则': 'Remove selected rule',
    '导入合法候选表（Excel / CSV）': 'Import allowed candidates (Excel / CSV)',
    '清除候选表': 'Clear candidate list',
    '候选表只含变量列，表头与变量名一致；历史实验可来自表外，下一批仅从候选表选择。配比的分母为 0 时不合法。': 'The candidate list contains variable columns only, with matching names. Historical experiments may be outside the list; new suggestions come only from it. A zero ratio denominator is invalid.',
    '应用（使用 BoTorch）': 'Apply (use BoTorch)', '不限': 'Unbounded',
    '合法候选表：{v0} 个配方（下方预览前 30 行）': 'Allowed candidates: {v0} recipes (first 30 previewed below)',
    '未设置候选表：从变量范围／步长和约束构建候选。': 'No candidate list: construct candidates from variable bounds, steps and constraints.',
    '需要数值变量': 'Numeric variables required',
    '总量／线性约束需要至少一个数值变量。': 'A total / linear constraint needs at least one numeric variable.',
    '总量／线性约束': 'Total / linear constraint',
    '填写各变量的系数；总量约束将参与求和的变量设为 1，其余设为 0。': 'Enter coefficients. For a total constraint, set included variables to 1 and all others to 0.',
    '关系': 'Relation', '右侧数值（原始单位）': 'Right-hand value (original units)',
    '系数不能为空': 'Coefficients required', '至少一个变量的系数需要非零。': 'At least one coefficient must be nonzero.',
    '需要两个数值变量': 'Two numeric variables required',
    '配比约束需要两个不同的数值变量。': 'A ratio constraint needs two different numeric variables.',
    '配比范围': 'Ratio bounds', '分子': 'Numerator', '分母': 'Denominator',
    '最小配比': 'Minimum ratio', '最大配比': 'Maximum ratio',
    '导入合法候选表': 'Import allowed candidates', '候选表未导入': 'Candidate import failed',
    '请检查规则': 'Check the rules',
}

# Engine messages are localized at the presentation boundary. Keeping the engine
# sources untouched also keeps the proven Windows scientific runtime unchanged.
EN.update({
    '项目必须是对象。': 'The project must be a JSON object.',
    '项目必须是有效的 JSON 数据，且不能包含 NaN/Infinity。': 'The project must be valid JSON without NaN or Infinity.',
    '项目备注必须是文字。': 'Project notes must be text.',
    '项目历史必须是列表。': 'Project history must be a list.',
    '算法必须是 gryffin、atlas 或 bo-mcp。': 'Choose gryffin, atlas or bo-mcp as the engine.',
    '任务必须是 optimization 或 classification。': 'Task must be optimization or classification.',
    '多目标模式必须是 hierarchical 或 pareto。': 'Objective mode must be hierarchical or pareto.',
    '分类任务至少需要两个预定义标签。': 'Classification needs at least two predefined labels.',
    '分类标签不能重复。': 'Class labels must be unique.',
    '分类任务不能使用 Pareto 多目标模式。': 'Classification cannot use Pareto mode.',
    '至少设置一个实验参数。': 'Define at least one experiment variable.',
    '至少设置一个优化目标。': 'Define at least one objective.',
    '参数和目标名称必须各不相同。': 'Variable and objective names must all be unique.',
    '分类任务必须且只能设置一个标签列。': 'Classification requires exactly one label column.',
    'Pareto 优化至少需要两个数值目标。': 'Pareto optimization needs at least two numeric objectives.',
    'Atlas / BO-MCP 层级接口支持单目标；多目标请选择 Pareto + BO-MCP 或 Gryffin + Chimera。': 'The Atlas / BO-MCP hierarchical interface supports one objective. For multiple objectives choose Pareto + BO-MCP or Gryffin + Chimera.',
    '步长、候选表、配方约束、Pareto 和分类任务请明确选择 BO-MCP / BoTorch 引擎执行。': 'Select BO-MCP / BoTorch for steps, candidate lists, recipe constraints, Pareto and classification.',
    '候选表必须是参数记录列表。': 'The candidate list must contain variable records.',
    '候选表超过 200000 行，请缩小候选范围。': 'The candidate list exceeds 200000 rows. Reduce its size.',
    '候选表包含重复条件，请先去除重复记录。': 'Remove duplicate conditions before importing the candidate list.',
    '候选表包含重复或过于接近的条件（连续变量阈值为范围的 1e-6），请合并后导入。': 'Merge duplicate or near-identical candidates before importing (continuous threshold: 1e-6 of the range).',
    '待实验条件不在当前允许的候选表中。': 'A pending condition is outside the current allowed candidate list.',
    'pending 必须是记录列表。': 'pending must be a list of records.',
    '候选表没有数据行。': 'The candidate list has no data rows.',
    'BO-MCP 必须由独立的 Python 3.13 现代 worker 执行；不能在此经典优化器环境中运行。': 'BO-MCP requires the separate Python 3.13 modern worker.',
    '离散组合超过 200000 个，当前桌面接口暂不展开此规模；请缩小搜索范围。': 'More than 200000 discrete combinations. Reduce the search space.',
    'Atlas 混合域的离散组合超过 200000 个，请缩小搜索范围。': 'The Atlas mixed domain exceeds 200000 discrete combinations. Reduce the search space.',
    '配方约束必须是列表。': 'Recipe constraints must be a list.',
    '线性约束至少需要一个数值变量的系数。': 'A linear constraint needs a coefficient for at least one numeric variable.',
    '线性约束只能使用已定义的数值变量。': 'Linear constraints can use only defined numeric variables.',
    '线性约束系数不能全为零。': 'Linear coefficients cannot all be zero.',
    '线性约束关系必须是 eq、le 或 ge。': 'Linear relation must be eq, le or ge.',
    '约束容差必须为正数。': 'Constraint tolerance must be positive.',
    '配方约束与参数边界冲突，没有可行条件。': 'Recipe constraints conflict with variable bounds; no feasible conditions exist.',
    '配比约束的分母必须有大于零的允许值。': 'The ratio denominator must allow a positive value.',
    '配比约束至少设置一个上下限。': 'Set at least one ratio bound.',
    '配比上限不能小于下限。': 'The upper ratio bound cannot be below the lower bound.',
    '约束类型必须是 linear 或 ratio。': 'Constraint kind must be linear or ratio.',
    '单个变量的允许档位超过 200001 个，请增大步长。': 'A variable exceeds 200001 levels. Increase its step.',
    '等式约束相互冲突，没有可行候选条件。': 'Equality constraints conflict; no feasible candidates exist.',
    '候选池上限必须是 1–200000 的整数。': 'Candidate pool size must be an integer from 1 to 200000.',
    '有限配方空间超过 200000 组，请增大步长或导入预先筛选的候选表。': 'The finite recipe space exceeds 200000 combinations. Increase steps or import a filtered candidate list.',
    '等式约束与档位或边界冲突，没有可行候选条件。': 'Equality constraints conflict with levels or bounds; no feasible candidates exist.',
    '没有找到满足边界、步长和配方约束的候选条件；请检查约束，或导入合法候选表。': 'No candidates satisfy bounds, steps and recipe constraints. Check the rules or import allowed candidates.',
    '只支持 CSV、XLS 或 XLSX 文件。': 'Choose a CSV, XLS or XLSX file.',
    '当前安装包缺少 Excel 读取组件，请使用完整版或先另存为 CSV。': 'Excel support is missing. Install the full package or save the file as CSV.',
    'CSV 请保存为 UTF-8 编码，或直接导入 Excel 工作簿。': 'Save CSV in UTF-8 encoding, or import an Excel workbook.',
    'Excel 工作簿没有工作表。': 'The Excel workbook has no worksheets.',
    '工作簿包含多个工作表，请先选择需要导入的工作表。': 'Choose the worksheet to import from this multi-sheet workbook.',
    '选定的工作表不存在。': 'The selected worksheet does not exist.',
    '高斯过程返回非有限预测；未保存本次建议。': 'The Gaussian process returned non-finite predictions. Suggestions were not saved.',
    'Pareto 参考点必须为每个目标提供一个原单位数值。': 'Supply a Pareto reference value for every objective in its original units.',
    'Pareto 参考点必须为有限数字。': 'Pareto reference values must be finite numbers.',
    '用户给定；同一参考点用于整个历史曲线。': 'User-defined reference point, shared across the whole history.',
    '本次全部已测目标的最差值外加余量；本图历史统一用此点。自动参考点跨分析可能变化，跨轮比较请固定参考点。': 'Worst measured values plus a margin, shared across this history. Automatic reference points can change between analyses; fix the reference point for comparisons between rounds.',
    '尚无实测结果。': 'No measured results yet.',
    '采集函数返回非有限分值；请检查数据或搜索空间。': 'The acquisition function returned non-finite scores. Check the data and search space.',
    '至少三条实测记录才能进行留一验证。': 'Leave-one-out validation requires at least three measured records.',
    '此分析接口仅用于 BoTorch / 分类任务；经典引擎应走其原生分析接口。': 'This analysis interface supports BoTorch / classification; classic engines use their native interfaces.',
    '未知计算操作。': 'Unknown calculation operation.', '诊断选项必须为布尔值。': 'The diagnostic option must be Boolean.',
    '候选排序基于本次确定性生成/抽取的合法候选子集，不代表整个连续域或完整候选表的全局最优。': 'Ranking uses the feasible candidate subset generated / sampled for this analysis. It does not establish a global optimum over the continuous domain or the full candidate list.',
    '尚未观察到两个类别，当前执行合法候选域中的分散初始设计，不提供分类概率。': 'Fewer than two classes observed. Using a spread-out initial design in the feasible domain; no class probabilities are available.',
    '表中为考虑现有待实验条件的首轮单点采集分值；批内依次将新选择点加入 X_pending 后重新评分，推荐顺序可能不同于首轮排名。': 'The table shows first-round single-point acquisition scores accounting for existing pending experiments. Within a batch, selected points enter X_pending and scores are recomputed; selection order can differ from the initial ranking.',
    '少于两条实测结果，当前执行合法候选域中的分散初始设计，不提供后验预测。': 'Fewer than two measured results. Using a spread-out initial design in the feasible domain; no posterior predictions are available.',
    ' 部分留一折只剩一个训练类别，已跳过并计入 evaluated/total。': ' Some leave-one-out folds had only one training class; they were skipped and counted in evaluated/total.',
})

EN.update({
    '{v0} 必须是有限数字。': '{v0} must be a finite number.',
    '{v0} 不允许 NaN 或 Infinity。': '{v0} cannot be NaN or Infinity.',
    '{v0} 必须是 {v1}–{v2} 之间的整数。': '{v0} must be an integer from {v1} to {v2}.',
    '{v0} 必须是非空文字，且不能包含换行等控制字符。': '{v0} must be nonempty text without control characters.',
    '{v0} 必须是对象。': '{v0} must be an object.',
    '{v0} 包含未知字段：{v1}。': '{v0} has unknown fields: {v1}.',
    '{v0} 缺少字段：{v1}。': '{v0} is missing fields: {v1}.',
    '{v0} / {v1} 不在允许的类别中。': '{v0} / {v1} is not an allowed category.',
    '{v0} / {v1} 超出范围 [{v2}, {v3}]。': '{v0} / {v1} is outside [{v2}, {v3}].',
    '{v0} / {v1} 必须是整数。': '{v0} / {v1} must be an integer.',
    '{v0} / {v1} 不在以 {v2} 为起点、步长 {v3} 的允许档位上。': '{v0} / {v1} is not on an allowed level starting at {v2} with step {v3}.',
    '{v0} / {v1} 不在已定义的分类标签中。': '{v0} / {v1} is not a defined class label.',
    '{v0} 至少需要两个类别。': '{v0} needs at least two categories.',
    '{v0} 的类别不能重复。': 'Categories for {v0} must be unique.',
    '{v0} 上限必须大于下限，且跨度必须有限。': 'For {v0}, the upper bound must exceed the lower bound and the range must be finite.',
    '{v0} 整数范围超过 10001 个候选值，请缩小范围。': '{v0} exceeds 10001 integer candidates. Reduce the range.',
    '{v0} 的类型必须是 continuous、discrete 或 categorical。': 'The type of {v0} must be continuous, discrete or categorical.',
    '{v0} 类别变量不能设置数值步长。': '{v0} is categorical and cannot have a numeric step.',
    '{v0} 步长必须为正数，且档位数必须有限。': 'The step of {v0} must be positive with a finite number of levels.',
    '{v0} 整数变量的步长必须是整数。': 'The step of integer variable {v0} must be an integer.',
    '{v0} 的步长小于当前数值范围的浮点精度，请调整单位或增大步长。': 'The step of {v0} is below floating-point precision for this range. Change units or increase the step.',
    '{v0} 的步长生成超过 200001 个档位，请增大步长。': 'The step of {v0} creates more than 200001 levels. Increase the step.',
    '{v0} 单位必须是文字。': 'The unit of {v0} must be text.',
    '{v0} 的方向必须是 min 或 max。': 'The goal for {v0} must be min or max.',
    '{v0} 的相对容差必须在 0–1 之间。': 'The relative tolerance for {v0} must be between 0 and 1.',
    '{v0} 必须是记录列表。': '{v0} must be a list of records.',
    '{v0} 第 {v1} 行不满足配方约束。': 'Row {v1} in {v0} violates recipe constraints.',
    '待做实验第 {v0} 行与已测或其他待做实验重复/过于接近，请移除重复记录。': 'Pending row {v0} duplicates or is too close to a measured / pending condition. Remove the duplicate.',
    '结果表列名必须恰好是：{v0}。': 'Result column names must be exactly: {v0}.',
    '候选表只包含参数列：{v0}。': 'The candidate list must contain only these variable columns: {v0}.',
    '离散搜索空间只剩 {v0} 个未做且未排队的条件，少于请求的 {v1} 个；请缩小批量或扩展范围。': 'Only {v0} unmeasured, non-pending conditions remain, fewer than the requested {v1}. Reduce the batch or expand the range.',
    '{v0} 未能给出足够的不重复条件。尚未保存部分批次；请调整批量大小、种子或搜索范围。': '{v0} could not suggest enough distinct conditions. No partial batch was saved. Adjust batch size, seed or search space.',
    '约束 {v0} 必须是对象。': 'Constraint {v0} must be an object.',
    '不能读取 Excel 工作簿：{v0}': 'Could not read the Excel workbook: {v0}',
    '{v0} 不能为空。': '{v0} cannot be empty.',
    '{v0} 必须有非空文字列名。': '{v0} needs nonempty text column names.',
    '{v0} 列名不能重复。': 'Column names in {v0} must be unique.',
    '{v0} 第 {v1} 行列数过多。': 'Row {v1} in {v0} has too many columns.',
    '{v0} 第 {v1} 行有缺失单元格，请补齐后导入。': 'Row {v1} in {v0} has missing cells. Fill them before importing.',
    '不能读取工作表 {v0}：{v1}': 'Could not read worksheet {v0}: {v1}',
    '合法且未做的候选只剩 {v0} 个，少于请求的 {v1} 个。': 'Only {v0} feasible unmeasured candidates remain, fewer than the requested {v1}.',
    '为控制计算时间，对 {v0} 条记录中均匀选出的 30 条做留一预测；每折训练仍使用其余全部记录。': 'To limit calculation time, 30 evenly spaced records out of {v0} are evaluated with leave-one-out predictions. Every fold still trains on all other records.',
    '尚未观察到类别 {v0}；预测概率仅在已观察类别之间归一化，不能解释为未见类别的概率。': 'Classes not yet observed: {v0}. Probabilities are normalized over observed classes only and do not describe unseen classes.',
})

_language = 'zh-CN'
_initialized = False
_rendered = OrderedDict()
_reverse = {english: chinese for chinese, english in EN.items() if '{' not in chinese}
_patterns = []
for _source, _english in sorted(EN.items(), key=lambda pair: len(pair[0]), reverse=True):
    if '{v' in _source:
        _regex = ''
        for _literal, _field, _spec, _conversion in Formatter().parse(_source):
            _regex += re.escape(_literal)
            if _field:
                _regex += '(?P<' + _field + '>.*?)'
        _patterns.append((re.compile(_regex, re.DOTALL), _english))


class _Events(QObject):
    languageChanged = Signal()


events = _Events()


def language():
    return _language


def tr(source, **values):
    """Translate a UI template; substitutions are data and remain unchanged."""
    chinese = source.format(**values) if values else source
    english_template = EN.get(source, source)
    english = english_template.format(**values) if values else english_template
    _rendered[chinese] = _rendered[english] = (source, values)
    while len(_rendered) > 4096:
        _rendered.popitem(last=False)
    return english if _language == 'en' else chinese


def message(value):
    """Translate an already-rendered engine/error message at the UI boundary."""
    value = str(value)
    if value in _rendered:
        return tr(_rendered[value][0], **_rendered[value][1])
    if value in EN:
        return tr(value)
    if value in _reverse:
        return tr(_reverse[value])
    if _language == 'en':
        for pattern, english in _patterns:
            match = pattern.fullmatch(value)
            if match:
                return english.format(**match.groupdict())
        # Diagnostic messages may append this separate, fixed explanation.
        suffix = ' 部分留一折只剩一个训练类别，已跳过并计入 evaluated/total。'
        if value.endswith(suffix):
            return message(value[:-len(suffix)]) + tr(suffix)
    return value


class _QtTranslator(QTranslator):
    """Standard Qt buttons; user data never pass through Qt's translator."""
    words = {
        'OK': '确定', '&OK': '确定', 'Cancel': '取消', '&Cancel': '取消',
        'Close': '关闭', '&Close': '关闭', 'Save': '保存', '&Save': '保存',
        'Discard': '不保存', '&Discard': '不保存', 'Yes': '是', '&Yes': '是',
        'No': '否', '&No': '否', 'Open': '打开', '&Open': '打开',
        'Apply': '应用', '&Apply': '应用', 'Reset': '重置', 'Help': '帮助',
        'Show Details...': '显示详情…', 'Hide Details...': '隐藏详情…',
    }

    def isEmpty(self):
        return False

    def translate(self, context, sourceText, disambiguation=None, n=-1):
        return self.words.get(sourceText, '') if _language == 'zh-CN' else sourceText if sourceText in self.words else ''


_qt = _QtTranslator()


def initialize():
    global _initialized, _language
    if not _initialized:
        selected = os.environ.get('SYNTHBO_LANGUAGE') or QSettings('NaNoBO', 'NaNoBO').value('interface/language', 'zh-CN')
        _language = selected if selected in ('en', 'zh-CN') else 'zh-CN'
        _initialized = True
    app = QApplication.instance()
    if app:
        app.installTranslator(_qt)


def set_language(selected, *, persist=True):
    global _language, _initialized
    if selected not in ('en', 'zh-CN'):
        raise ValueError('Language must be en or zh-CN')
    _initialized = True
    if persist:
        QSettings('NaNoBO', 'NaNoBO').setValue('interface/language', selected)
    if selected != _language:
        _language = selected
        app = QApplication.instance()
        if app:
            app.removeTranslator(_qt)
            app.installTranslator(_qt)
        events.languageChanged.emit()


def localize(root):
    """Refresh known presentation properties, never editable data or data headers.

    Only explicitly marked choice boxes and header tables are localized. Thus a
    variable, class label or worksheet called e.g. “打开” remains exactly “打开”.
    Signals are blocked while replacing combo labels so the model stays intact.
    """
    for widget in [root] + root.findChildren(QWidget):
        if widget.property('i18nData'):
            continue
        for getter, setter in [('windowTitle', 'setWindowTitle'), ('toolTip', 'setToolTip'),
                               ('accessibleName', 'setAccessibleName'), ('placeholderText', 'setPlaceholderText')]:
            if hasattr(widget, getter):
                value = getattr(widget, getter)()
                if value:
                    getattr(widget, setter)(message(value))
        if isinstance(widget, (QLabel, QPushButton, QMenu)):
            if isinstance(widget, QMenu):
                widget.setTitle(message(widget.title()))
            else:
                widget.setText(message(widget.text()))
        if isinstance(widget, QPlainTextEdit) and widget.property('i18nText'):
            widget.setPlainText(message(widget.toPlainText()))
        if isinstance(widget, QComboBox) and widget.property('i18nChoices'):
            blocker = QSignalBlocker(widget)
            for index in range(widget.count()):
                widget.setItemText(index, message(widget.itemText(index)))
            del blocker
        if isinstance(widget, QTabWidget):
            for index in range(widget.count()):
                widget.setTabText(index, message(widget.tabText(index)))
        if isinstance(widget, QTableWidget) and widget.property('i18nHeaders'):
            for index in range(widget.columnCount()):
                header = widget.horizontalHeaderItem(index)
                if header:
                    header.setText(message(header.text()))
    for action in root.findChildren(QAction):
        action.setText(message(action.text()))
        action.setToolTip(message(action.toolTip()))

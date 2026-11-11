[简体中文](STEP_BY_STEP.zh-CN.md) | [English](STEP_BY_STEP.en.md)

# SynthBO 逐步截图指南

从安装后第一次打开开始。本页全部采用实际的英文界面截图，来自 macOS 应用和配套 **en/** 英文练习文件；Windows 应用中的共用功能操作一致，系统文件选择窗口的外观可能不同。安装步骤见[完整教程](TUTORIAL.zh-CN.md)。

**所有实验数值都是模拟数据。** 图表来自应用实际模型及验证输出。各节会打开对应的独立项目，切换练习时按文件名重新打开，不能把上个项目的设置直接套入下个练习。原始中文标签数据仍保留在 en/ 旁边。

## 启动与认识界面

### 01. 打开英文练习项目，认识项目设置、已完成结果、待实验条件和模型分析区域

打开英文练习项目，认识项目设置、已完成结果、待实验条件和模型分析区域。

![Step 01: actual English SynthBO interface](screenshots/steps/01-main-window.png)

### 02. 使用右上角 English / 中文 按钮

使用右上角 English / 中文 按钮。按钮文字表示可以切换到的语言；本图已经处于英文界面。

![Step 02: actual English SynthBO interface](screenshots/steps/02-language-button.png)

### 03. 打开 Help 菜单，找到中英文离线教程和 Export practice data 练习数据导出入口

打开 Help 菜单，找到中英文离线教程和 Export practice data 练习数据导出入口。

![Step 03: actual English SynthBO interface](screenshots/steps/03-help-menu.png)

### 04. 选择可写入的练习数据保存文件夹

选择可写入的练习数据保存文件夹。随后进入 en 子文件夹，使用与本教程截图相同的英文样例。

![Step 04: actual English SynthBO interface](screenshots/steps/04-export-practice-data.png)

## 完成第一次实验循环

### 05. 点击 Open，选择 en/01_quickstart/project.chembo.json

点击 Open，选择 en/01_quickstart/project.chembo.json。项目 JSON 通过打开功能载入，不作为结果表导入。

![Step 05: actual English SynthBO interface](screenshots/steps/05-open-project.png)

### 06. 检查已有 6 条完成结果、0 个待实验条件

检查已有 6 条完成结果、0 个待实验条件。本练习的所有数值都是模拟数据。

![Step 06: actual English SynthBO interface](screenshots/steps/06-six-measured-results.png)

### 07. 计算前检查 Task、Engine、本批实验数 2 和随机种子 42

计算前检查 Task、Engine、本批实验数 2 和随机种子 42。

![Step 07: actual English SynthBO interface](screenshots/steps/07-task-engine-batch-seed.png)

### 08. 点击 Analyze / validate

点击 Analyze / validate。等待实际引擎完成；计算时会出现进度和 Cancel 控件。

![Step 08: actual English SynthBO interface](screenshots/steps/08-calculating.png)

### 09. 打开 Models and plots → Prediction table

打开 Models and plots → Prediction table。练习 1 的首次分析应有 14 个未测候选。

![Step 09: actual English SynthBO interface](screenshots/steps/09-fourteen-candidate-predictions.png)

### 10. 选择 Model validation → Predicted vs measured

选择 Model validation → Predicted vs measured。6 条起始结果分别被留出验证。

![Step 10: actual English SynthBO interface](screenshots/steps/10-six-row-cross-validation.png)

### 11. 点击 Suggest next experiments

点击 Suggest next experiments。待实验页新增 2 个条件，完成结果仍为 6 条。

![Step 11: actual English SynthBO interface](screenshots/steps/11-two-pending-experiments.png)

### 12. 点击 Export pending CSV 保存 round-1-pending.csv；按所有变量共同匹配模拟答案表，只填写空的目标单元格

点击 Export pending CSV 保存 round-1-pending.csv；按所有变量共同匹配模拟答案表，只填写空的目标单元格。

![Step 12: actual English SynthBO interface](screenshots/steps/12-export-pending-csv.png)

### 13. 在表格软件中填好两条模拟结果后，从 Completed experiments → Import Excel / CSV 导入填好的文件

在表格软件中填好两条模拟结果后，从 Completed experiments → Import Excel / CSV 导入填好的文件。

![Step 13: actual English SynthBO interface](screenshots/steps/13-import-measured-csv.png)

### 14. 确认完成结果变为 8 条、待实验为 0

确认完成结果变为 8 条、待实验为 0。合法结果导入后，匹配的待实验条件会自动移除。

![Step 14: actual English SynthBO interface](screenshots/steps/14-eight-completed-zero-pending.png)

### 15. 以自己的文件名保存项目 JSON，保留设置、结果、待实验条件与当前分析，便于下次继续

以自己的文件名保存项目 JSON，保留设置、结果、待实验条件与当前分析，便于下次继续。

![Step 15: actual English SynthBO interface](screenshots/steps/15-save-project.png)

## 新建项目与录入结果

### 16. 点击 New 开始自己的课题

点击 New 开始自己的课题。填写项目名称，并修改或删除默认变量。

![Step 16: actual English SynthBO interface](screenshots/steps/16-new-project.png)

### 17. 设置连续、整数或类别变量；类别之间用竖线分隔

设置连续、整数或类别变量；类别之间用竖线分隔。横向滚动变量表可查看 Unit 和 Step。

![Step 17: actual English SynthBO interface](screenshots/steps/17-variable-types-and-steps.png)

### 18. 产率等指标选择 Maximize，成本或误差选择 Minimize

产率等指标选择 Maximize，成本或误差选择 Minimize。图中 Pareto 示例同时展示两种方向；备注可记录单位与数据来源。

![Step 18: actual English SynthBO interface](screenshots/steps/18-objective-goal-and-notes.png)

### 19. 练习导入时，先打开空项目，再导入一份 seed-observations 的 CSV、XLS 或 XLSX 文件

练习导入时，先打开空项目，再导入一份 seed-observations 的 CSV、XLS 或 XLSX 文件。

![Step 19: actual English SynthBO interface](screenshots/steps/19-import-excel.png)

### 20. 多工作表文件选择 Results；ReadMe 是说明页，不能作为实验结果导入

多工作表文件选择 Results；ReadMe 是说明页，不能作为实验结果导入。

![Step 20: actual English SynthBO interface](screenshots/steps/20-select-results-worksheet.png)

### 21. 点击 + Row 手工录入

点击 + Row 手工录入。保存或计算前填写全部变量和目标，未知结果不能用 0 代替。

![Step 21: actual English SynthBO interface](screenshots/steps/21-manual-experiment-row.png)

## 设置可执行配方空间

### 22. 打开配方练习，再点击 Constraints / candidates

打开配方练习，再点击 Constraints / candidates。列表显示当前启用的联合约束。

![Step 22: actual English SynthBO interface](screenshots/steps/22-recipe-rules.png)

### 23. 点击 + Total / linear；A_mL 与 B_mL 系数填 1，aging_min 填 0，关系选择等号，右侧数值填 1

点击 + Total / linear；A_mL 与 B_mL 系数填 1，aging_min 填 0，关系选择等号，右侧数值填 1。

![Step 23: actual English SynthBO interface](screenshots/steps/23-total-volume-rule.png)

### 24. 点击 + Ratio，选择分子、分母，再填写允许的最小与最大配比

点击 + Ratio，选择分子、分母，再填写允许的最小与最大配比。

![Step 24: actual English SynthBO interface](screenshots/steps/24-ratio-rule.png)

### 25. 使用 Import allowed candidates 导入只含变量列的候选表，表头必须与变量名一致

使用 Import allowed candidates 导入只含变量列的候选表，表头必须与变量名一致。

![Step 25: actual English SynthBO interface](screenshots/steps/25-import-candidates.png)

### 26. 检查候选数量及前 30 行预览，确认各项规则后点击 Apply (use BoTorch)

检查候选数量及前 30 行预览，确认各项规则后点击 Apply (use BoTorch)。

![Step 26: actual English SynthBO interface](screenshots/steps/26-allowed-candidate-preview.png)

### 27. 生成下一批并检查条件

生成下一批并检查条件。范围、步长、总量、配比和候选清单规则会同时执行。

![Step 27: actual English SynthBO interface](screenshots/steps/27-feasible-recipe-batch.png)

### 28. 分析剩余合法配方

分析剩余合法配方。横轴是候选编号，具体体积与老化时间从预测表读取。

![Step 28: actual English SynthBO interface](screenshots/steps/28-recipe-predictions.png)

## 设置 Pareto 多目标

### 29. 打开 Pareto 项目，确认任务类型及目标方向：产率最大化、成本最小化

打开 Pareto 项目，确认任务类型及目标方向：产率最大化、成本最小化。

![Step 29: actual English SynthBO interface](screenshots/steps/29-pareto-objective-settings.png)

### 30. 分析 6 条起始结果

分析 6 条起始结果。示例有 22 个未测候选，每个目标都有独立的预测列。

![Step 30: actual English SynthBO interface](screenshots/steps/30-pareto-prediction-table.png)

### 31. 选择 Pareto optimization → 2D Pareto，为 X、Y 选择不同目标

选择 Pareto optimization → 2D Pareto，为 X、Y 选择不同目标。绿色点是已完成结果中的非支配方案。

![Step 31: actual English SynthBO interface](screenshots/steps/31-pareto-trade-offs.png)

### 32. 选择 Hypervolume history

选择 Hypervolume history。同一历史曲线使用同一参考点；跨轮比较时应固定参考点。

![Step 32: actual English SynthBO interface](screenshots/steps/32-hypervolume-history.png)

### 33. 打开三目标变体并分析，再选择 3D Pareto，为三个坐标轴选择不同目标

打开三目标变体并分析，再选择 3D Pareto，为三个坐标轴选择不同目标。

![Step 33: actual English SynthBO interface](screenshots/steps/33-three-dimensional-pareto.png)

## 使用分类主动学习

### 34. 打开形貌项目，确认 Classification active learning，以及 Aggregated、Spheres、Rods 三个标签

打开形貌项目，确认 Classification active learning，以及 Aggregated、Spheres、Rods 三个标签。

![Step 34: actual English SynthBO interface](screenshots/steps/34-classification-label-settings.png)

### 35. 分析后打开 Classification → Candidate class probabilities

分析后打开 Classification → Candidate class probabilities。每根柱子是模型概率分布，不是实测形貌图像。

![Step 35: actual English SynthBO interface](screenshots/steps/35-class-probabilities.png)

### 36. 选择 Classification uncertainty

选择 Classification uncertainty。熵越高，表示分类器对该候选所属类别越不确定。

![Step 36: actual English SynthBO interface](screenshots/steps/36-classification-entropy.png)

### 37. 选择 Measured class counts，仅统计已完成且带标签的记录，包含重复实验

选择 Measured class counts，仅统计已完成且带标签的记录，包含重复实验。

![Step 37: actual English SynthBO interface](screenshots/steps/37-measured-class-counts.png)

### 38. 选择 Confusion matrix

选择 Confusion matrix。行是留出的已记录标签，列是预测标签；本模拟示例预测正确 3/6。

![Step 38: actual English SynthBO interface](screenshots/steps/38-held-out-confusion-matrix.png)

### 39. 打开 binary-project.chembo.json，以 outcome 目标列记录 Success 或 Failure

打开 binary-project.chembo.json，以 outcome 目标列记录 Success 或 Failure。

![Step 39: actual English SynthBO interface](screenshots/steps/39-success-failure-labels.png)

### 40. 分析二分类项目，查看两种标签的概率；应导入对应的二分类结果表，不使用形貌表

分析二分类项目，查看两种标签的概率；应导入对应的二分类结果表，不使用形貌表。

![Step 40: actual English SynthBO interface](screenshots/steps/40-binary-class-probabilities.png)

### 41. 尚无已记录类别时，建议属于初始实验设计；界面会明确说明没有已训练的类别概率

尚无已记录类别时，建议属于初始实验设计；界面会明确说明没有已训练的类别概率。

![Step 41: actual English SynthBO interface](screenshots/steps/41-initial-design-without-probabilities.png)

## 阅读各类数值图表

### 42. 选择 Predictions → Predictions & intervals

选择 Predictions → Predictions & intervals。点是模型均值，阴影是模型区间，有本批推荐时以星号标记。

![Step 42: actual English SynthBO interface](screenshots/steps/42-prediction-intervals.png)

### 43. 选择 Mean & uncertainty，比较预测均值和模型标准差

选择 Mean & uncertainty，比较预测均值和模型标准差。

![Step 43: actual English SynthBO interface](screenshots/steps/43-mean-and-uncertainty.png)

### 44. 选择 Acquisition ranking

选择 Acquisition ranking。分值仅在本次分析内比较；批内加入新的待实验点后，推荐次序可能变化。

![Step 44: actual English SynthBO interface](screenshots/steps/44-acquisition-ranking.png)

### 45. 选择 Model validation → Predicted vs measured，从同一次留出验证读取 RMSE、MAE 和 R²

选择 Model validation → Predicted vs measured，从同一次留出验证读取 RMSE、MAE 和 R²。

![Step 45: actual English SynthBO interface](screenshots/steps/45-predicted-versus-measured.png)

### 46. 选择 Validation residuals

选择 Validation residuals。大于 0 为预测偏高，小于 0 为预测偏低。

![Step 46: actual English SynthBO interface](screenshots/steps/46-validation-residuals.png)

### 47. 选择 Data distribution → Measured distribution，再选择变量或目标

选择 Data distribution → Measured distribution，再选择变量或目标。

![Step 47: actual English SynthBO interface](screenshots/steps/47-measured-data-distribution.png)

### 48. 对数值目标选择 Measurement history

对数值目标选择 Measurement history。折线表示历史最佳完成值，记录顺序不等于真实时间间隔。

![Step 48: actual English SynthBO interface](screenshots/steps/48-best-measured-history.png)

### 49. 点击预测点，在图下方查看精确变量条件；工具栏可平移、缩放和还原

点击预测点，在图下方查看精确变量条件；工具栏可平移、缩放和还原。

![Step 49: actual English SynthBO interface](screenshots/steps/49-inspect-a-candidate.png)

## 保存与导出

### 50. 先选择所需图，再点击 Export chart，导出 PNG、PDF 或 SVG；文件会包含模型与解释文字

先选择所需图，再点击 Export chart，导出 PNG、PDF 或 SVG；文件会包含模型与解释文字。

![Step 50: actual English SynthBO interface](screenshots/steps/50-export-chart-png-pdf-svg.png)

### 51. 使用 Export predictions CSV 导出所有候选条件及模型输出，不能把它作为实测结果导入

使用 Export predictions CSV 导出所有候选条件及模型输出，不能把它作为实测结果导入。

![Step 51: actual English SynthBO interface](screenshots/steps/51-export-prediction-table.png)

### 52. 使用 File → Save project as 另存项目，保留原文件

使用 File → Save project as 另存项目，保留原文件。

![Step 52: actual English SynthBO interface](screenshots/steps/52-file-menu.png)

### 53. 使用 Completed experiments → Export results 导出完成结果，与待实验表、预测表分开

使用 Completed experiments → Export results 导出完成结果，与待实验表、预测表分开。

![Step 53: actual English SynthBO interface](screenshots/steps/53-export-measured-results.png)

## 转入与撤回待实验条件

### 54. 先选中待实验行，再执行转入或撤回

先选中待实验行，再执行转入或撤回。示例开始时为 6 条完成结果和 2 个固定待实验条件。

![Step 54: actual English SynthBO interface](screenshots/steps/54-select-pending-condition.png)

### 55. 点击 Move selected to results，填写空的目标单元格后保存；验证通过后匹配的待实验条件会自动对齐

点击 Move selected to results，填写空的目标单元格后保存；验证通过后匹配的待实验条件会自动对齐。

![Step 55: actual English SynthBO interface](screenshots/steps/55-move-condition-to-results.png)

### 56. 点击 Withdraw selected 撤回不再执行的条件，不会把它变成已完成实验

点击 Withdraw selected 撤回不再执行的条件，不会把它变成已完成实验。

![Step 56: actual English SynthBO interface](screenshots/steps/56-withdraw-pending-condition.png)

## 取消计算、科研来源与原生引擎

### 57. 计算时打开 Run log 查看进度

计算时打开 Run log 查看进度。Cancel 可停止引擎，上游诊断日志保留原文。

![Step 57: actual English SynthBO interface](screenshots/steps/57-calculation-log-and-cancel.png)

### 58. 取消后原有完成结果与待实验记录保留

取消后原有完成结果与待实验记录保留。准备好后可重新计算，不会接收已取消的部分输出。

![Step 58: actual English SynthBO interface](screenshots/steps/58-cancelled-records-preserved.png)

### 59. 打开 About / licenses 查看科研来源、许可与引用说明；Open bundled licenses 可打开随附文件

打开 About / licenses 查看科研来源、许可与引用说明；Open bundled licenses 可打开随附文件。

![Step 59: actual English SynthBO interface](screenshots/steps/59-about-and-scientific-licenses.png)

### 60. 打开 Gryffin 项目使用其原生推荐；该变体去除了步长和有限候选清单

打开 Gryffin 项目使用其原生推荐；该变体去除了步长和有限候选清单。

![Step 60: actual English SynthBO interface](screenshots/steps/60-gryffin-native-engine.png)

### 61. 打开 Atlas 项目使用原生高斯过程推荐；需要本应用的图形诊断时使用 BoTorch 项目

打开 Atlas 项目使用原生高斯过程推荐；需要本应用的图形诊断时使用 BoTorch 项目。

![Step 61: actual English SynthBO interface](screenshots/steps/61-atlas-native-engine.png)

### 62. Gryffin 配合 Chimera 时，按优先级排列数值目标并设置相对容差；这与 Pareto 优化不同

Gryffin 配合 Chimera 时，按优先级排列数值目标并设置相对容差；这与 Pareto 优化不同。

![Step 62: actual English SynthBO interface](screenshots/steps/62-gryffin-objective-priorities.png)

### 63. Examples 可打开四个内置小示例；要复现上面的准确行数检查点，应使用 en 下的配套文件练习

Examples 可打开四个内置小示例；要复现上面的准确行数检查点，应使用 en 下的配套文件练习。

![Step 63: actual English SynthBO interface](screenshots/steps/63-built-in-workflow-examples.png)

### 64. 使用 Guide 重新打开当前界面语言的教程

使用 Guide 重新打开当前界面语言的教程。软件会记住语言选择，不改动实验数据。

![Step 64: actual English SynthBO interface](screenshots/steps/64-english-interface.png)

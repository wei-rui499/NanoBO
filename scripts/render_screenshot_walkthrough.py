"""Write parallel Chinese/English guides from the actual tutorial screenshots."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEPS = '''
01-main-window|Open the English practice project and find the project settings, measured results, pending conditions and model tabs.|打开英文练习项目，认识项目设置、已完成结果、待实验条件和模型分析区域。
02-language-button|Use the top-right English / 中文 button. It names the language you can switch to; this screenshot is already in English.|使用右上角 English / 中文 按钮。按钮文字表示可以切换到的语言；本图已经处于英文界面。
03-help-menu|Open Help to find both offline tutorials and Export practice data.|打开 Help 菜单，找到中英文离线教程和 Export practice data 练习数据导出入口。
04-export-practice-data|Choose a writable folder for the practice data. Enter its en folder to use the English-labeled copies shown here.|选择可写入的练习数据保存文件夹。随后进入 en 子文件夹，使用与本教程截图相同的英文样例。
05-open-project|Click Open and choose en/01_quickstart/project.chembo.json. Open a project JSON; do not import it as a result table.|点击 Open，选择 en/01_quickstart/project.chembo.json。项目 JSON 通过打开功能载入，不作为结果表导入。
06-six-measured-results|Check for 6 completed results and 0 pending experiments. All values in this practice project are synthetic.|检查已有 6 条完成结果、0 个待实验条件。本练习的所有数值都是模拟数据。
07-task-engine-batch-seed|Check Task, Engine, Experiments per batch = 2 and Random seed = 42 before calculating.|计算前检查 Task、Engine、本批实验数 2 和随机种子 42。
08-calculating|Click Analyze / validate. Wait for the calculation to finish; the progress and Cancel controls appear while a real worker runs.|点击 Analyze / validate。等待实际引擎完成；计算时会出现进度和 Cancel 控件。
09-fourteen-candidate-predictions|Open Models and plots → Prediction table. The initial quickstart analysis contains 14 unmeasured candidates.|打开 Models and plots → Prediction table。练习 1 的首次分析应有 14 个未测候选。
10-six-row-cross-validation|Select Model validation → Predicted vs measured. The 6 seed results are each held out for validation.|选择 Model validation → Predicted vs measured。6 条起始结果分别被留出验证。
11-two-pending-experiments|Click Suggest next experiments. The Pending tab now contains 2 conditions; the completed count remains 6.|点击 Suggest next experiments。待实验页新增 2 个条件，完成结果仍为 6 条。
12-export-pending-csv|Click Export pending CSV and save round-1-pending.csv. Fill only its empty objective cells using exact matching rows in the simulated answer table.|点击 Export pending CSV 保存 round-1-pending.csv；按所有变量共同匹配模拟答案表，只填写空的目标单元格。
13-import-measured-csv|After adding the two simulated results in your spreadsheet, use Completed experiments → Import Excel / CSV to import that completed file.|在表格软件中填好两条模拟结果后，从 Completed experiments → Import Excel / CSV 导入填好的文件。
14-eight-completed-zero-pending|Confirm 8 completed results and 0 pending conditions. Matching pending rows disappear automatically after valid results are imported.|确认完成结果变为 8 条、待实验为 0。合法结果导入后，匹配的待实验条件会自动移除。
15-save-project|Save a project JSON under your own name. This preserves settings, measurements, pending conditions and current analysis for later use.|以自己的文件名保存项目 JSON，保留设置、结果、待实验条件与当前分析，便于下次继续。
16-new-project|Click New to begin your own study. Set a meaningful project name and edit or remove the default variables.|点击 New 开始自己的课题。填写项目名称，并修改或删除默认变量。
17-variable-types-and-steps|Define continuous, integer and categorical variables. Use vertical bars between categories. Scroll the variable table horizontally to see Unit and Step.|设置连续、整数或类别变量；类别之间用竖线分隔。横向滚动变量表可查看 Unit 和 Step。
18-objective-goal-and-notes|Use Maximize for a response such as yield and Minimize for a cost or error. The Pareto example shows both directions; notes can record units and data sources.|产率等指标选择 Maximize，成本或误差选择 Minimize。图中 Pareto 示例同时展示两种方向；备注可记录单位与数据来源。
19-import-excel|For a clean import exercise, open the empty project and import ONE seed-observations CSV, XLS or XLSX file.|练习导入时，先打开空项目，再导入一份 seed-observations 的 CSV、XLS 或 XLSX 文件。
20-select-results-worksheet|For a multi-sheet workbook, choose Results. ReadMe is an explanation sheet and must not be imported as experiments.|多工作表文件选择 Results；ReadMe 是说明页，不能作为实验结果导入。
21-manual-experiment-row|Click + Row for manual entry. Fill every variable and objective before saving or calculating; an empty result is not zero.|点击 + Row 手工录入。保存或计算前填写全部变量和目标，未知结果不能用 0 代替。
22-recipe-rules|Open the recipe exercise, then Constraints / candidates. Existing joint constraints appear in the list.|打开配方练习，再点击 Constraints / candidates。列表显示当前启用的联合约束。
23-total-volume-rule|Click + Total / linear. Set A_mL and B_mL coefficients to 1, aging_min to 0, relation = and the right-hand value to 1.|点击 + Total / linear；A_mL 与 B_mL 系数填 1，aging_min 填 0，关系选择等号，右侧数值填 1。
24-ratio-rule|Click + Ratio. Choose the numerator and denominator, then set minimum and maximum permitted ratios.|点击 + Ratio，选择分子、分母，再填写允许的最小与最大配比。
25-import-candidates|Use Import allowed candidates for a table containing variable columns only. Its headers must match the variable names.|使用 Import allowed candidates 导入只含变量列的候选表，表头必须与变量名一致。
26-allowed-candidate-preview|Review the candidate count and first 30 rows. Click Apply (use BoTorch) after checking every rule.|检查候选数量及前 30 行预览，确认各项规则后点击 Apply (use BoTorch)。
27-feasible-recipe-batch|Generate a batch and inspect its conditions. Bounds, steps, total, ratio and candidate-list rules are applied together.|生成下一批并检查条件。范围、步长、总量、配比和候选清单规则会同时执行。
28-recipe-predictions|Analyze the remaining feasible recipes. The horizontal axis is candidate ID; read volumes and aging times from the prediction table.|分析剩余合法配方。横轴是候选编号，具体体积与老化时间从预测表读取。
29-pareto-objective-settings|Open the Pareto project. Confirm the Pareto task and each objective direction: yield up, cost down.|打开 Pareto 项目，确认任务类型及目标方向：产率最大化、成本最小化。
30-pareto-prediction-table|Analyze the 6 starting results. The example has 22 unmeasured candidates and separate predictions for each objective.|分析 6 条起始结果。示例有 22 个未测候选，每个目标都有独立的预测列。
31-pareto-trade-offs|Choose Pareto optimization → 2D Pareto and different X/Y objectives. Green points are measured non-dominated alternatives.|选择 Pareto optimization → 2D Pareto，为 X、Y 选择不同目标。绿色点是已完成结果中的非支配方案。
32-hypervolume-history|Choose Hypervolume history. Compare history using one reference point; keep it fixed when comparing separate rounds.|选择 Hypervolume history。同一历史曲线使用同一参考点；跨轮比较时应固定参考点。
33-three-dimensional-pareto|Open the three-objective variant, analyze, then select 3D Pareto and three different axes.|打开三目标变体并分析，再选择 3D Pareto，为三个坐标轴选择不同目标。
34-classification-label-settings|Open the morphology project. Confirm Classification active learning and Aggregated / Spheres / Rods labels.|打开形貌项目，确认 Classification active learning，以及 Aggregated、Spheres、Rods 三个标签。
35-class-probabilities|Analyze and open Classification → Candidate class probabilities. Each bar describes a model probability distribution, not a measured image.|分析后打开 Classification → Candidate class probabilities。每根柱子是模型概率分布，不是实测形貌图像。
36-classification-entropy|Choose Classification uncertainty. Higher entropy means the classifier is less certain about a candidate's class.|选择 Classification uncertainty。熵越高，表示分类器对该候选所属类别越不确定。
37-measured-class-counts|Choose Measured class counts. These counts include completed labeled records only, including replicates.|选择 Measured class counts，仅统计已完成且带标签的记录，包含重复实验。
38-held-out-confusion-matrix|Choose Confusion matrix. Rows are held-out measured labels and columns are predictions; this synthetic example scores 3/6.|选择 Confusion matrix。行是留出的已记录标签，列是预测标签；本模拟示例预测正确 3/6。
39-success-failure-labels|Open binary-project.chembo.json to use Success / Failure with the outcome target column.|打开 binary-project.chembo.json，以 outcome 目标列记录 Success 或 Failure。
40-binary-class-probabilities|Analyze the binary project to inspect two-label probabilities. Import its binary result table, not the morphology table.|分析二分类项目，查看两种标签的概率；应导入对应的二分类结果表，不使用形貌表。
41-initial-design-without-probabilities|With no measured classes, suggestions are an initial design. The app explicitly shows that trained probabilities are unavailable.|尚无已记录类别时，建议属于初始实验设计；界面会明确说明没有已训练的类别概率。
42-prediction-intervals|Choose Predictions → Predictions & intervals. Dots are model means, shaded bands are model intervals, and stars mark this batch when available.|选择 Predictions → Predictions & intervals。点是模型均值，阴影是模型区间，有本批推荐时以星号标记。
43-mean-and-uncertainty|Choose Mean & uncertainty to compare predicted means with model standard deviations.|选择 Mean & uncertainty，比较预测均值和模型标准差。
44-acquisition-ranking|Choose Acquisition ranking. Scores are comparable within this analysis; batch selection can change after each pending point.|选择 Acquisition ranking。分值仅在本次分析内比较；批内加入新的待实验点后，推荐次序可能变化。
45-predicted-versus-measured|Choose Model validation → Predicted vs measured. Read RMSE, MAE and R² from the same held-out validation.|选择 Model validation → Predicted vs measured，从同一次留出验证读取 RMSE、MAE 和 R²。
46-validation-residuals|Choose Validation residuals. Values above zero are overpredictions; values below zero are underpredictions.|选择 Validation residuals。大于 0 为预测偏高，小于 0 为预测偏低。
47-measured-data-distribution|Choose Data distribution → Measured distribution, then select a variable or objective.|选择 Data distribution → Measured distribution，再选择变量或目标。
48-best-measured-history|Choose Measurement history for a numeric objective. The line tracks the best completed value; record order is not elapsed time.|对数值目标选择 Measurement history。折线表示历史最佳完成值，记录顺序不等于真实时间间隔。
49-inspect-a-candidate|Click a prediction point to display its exact variable conditions below the plot. Use the toolbar to pan, zoom and reset.|点击预测点，在图下方查看精确变量条件；工具栏可平移、缩放和还原。
50-export-chart-png-pdf-svg|Select the required chart, then Export chart. Choose PNG, PDF or SVG; explanatory model text is included.|先选择所需图，再点击 Export chart，导出 PNG、PDF 或 SVG；文件会包含模型与解释文字。
51-export-prediction-table|Use Export predictions CSV for all candidate conditions and model outputs. Do not import this as measured data.|使用 Export predictions CSV 导出所有候选条件及模型输出，不能把它作为实测结果导入。
52-file-menu|Use File → Save project as to preserve another project copy without replacing the original.|使用 File → Save project as 另存项目，保留原文件。
53-export-measured-results|Use Completed experiments → Export results for measured rows. This differs from exporting pending or predicted rows.|使用 Completed experiments → Export results 导出完成结果，与待实验表、预测表分开。
54-select-pending-condition|Select a pending row before moving or withdrawing it. The example starts with 6 completed and 2 fixed pending conditions.|先选中待实验行，再执行转入或撤回。示例开始时为 6 条完成结果和 2 个固定待实验条件。
55-move-condition-to-results|Click Move selected to results. Fill the blank objective cells, then save; matching pending conditions reconcile after validation.|点击 Move selected to results，填写空的目标单元格后保存；验证通过后匹配的待实验条件会自动对齐。
56-withdraw-pending-condition|Click Withdraw selected to remove an unneeded pending condition without treating it as a measured experiment.|点击 Withdraw selected 撤回不再执行的条件，不会把它变成已完成实验。
57-calculation-log-and-cancel|Open Run log while computing. Cancel stops the worker; upstream diagnostic lines keep their original language.|计算时打开 Run log 查看进度。Cancel 可停止引擎，上游诊断日志保留原文。
58-cancelled-records-preserved|After cancellation, the existing measured and pending records remain. Re-run when ready; cancelled partial results are not accepted.|取消后原有完成结果与待实验记录保留。准备好后可重新计算，不会接收已取消的部分输出。
59-about-and-scientific-licenses|Open About / licenses for scientific authorship, licensing and citation instructions; Open bundled licenses opens the accompanying files.|打开 About / licenses 查看科研来源、许可与引用说明；Open bundled licenses 可打开随附文件。
60-gryffin-native-engine|Open the Gryffin project to use its native recommendations. This variant removes steps and the finite candidate list.|打开 Gryffin 项目使用其原生推荐；该变体去除了步长和有限候选清单。
61-atlas-native-engine|Open the Atlas project for native Gaussian-process suggestions. Use the BoTorch project for the app's plotted diagnostics.|打开 Atlas 项目使用原生高斯过程推荐；需要本应用的图形诊断时使用 BoTorch 项目。
62-gryffin-objective-priorities|For Gryffin with Chimera, order numeric objectives by priority and set their relative tolerances. This is different from Pareto optimization.|Gryffin 配合 Chimera 时，按优先级排列数值目标并设置相对容差；这与 Pareto 优化不同。
63-built-in-workflow-examples|Examples opens four small built-in workflows. Use the file-based en exercises for the exact row-count checkpoints above.|Examples 可打开四个内置小示例；要复现上面的准确行数检查点，应使用 en 下的配套文件练习。
64-english-interface|Use Guide to reopen the tutorial in the current interface language. Your language preference is remembered without changing experiment data.|使用 Guide 重新打开当前界面语言的教程。软件会记住语言选择，不改动实验数据。
'''.strip()

GROUPS = {
    1: ('Start and find the controls', '启动与认识界面'),
    5: ('Complete the first experiment loop', '完成第一次实验循环'),
    16: ('Create projects and import measurements', '新建项目与录入结果'),
    22: ('Executable recipe constraints', '设置可执行配方空间'),
    29: ('Pareto objectives and trade-offs', '设置 Pareto 多目标'),
    34: ('Classification active learning', '使用分类主动学习'),
    42: ('Read every numerical chart', '阅读各类数值图表'),
    50: ('Save and export', '保存与导出'),
    54: ('Move and withdraw pending conditions', '转入与撤回待实验条件'),
    57: ('Cancel, licenses and native engines', '取消计算、科研来源与原生引擎'),
}


def main():
    for language, column in [('en', 1), ('zh-CN', 2)]:
        english = language == 'en'
        text = '[简体中文](STEP_BY_STEP.zh-CN.md) | [English](STEP_BY_STEP.en.md)\n\n'
        text += '# SynthBO: step-by-step screenshots\n\n' if english else '# SynthBO 逐步截图指南\n\n'
        text += ('Start after installing the app. These are actual English-interface screenshots captured on macOS with the supplied **en/** practice files; the shared app controls also apply to Windows, while system file pickers can look different. Installation instructions are in the [detailed tutorial](TUTORIAL.en.md).\n\n'
                 '**All experiment values are synthetic.** Model and validation charts are actual application outputs. Each section opens its own named project; follow the file names instead of carrying an unrelated project into the next exercise. Original Chinese-labeled examples remain available alongside en/.\n\n') if english else (
                 '从安装后第一次打开开始。本页全部采用实际的英文界面截图，来自 macOS 应用和配套 **en/** 英文练习文件；Windows 应用中的共用功能操作一致，系统文件选择窗口的外观可能不同。安装步骤见[完整教程](TUTORIAL.zh-CN.md)。\n\n'
                 '**所有实验数值都是模拟数据。** 图表来自应用实际模型及验证输出。各节会打开对应的独立项目，切换练习时按文件名重新打开，不能把上个项目的设置直接套入下个练习。原始中文标签数据仍保留在 en/ 旁边。\n\n')
        for index, line in enumerate(STEPS.splitlines(), 1):
            stem, en, zh = line.split('|', 2)
            if index in GROUPS:
                text += '## ' + GROUPS[index][0 if english else 1] + '\n\n'
            title = en.split('. ')[0] if english else zh.split('。')[0]
            text += f'### {index:02d}. {title}\n\n' + (en if english else zh) + '\n\n'
            text += f'![Step {index:02d}: actual English SynthBO interface](screenshots/steps/{stem}.png)\n\n'
        (ROOT / 'docs' / ('STEP_BY_STEP.' + language + '.md')).write_text(text.rstrip() + '\n')
    print('Wrote two screenshot guides with 64 actual English UI steps each.')


if __name__ == '__main__':
    main()

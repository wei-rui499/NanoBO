[简体中文](STEP_BY_STEP.zh-CN.md) | [English](STEP_BY_STEP.en.md)

# SynthBO: step-by-step screenshots

Start after installing the app. These are actual English-interface screenshots captured on macOS with the supplied **en/** practice files; the shared app controls also apply to Windows, while system file pickers can look different. Installation instructions are in the [detailed tutorial](TUTORIAL.en.md).

**All experiment values are synthetic.** Model and validation charts are actual application outputs. Each section opens its own named project; follow the file names instead of carrying an unrelated project into the next exercise. Original Chinese-labeled examples remain available alongside en/.

## Start and find the controls

### 01. Open the English practice project and find the project settings, measured results, pending conditions and model tabs.

Open the English practice project and find the project settings, measured results, pending conditions and model tabs.

![Step 01: actual English SynthBO interface](screenshots/steps/01-main-window.png)

### 02. Use the top-right English / 中文 button

Use the top-right English / 中文 button. It names the language you can switch to; this screenshot is already in English.

![Step 02: actual English SynthBO interface](screenshots/steps/02-language-button.png)

### 03. Open Help to find both offline tutorials and Export practice data.

Open Help to find both offline tutorials and Export practice data.

![Step 03: actual English SynthBO interface](screenshots/steps/03-help-menu.png)

### 04. Choose a writable folder for the practice data

Choose a writable folder for the practice data. Enter its en folder to use the English-labeled copies shown here.

![Step 04: actual English SynthBO interface](screenshots/steps/04-export-practice-data.png)

## Complete the first experiment loop

### 05. Click Open and choose en/01_quickstart/project.chembo.json

Click Open and choose en/01_quickstart/project.chembo.json. Open a project JSON; do not import it as a result table.

![Step 05: actual English SynthBO interface](screenshots/steps/05-open-project.png)

### 06. Check for 6 completed results and 0 pending experiments

Check for 6 completed results and 0 pending experiments. All values in this practice project are synthetic.

![Step 06: actual English SynthBO interface](screenshots/steps/06-six-measured-results.png)

### 07. Check Task, Engine, Experiments per batch = 2 and Random seed = 42 before calculating.

Check Task, Engine, Experiments per batch = 2 and Random seed = 42 before calculating.

![Step 07: actual English SynthBO interface](screenshots/steps/07-task-engine-batch-seed.png)

### 08. Click Analyze / validate

Click Analyze / validate. Wait for the calculation to finish; the progress and Cancel controls appear while a real worker runs.

![Step 08: actual English SynthBO interface](screenshots/steps/08-calculating.png)

### 09. Open Models and plots → Prediction table

Open Models and plots → Prediction table. The initial quickstart analysis contains 14 unmeasured candidates.

![Step 09: actual English SynthBO interface](screenshots/steps/09-fourteen-candidate-predictions.png)

### 10. Select Model validation → Predicted vs measured

Select Model validation → Predicted vs measured. The 6 seed results are each held out for validation.

![Step 10: actual English SynthBO interface](screenshots/steps/10-six-row-cross-validation.png)

### 11. Click Suggest next experiments

Click Suggest next experiments. The Pending tab now contains 2 conditions; the completed count remains 6.

![Step 11: actual English SynthBO interface](screenshots/steps/11-two-pending-experiments.png)

### 12. Click Export pending CSV and save round-1-pending.csv

Click Export pending CSV and save round-1-pending.csv. Fill only its empty objective cells using exact matching rows in the simulated answer table.

![Step 12: actual English SynthBO interface](screenshots/steps/12-export-pending-csv.png)

### 13. After adding the two simulated results in your spreadsheet, use Completed experiments → Import Excel / CSV to import that completed file.

After adding the two simulated results in your spreadsheet, use Completed experiments → Import Excel / CSV to import that completed file.

![Step 13: actual English SynthBO interface](screenshots/steps/13-import-measured-csv.png)

### 14. Confirm 8 completed results and 0 pending conditions

Confirm 8 completed results and 0 pending conditions. Matching pending rows disappear automatically after valid results are imported.

![Step 14: actual English SynthBO interface](screenshots/steps/14-eight-completed-zero-pending.png)

### 15. Save a project JSON under your own name

Save a project JSON under your own name. This preserves settings, measurements, pending conditions and current analysis for later use.

![Step 15: actual English SynthBO interface](screenshots/steps/15-save-project.png)

## Create projects and import measurements

### 16. Click New to begin your own study

Click New to begin your own study. Set a meaningful project name and edit or remove the default variables.

![Step 16: actual English SynthBO interface](screenshots/steps/16-new-project.png)

### 17. Define continuous, integer and categorical variables

Define continuous, integer and categorical variables. Use vertical bars between categories. Scroll the variable table horizontally to see Unit and Step.

![Step 17: actual English SynthBO interface](screenshots/steps/17-variable-types-and-steps.png)

### 18. Use Maximize for a response such as yield and Minimize for a cost or error

Use Maximize for a response such as yield and Minimize for a cost or error. The Pareto example shows both directions; notes can record units and data sources.

![Step 18: actual English SynthBO interface](screenshots/steps/18-objective-goal-and-notes.png)

### 19. For a clean import exercise, open the empty project and import ONE seed-observations CSV, XLS or XLSX file.

For a clean import exercise, open the empty project and import ONE seed-observations CSV, XLS or XLSX file.

![Step 19: actual English SynthBO interface](screenshots/steps/19-import-excel.png)

### 20. For a multi-sheet workbook, choose Results

For a multi-sheet workbook, choose Results. ReadMe is an explanation sheet and must not be imported as experiments.

![Step 20: actual English SynthBO interface](screenshots/steps/20-select-results-worksheet.png)

### 21. Click + Row for manual entry

Click + Row for manual entry. Fill every variable and objective before saving or calculating; an empty result is not zero.

![Step 21: actual English SynthBO interface](screenshots/steps/21-manual-experiment-row.png)

## Executable recipe constraints

### 22. Open the recipe exercise, then Constraints / candidates

Open the recipe exercise, then Constraints / candidates. Existing joint constraints appear in the list.

![Step 22: actual English SynthBO interface](screenshots/steps/22-recipe-rules.png)

### 23. Click + Total / linear

Click + Total / linear. Set A_mL and B_mL coefficients to 1, aging_min to 0, relation = and the right-hand value to 1.

![Step 23: actual English SynthBO interface](screenshots/steps/23-total-volume-rule.png)

### 24. Click + Ratio

Click + Ratio. Choose the numerator and denominator, then set minimum and maximum permitted ratios.

![Step 24: actual English SynthBO interface](screenshots/steps/24-ratio-rule.png)

### 25. Use Import allowed candidates for a table containing variable columns only

Use Import allowed candidates for a table containing variable columns only. Its headers must match the variable names.

![Step 25: actual English SynthBO interface](screenshots/steps/25-import-candidates.png)

### 26. Review the candidate count and first 30 rows

Review the candidate count and first 30 rows. Click Apply (use BoTorch) after checking every rule.

![Step 26: actual English SynthBO interface](screenshots/steps/26-allowed-candidate-preview.png)

### 27. Generate a batch and inspect its conditions

Generate a batch and inspect its conditions. Bounds, steps, total, ratio and candidate-list rules are applied together.

![Step 27: actual English SynthBO interface](screenshots/steps/27-feasible-recipe-batch.png)

### 28. Analyze the remaining feasible recipes

Analyze the remaining feasible recipes. The horizontal axis is candidate ID; read volumes and aging times from the prediction table.

![Step 28: actual English SynthBO interface](screenshots/steps/28-recipe-predictions.png)

## Pareto objectives and trade-offs

### 29. Open the Pareto project

Open the Pareto project. Confirm the Pareto task and each objective direction: yield up, cost down.

![Step 29: actual English SynthBO interface](screenshots/steps/29-pareto-objective-settings.png)

### 30. Analyze the 6 starting results

Analyze the 6 starting results. The example has 22 unmeasured candidates and separate predictions for each objective.

![Step 30: actual English SynthBO interface](screenshots/steps/30-pareto-prediction-table.png)

### 31. Choose Pareto optimization → 2D Pareto and different X/Y objectives

Choose Pareto optimization → 2D Pareto and different X/Y objectives. Green points are measured non-dominated alternatives.

![Step 31: actual English SynthBO interface](screenshots/steps/31-pareto-trade-offs.png)

### 32. Choose Hypervolume history

Choose Hypervolume history. Compare history using one reference point; keep it fixed when comparing separate rounds.

![Step 32: actual English SynthBO interface](screenshots/steps/32-hypervolume-history.png)

### 33. Open the three-objective variant, analyze, then select 3D Pareto and three different axes.

Open the three-objective variant, analyze, then select 3D Pareto and three different axes.

![Step 33: actual English SynthBO interface](screenshots/steps/33-three-dimensional-pareto.png)

## Classification active learning

### 34. Open the morphology project

Open the morphology project. Confirm Classification active learning and Aggregated / Spheres / Rods labels.

![Step 34: actual English SynthBO interface](screenshots/steps/34-classification-label-settings.png)

### 35. Analyze and open Classification → Candidate class probabilities

Analyze and open Classification → Candidate class probabilities. Each bar describes a model probability distribution, not a measured image.

![Step 35: actual English SynthBO interface](screenshots/steps/35-class-probabilities.png)

### 36. Choose Classification uncertainty

Choose Classification uncertainty. Higher entropy means the classifier is less certain about a candidate's class.

![Step 36: actual English SynthBO interface](screenshots/steps/36-classification-entropy.png)

### 37. Choose Measured class counts

Choose Measured class counts. These counts include completed labeled records only, including replicates.

![Step 37: actual English SynthBO interface](screenshots/steps/37-measured-class-counts.png)

### 38. Choose Confusion matrix

Choose Confusion matrix. Rows are held-out measured labels and columns are predictions; this synthetic example scores 3/6.

![Step 38: actual English SynthBO interface](screenshots/steps/38-held-out-confusion-matrix.png)

### 39. Open binary-project.chembo.json to use Success / Failure with the outcome target column.

Open binary-project.chembo.json to use Success / Failure with the outcome target column.

![Step 39: actual English SynthBO interface](screenshots/steps/39-success-failure-labels.png)

### 40. Analyze the binary project to inspect two-label probabilities

Analyze the binary project to inspect two-label probabilities. Import its binary result table, not the morphology table.

![Step 40: actual English SynthBO interface](screenshots/steps/40-binary-class-probabilities.png)

### 41. With no measured classes, suggestions are an initial design

With no measured classes, suggestions are an initial design. The app explicitly shows that trained probabilities are unavailable.

![Step 41: actual English SynthBO interface](screenshots/steps/41-initial-design-without-probabilities.png)

## Read every numerical chart

### 42. Choose Predictions → Predictions & intervals

Choose Predictions → Predictions & intervals. Dots are model means, shaded bands are model intervals, and stars mark this batch when available.

![Step 42: actual English SynthBO interface](screenshots/steps/42-prediction-intervals.png)

### 43. Choose Mean & uncertainty to compare predicted means with model standard deviations.

Choose Mean & uncertainty to compare predicted means with model standard deviations.

![Step 43: actual English SynthBO interface](screenshots/steps/43-mean-and-uncertainty.png)

### 44. Choose Acquisition ranking

Choose Acquisition ranking. Scores are comparable within this analysis; batch selection can change after each pending point.

![Step 44: actual English SynthBO interface](screenshots/steps/44-acquisition-ranking.png)

### 45. Choose Model validation → Predicted vs measured

Choose Model validation → Predicted vs measured. Read RMSE, MAE and R² from the same held-out validation.

![Step 45: actual English SynthBO interface](screenshots/steps/45-predicted-versus-measured.png)

### 46. Choose Validation residuals

Choose Validation residuals. Values above zero are overpredictions; values below zero are underpredictions.

![Step 46: actual English SynthBO interface](screenshots/steps/46-validation-residuals.png)

### 47. Choose Data distribution → Measured distribution, then select a variable or objective.

Choose Data distribution → Measured distribution, then select a variable or objective.

![Step 47: actual English SynthBO interface](screenshots/steps/47-measured-data-distribution.png)

### 48. Choose Measurement history for a numeric objective

Choose Measurement history for a numeric objective. The line tracks the best completed value; record order is not elapsed time.

![Step 48: actual English SynthBO interface](screenshots/steps/48-best-measured-history.png)

### 49. Click a prediction point to display its exact variable conditions below the plot

Click a prediction point to display its exact variable conditions below the plot. Use the toolbar to pan, zoom and reset.

![Step 49: actual English SynthBO interface](screenshots/steps/49-inspect-a-candidate.png)

## Save and export

### 50. Select the required chart, then Export chart

Select the required chart, then Export chart. Choose PNG, PDF or SVG; explanatory model text is included.

![Step 50: actual English SynthBO interface](screenshots/steps/50-export-chart-png-pdf-svg.png)

### 51. Use Export predictions CSV for all candidate conditions and model outputs

Use Export predictions CSV for all candidate conditions and model outputs. Do not import this as measured data.

![Step 51: actual English SynthBO interface](screenshots/steps/51-export-prediction-table.png)

### 52. Use File → Save project as to preserve another project copy without replacing the original.

Use File → Save project as to preserve another project copy without replacing the original.

![Step 52: actual English SynthBO interface](screenshots/steps/52-file-menu.png)

### 53. Use Completed experiments → Export results for measured rows

Use Completed experiments → Export results for measured rows. This differs from exporting pending or predicted rows.

![Step 53: actual English SynthBO interface](screenshots/steps/53-export-measured-results.png)

## Move and withdraw pending conditions

### 54. Select a pending row before moving or withdrawing it

Select a pending row before moving or withdrawing it. The example starts with 6 completed and 2 fixed pending conditions.

![Step 54: actual English SynthBO interface](screenshots/steps/54-select-pending-condition.png)

### 55. Click Move selected to results

Click Move selected to results. Fill the blank objective cells, then save; matching pending conditions reconcile after validation.

![Step 55: actual English SynthBO interface](screenshots/steps/55-move-condition-to-results.png)

### 56. Click Withdraw selected to remove an unneeded pending condition without treating it as a measured experiment.

Click Withdraw selected to remove an unneeded pending condition without treating it as a measured experiment.

![Step 56: actual English SynthBO interface](screenshots/steps/56-withdraw-pending-condition.png)

## Cancel, licenses and native engines

### 57. Open Run log while computing

Open Run log while computing. Cancel stops the worker; upstream diagnostic lines keep their original language.

![Step 57: actual English SynthBO interface](screenshots/steps/57-calculation-log-and-cancel.png)

### 58. After cancellation, the existing measured and pending records remain

After cancellation, the existing measured and pending records remain. Re-run when ready; cancelled partial results are not accepted.

![Step 58: actual English SynthBO interface](screenshots/steps/58-cancelled-records-preserved.png)

### 59. Open About / licenses for scientific authorship, licensing and citation instructions; Open bundled licenses opens the accompanying files.

Open About / licenses for scientific authorship, licensing and citation instructions; Open bundled licenses opens the accompanying files.

![Step 59: actual English SynthBO interface](screenshots/steps/59-about-and-scientific-licenses.png)

### 60. Open the Gryffin project to use its native recommendations

Open the Gryffin project to use its native recommendations. This variant removes steps and the finite candidate list.

![Step 60: actual English SynthBO interface](screenshots/steps/60-gryffin-native-engine.png)

### 61. Open the Atlas project for native Gaussian-process suggestions

Open the Atlas project for native Gaussian-process suggestions. Use the BoTorch project for the app's plotted diagnostics.

![Step 61: actual English SynthBO interface](screenshots/steps/61-atlas-native-engine.png)

### 62. For Gryffin with Chimera, order numeric objectives by priority and set their relative tolerances

For Gryffin with Chimera, order numeric objectives by priority and set their relative tolerances. This is different from Pareto optimization.

![Step 62: actual English SynthBO interface](screenshots/steps/62-gryffin-objective-priorities.png)

### 63. Examples opens four small built-in workflows

Examples opens four small built-in workflows. Use the file-based en exercises for the exact row-count checkpoints above.

![Step 63: actual English SynthBO interface](screenshots/steps/63-built-in-workflow-examples.png)

### 64. Use Guide to reopen the tutorial in the current interface language

Use Guide to reopen the tutorial in the current interface language. Your language preference is remembered without changing experiment data.

![Step 64: actual English SynthBO interface](screenshots/steps/64-english-interface.png)

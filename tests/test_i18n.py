"""Language switching must change presentation without changing experiments."""
import ast
import copy
import csv
import os
from pathlib import Path

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
import typing_extensions
import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QDialogButtonBox

from chembo import i18n
from chembo.app import Window
from chembo.examples import workflow_example
from chembo.recipe_dialog import RecipeDialog
from test_analysis_view import synthetic_optimization, synthetic_classification


@pytest.fixture
def window(monkeypatch):
    app = QApplication.instance() or QApplication([])
    preferences = {}

    class Settings:
        def __init__(self, *args):
            pass

        def value(self, key, default=None):
            return preferences.get(key, default)

        def setValue(self, key, value):
            preferences[key] = value

    monkeypatch.setattr(i18n, 'QSettings', Settings)
    i18n.set_language('zh-CN', persist=False)
    result = Window()
    result._test_preferences = preferences
    yield result
    result.process = None
    result.dirty = False
    result.close()
    result.deleteLater()
    app.processEvents()
    i18n.set_language('zh-CN', persist=False)


@pytest.mark.parametrize('mode', ['optimization', 'recipe', 'pareto', 'classification'])
def test_button_roundtrip_preserves_every_workflow(window, mode):
    window.set_project(workflow_example(mode))
    before = window.collect()
    for destination in ('en', 'zh-CN'):
        window.language_button.click()
        assert i18n.language() == destination
        assert window.collect() == before
        assert not window.dirty
        assert window.engine.currentData() == before['engine']
    assert window.language_button.text() == 'English'
    assert window._test_preferences['interface/language'] == 'zh-CN'


def test_switch_preserves_unsaved_incomplete_input_and_pending(window):
    project = workflow_example('recipe')
    project['pending'] = [{'A': .2, 'B': .8}]
    window.set_project(project)
    window.params.item(0, 2).setText('')
    window.name.setText('未保存 / precious data')
    window.notes.setPlainText('打开 最大化 成功: user notes')
    state = copy.deepcopy(window.project)
    window.language_button.click()
    assert window.dirty and window.params.item(0, 2).text() == ''
    assert window.name.text() == '未保存 / precious data'
    assert window.notes.toPlainText() == '打开 最大化 成功: user notes'
    assert window.project == state
    assert window.pending.rowCount() == 1
    assert window.status.text().startswith('4 completed')


def test_english_controls_keep_stable_identifiers(window):
    window.language_button.click()
    window.engine.setCurrentIndex(0)
    window.task.setCurrentIndex(2)
    assert window.engine.currentData() == 'bo-mcp'
    assert window.engine.currentText() == i18n.EN['BoTorch · 优化与分类']
    assert window.task.currentData() == ('classification', 'hierarchical')
    assert window.params.cellWidget(0, 1).currentData() == 'continuous'
    assert window.objectives.cellWidget(0, 1).currentData() == 'max'
    window.task.setCurrentIndex(0)
    window.add_parameter()
    assert window.params.cellWidget(window.params.rowCount()-1, 1).currentText() == 'Continuous'
    window.add_objective()
    assert window.objectives.cellWidget(window.objectives.rowCount()-1, 1).currentText() == 'Maximize'


def test_language_preference_is_restored_when_app_starts(window, monkeypatch):
    window._test_preferences['interface/language'] = 'en'
    monkeypatch.setattr(i18n, '_initialized', False)
    i18n.initialize()
    second = Window()
    assert i18n.language() == 'en'
    assert second.language_button.text() == '中文'
    assert second.generate.text().startswith('Suggest')
    assert second.collect()['engine'] == 'bo-mcp'
    second.dirty = False
    second.close()
    second.deleteLater()


def test_words_that_match_ui_text_are_preserved_as_user_data(window):
    project = workflow_example('classification')
    old = project['parameters'][0]['name']
    project['parameters'][0]['name'] = '打开'
    for row in project['observations']:
        row['打开'] = row.pop(old)
    project['name'], project['notes'] = '保存', '最大化'
    window.set_project(project)
    before = window.collect()
    window.language_button.click()
    assert window.collect() == before
    assert window.observed.horizontalHeaderItem(0).text() == '打开'
    assert window.analysis_view.variable.itemText(0) == '打开'
    assert window.labels.text() == '成功 | 失败'
    assert window.notes.toPlainText() == '最大化'


def test_language_switch_preserves_running_process_and_button_states(window):
    sentinel = object()
    window.process = sentinel
    window.busy(True)
    window.language_button.click()
    assert window.process is sentinel
    assert not window.generate.isEnabled() and not window.analyze.isEnabled()
    assert all(not button.isEnabled() for button in window.action_buttons)
    assert 'Calculating' in window.message.text()
    assert window.cancel.text() == 'Cancel'
    window.process = None
    window.busy(False)


def test_recipe_dialog_translates_without_changing_rules(window):
    project = workflow_example('recipe')
    project['candidates'] = [{'A': .2, 'B': .8}, {'A': .8, 'B': .2}]
    dialog = RecipeDialog(project, window)
    before = copy.deepcopy(dialog.project)
    i18n.set_language('en', persist=False)
    assert dialog.windowTitle() == 'Executable recipe space'
    assert dialog.project == before
    assert dialog.table.horizontalHeaderItem(0).text() == 'Enabled joint constraints'
    assert dialog.candidate_label.text().startswith('Allowed candidates:')
    assert dialog.preview.horizontalHeaderItem(0).text() == before['parameters'][0]['name']
    buttons = dialog.findChild(QDialogButtonBox)
    assert buttons.button(QDialogButtonBox.Cancel).text().replace('&', '') == 'Cancel'
    i18n.set_language('zh-CN', persist=False)
    assert dialog.windowTitle() == '可执行配方空间'
    assert dialog.project == before
    dialog.close()
    dialog.deleteLater()


@pytest.mark.parametrize('fixture', [synthetic_optimization, synthetic_classification])
def test_all_chart_modes_retranslate_and_preserve_scientific_values(window, fixture):
    project, analysis = fixture()
    view = window.analysis_view
    view.set_analysis(analysis, project)
    before = copy.deepcopy((view.project, view.analysis))
    view.objective.setCurrentIndex(view.objective.count()-1)
    view.variable.setCurrentIndex(view.variable.count()-1)
    for page in (view.prediction, view.validation, view.distribution, view.multi, view.classification):
        for mode in range(page.kind.count()):
            page.kind.setCurrentIndex(mode)
            selection = (view.objective.currentIndex(), view.variable.currentIndex(), [b.currentIndex() for b in view.axes])
            for destination in ('en', 'zh-CN'):
                i18n.set_language(destination, persist=False)
                assert page.kind.currentIndex() == mode
                assert selection == (view.objective.currentIndex(), view.variable.currentIndex(), [b.currentIndex() for b in view.axes])
                assert (view.project, view.analysis) == before
                title = page.figure.axes[0].get_title()
                assert not any('\u4e00' <= c <= '\u9fff' for c in title) if destination == 'en' else title


def test_english_export_preserves_predictions_and_uses_english_captions(window, tmp_path):
    project, analysis = synthetic_optimization()
    view = window.analysis_view
    view.set_analysis(analysis, project)
    i18n.set_language('en', persist=False)
    table = tmp_path / 'predictions.csv'
    view.export_predictions(table)
    with table.open(encoding='utf-8-sig') as stream:
        rows = list(csv.DictReader(stream))
    assert rows[0]['yield · prediction'] == '10'
    assert rows[1]['Selected for batch'] == 'Yes'
    assert rows[0]['yield · standard deviation'] == '1'
    chart = tmp_path / 'prediction.svg'
    view.export_figure(chart)
    contents = chart.read_text()
    assert 'candidate model predictions' in contents and 'model predictions' in contents
    assert '候选模型预测' not in contents


def test_engine_error_and_warning_messages_are_localized(window, monkeypatch):
    captured = []
    monkeypatch.setattr(QMessageBox, 'warning', lambda *args: captured.append(args[1:]))
    window.language_button.click()
    window.error(ValueError('结果表列名必须恰好是：dose, yield。'))
    assert captured == [('Check the input', 'Result column names must be exactly: dose, yield.')]
    assert i18n.message('合法且未做的候选只剩 1 个，少于请求的 3 个。') == 'Only 1 feasible unmeasured candidates remain, fewer than the requested 3.'
    assert 'two classes' in i18n.message('尚未观察到两个类别，当前执行合法候选域中的分散初始设计，不提供分类概率。')
    assert i18n.message('temperature / dose 超出范围 [0, 1]。') == 'temperature / dose is outside [0, 1].'


def test_every_literal_ui_template_has_an_english_translation():
    root = Path(__file__).resolve().parents[1] / 'src/chembo'
    for filename in ('app.py', 'analysis_view.py', 'recipe_dialog.py'):
        tree = ast.parse((root / filename).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'tr' and node.args and isinstance(node.args[0], ast.Constant):
                source = node.args[0].value
                assert source in i18n.EN, (filename, node.lineno, source)

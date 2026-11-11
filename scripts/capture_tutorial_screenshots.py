"""Capture the actual English Qt interface using explicitly synthetic exercises.

Developer command: PYTHONPATH=src .venv/bin/python scripts/capture_tutorial_screenshots.py
Requires the existing scientific workers. No predictions are fabricated: model
screenshots are captured after the normal application's real worker completes.
Native OS file-picker appearance varies; portable Qt pickers show the same fields.
"""
import copy
import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys
import traceback
from unittest.mock import patch

import typing_extensions
from PySide6.QtCore import QEventLoop, QPoint, QTimer
from PySide6.QtWidgets import (
    QApplication, QComboBox, QDialog, QDoubleSpinBox, QFileDialog, QFormLayout,
    QInputDialog, QMenu, QMessageBox, QScrollArea, QSplitter,
)

from chembo import app as desktop
from chembo import __version__
from chembo.engine import read_observations
from chembo.i18n import set_language
from chembo.recipe_dialog import RecipeDialog
from chembo.storage import write_csv

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs/screenshots/steps'
WORK = Path('/private/tmp/SynthBO-Practice')
RESULTS = ROOT / 'validation' / ('tutorial-' + __version__)


class Capture:
    def __init__(self, window):
        self.window = window
        self.records, self.errors, self.model_checks = [], [], []
        window.error = lambda error: self.errors.append(str(error))
        window.resize(1680, 1060)
        window.findChild(QSplitter).setSizes([670, 960])
        for index, width in enumerate((138, 104, 70, 70, 105, 60, 60)):
            window.params.setColumnWidth(index, width)

    def shot(self, name, widget=None):
        widget = widget or self.window
        widget.update()
        QApplication.processEvents()
        if hasattr(widget, 'analysis_view'):
            for page in ('prediction', 'validation', 'distribution', 'multi', 'classification'):
                getattr(widget.analysis_view, page).canvas.draw()
        path = OUTPUT / (name + '.png')
        if not widget.grab().save(str(path)):
            raise RuntimeError('Screenshot failed: ' + name)
        self.records = [record for record in self.records if record['file'] != path.relative_to(ROOT).as_posix()]
        self.records.append({'file': path.relative_to(ROOT).as_posix(), 'language': 'zh-CN' if name == '65-chinese-interface' else 'en',
                             'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                             'width': widget.width(), 'height': widget.height()})
        print('Captured:', name, flush=True)

    def load(self, folder, filename='project.chembo.json'):
        self.window.dirty = False
        project = json.loads((WORK / folder / filename).read_text())
        self.window.set_project(project)
        # Labels are data; this supplies English defaults only for these examples.
        if project.get('task') != 'classification':
            self.window.loading = True
            self.window.labels.setText('Success | Failure')
            self.window.loading = False
        self.window.tabs.setCurrentIndex(0)
        scroll = self.window.findChild(QScrollArea)
        scroll.verticalScrollBar().setValue(0)
        return project

    def run(self, name, operation='analyze', starting_shot=None):
        self.errors.clear()
        self.window.run(operation=operation)
        if starting_shot:
            self.shot(starting_shot)
        self.wait()
        if self.errors:
            raise RuntimeError('; '.join(self.errors))
        project = self.window.project
        record = {'case': name, 'operation': operation, 'engine': project['engine'],
                  'completed': len(project['observations']), 'pending': len(project['pending']),
                  'predictions': len(project.get('analysis', {}).get('predictions', [])),
                  'validation_rows': len(project.get('analysis', {}).get('diagnostics', {}).get('rows', []))}
        self.model_checks.append(record)
        (RESULTS / (name + '.json')).write_text(json.dumps(project, ensure_ascii=False, indent=2))
        print('Real worker completed:', name, flush=True)

    def wait(self):
        loop = QEventLoop()
        poll, timeout = QTimer(), QTimer()
        poll.setInterval(30)
        poll.timeout.connect(lambda: loop.quit() if self.window.process is None else None)
        timeout.setSingleShot(True)
        timeout.timeout.connect(loop.quit)
        poll.start(); timeout.start(180000)
        loop.exec()
        poll.stop(); timeout.stop()
        if self.window.process is not None:
            self.window.cancel_run()
            raise RuntimeError('Screenshot workflow timed out')

    def plot(self, name, page, index=0):
        view = self.window.analysis_view
        self.window.tabs.setCurrentIndex(self.window.analysis_tab)
        target = getattr(view, page)
        if hasattr(target, 'kind'):
            target.kind.setCurrentIndex(index)
        view.tabs.setCurrentWidget(target)
        self.shot(name)

    def picker(self, name, path, save=False, directory=False):
        """Show a real Qt file picker, then return its actual selected path."""
        def choose(parent, caption, initial='', filters='', *args, **kwargs):
            dialog = QFileDialog(parent, caption, str(path.parent), filters)
            dialog.setOption(QFileDialog.DontUseNativeDialog)
            dialog.setOption(QFileDialog.DontConfirmOverwrite)
            dialog.setAcceptMode(QFileDialog.AcceptSave if save else QFileDialog.AcceptOpen)
            dialog.setFileMode(QFileDialog.Directory if directory else QFileDialog.AnyFile if save else QFileDialog.ExistingFile)
            dialog.selectFile(str(path))
            dialog.resize(900, 560)
            def inspect():
                self.shot(name, dialog)
                dialog.accept()
            QTimer.singleShot(80, inspect)
            if dialog.exec() != QDialog.Accepted:
                raise RuntimeError('The documentation file picker was cancelled')
            selected = dialog.selectedFiles()[0]
            return selected if directory else (selected, dialog.selectedNameFilter())
        return patch.object(QFileDialog, 'getExistingDirectory' if directory else 'getSaveFileName' if save else 'getOpenFileName', choose)

    def modal(self, name, callback, setup=None):
        def inspect():
            dialog = QApplication.activeModalWidget()
            if setup:
                setup(dialog)
            self.shot(name, dialog)
            dialog.accept()
        QTimer.singleShot(80, inspect)
        return callback()

    def menu(self, name, index):
        menu = self.window.menuBar().actions()[index].menu()
        menu.popup(self.window.mapToGlobal(QPoint(10 + index * 50, 30)))
        self.shot(name, menu)
        menu.hide()

    def recipe(self):
        def edit():
            dialog = QApplication.activeModalWidget()
            assert isinstance(dialog, RecipeDialog)
            self.shot('22-recipe-rules', dialog)
            dialog.project['constraints'] = []
            dialog.refresh()
            def linear(child):
                for box, value in zip(child.findChildren(QDoubleSpinBox), (1, 1, 0, 1)):
                    box.setValue(value)
            self.modal('23-total-volume-rule', dialog.add_linear, linear)
            def ratio(child):
                for box, value in zip(child.findChildren(QDoubleSpinBox), (.25, 4)):
                    box.setValue(value)
            self.modal('24-ratio-rule', dialog.add_ratio, ratio)
            with self.picker('25-import-candidates', WORK / '02_recipe/candidates.csv'):
                dialog.import_candidates()
            self.shot('26-allowed-candidate-preview', dialog)
            dialog.accept_checked()
        QTimer.singleShot(80, edit)
        self.window.edit_recipe()

    def execute(self):
        w = self.window
        self.load('01_quickstart')
        self.shot('01-main-window')
        self.shot('02-language-button', w.language_button)
        self.menu('03-help-menu', 1)
        exported = WORK / 'Exported-practice'
        exported.mkdir(exist_ok=True)
        with self.picker('04-export-practice-data', exported, directory=True), patch.object(desktop.QDesktopServices, 'openUrl', lambda *args: True):
            w.export_tutorial_data()
        with self.picker('05-open-project', WORK / '01_quickstart/project.chembo.json'):
            w.open_project()
        self.shot('06-six-measured-results')
        self.shot('07-task-engine-batch-seed')
        self.run('quickstart-initial-analysis', starting_shot='08-calculating')
        self.plot('09-fourteen-candidate-predictions', 'table')
        self.plot('10-six-row-cross-validation', 'validation')
        self.run('quickstart-first-batch', 'recommend')
        assert len(w.project['pending']) == 2
        self.shot('11-two-pending-experiments')
        pending = WORK / 'round-1-pending.csv'
        with self.picker('12-export-pending-csv', pending, save=True):
            w.export_pending()
        p = copy.deepcopy(w.project)
        names = [item['name'] for item in p['parameters']]
        oracle = read_observations(p, WORK / '01_quickstart/all-simulated-results.csv')
        measured = [next(row for row in oracle if all(row[key] == condition[key] for key in names)) for condition in p['pending']]
        completed = WORK / 'round-1-measured.csv'
        write_csv(completed, names + ['yield_pct'], measured)
        with self.picker('13-import-measured-csv', completed):
            w.import_csv()
        assert len(w.project['observations']) == 8 and not w.project['pending']
        self.shot('14-eight-completed-zero-pending')
        with self.picker('15-save-project', WORK / 'quickstart-round-1.chembo.json', save=True):
            assert w.save(as_new=True)
        self.run('quickstart-after-refill')
        quickstart = copy.deepcopy(w.project)

        w.dirty = False
        w.new_project()
        w.name.setText('My synthesis study (SYNTHETIC example)')
        self.shot('16-new-project')
        self.load('01_quickstart')
        self.shot('17-variable-types-and-steps')
        self.load('03_pareto')
        w.findChild(QScrollArea).verticalScrollBar().setValue(10000)
        self.shot('18-objective-goal-and-notes')
        self.load('01_quickstart', 'empty-project.chembo.json')
        original_get_item = QInputDialog.getItem
        def choose_sheet(*args, **kwargs):
            return self.modal('20-select-results-worksheet', lambda: original_get_item(*args, **kwargs))
        with self.picker('19-import-excel', WORK / '01_quickstart/seed-observations.xlsx'):
            with patch.object(QInputDialog, 'getItem', choose_sheet):
                w.import_csv()
        assert len(w.project['observations']) == 6
        w.add_observation()
        self.shot('21-manual-experiment-row')

        self.load('02_recipe')
        self.recipe()
        self.run('recipe-batch', 'recommend')
        self.shot('27-feasible-recipe-batch')
        self.run('recipe-analysis')
        self.plot('28-recipe-predictions', 'prediction')
        w.analysis_view.export_figure(ROOT / 'docs/screenshots/tutorial-recipe.png')

        self.load('03_pareto')
        self.shot('29-pareto-objective-settings')
        self.run('pareto-analysis')
        self.plot('30-pareto-prediction-table', 'table')
        self.plot('31-pareto-trade-offs', 'multi')
        w.analysis_view.export_figure(ROOT / 'docs/screenshots/tutorial-pareto.png')
        self.plot('32-hypervolume-history', 'multi', 2)
        self.load('03_pareto', 'three-objective-project.chembo.json')
        self.run('three-objective-analysis')
        self.plot('33-three-dimensional-pareto', 'multi', 1)

        self.load('04_classification')
        self.shot('34-classification-label-settings')
        self.run('classification-analysis')
        self.plot('35-class-probabilities', 'classification')
        w.analysis_view.export_figure(ROOT / 'docs/screenshots/tutorial-classification.png')
        self.plot('36-classification-entropy', 'classification', 1)
        self.plot('37-measured-class-counts', 'classification', 2)
        self.plot('38-held-out-confusion-matrix', 'classification', 3)
        w.analysis_view.export_figure(ROOT / 'docs/screenshots/tutorial-confusion.png')
        self.load('04_classification', 'binary-project.chembo.json')
        self.shot('39-success-failure-labels')
        self.run('binary-analysis')
        self.plot('40-binary-class-probabilities', 'classification')
        self.load('04_classification', 'empty-project.chembo.json')
        self.run('initial-classification-design', 'recommend')
        self.plot('41-initial-design-without-probabilities', 'classification')

        w.set_project(quickstart)
        self.plot('42-prediction-intervals', 'prediction')
        w.analysis_view.export_figure(ROOT / 'docs/screenshots/tutorial-quickstart.png')
        self.plot('43-mean-and-uncertainty', 'prediction', 1)
        self.plot('44-acquisition-ranking', 'prediction', 2)
        self.plot('45-predicted-versus-measured', 'validation')
        w.analysis_view.export_figure(ROOT / 'docs/screenshots/tutorial-validation.png')
        self.plot('46-validation-residuals', 'validation', 1)
        self.plot('47-measured-data-distribution', 'distribution')
        w.analysis_view.variable.setCurrentText('yield_pct')
        self.plot('48-best-measured-history', 'distribution', 1)
        self.plot('49-inspect-a-candidate', 'prediction')
        artist = next(c for c in w.analysis_view.prediction.figure.axes[0].collections if hasattr(c, '_nanobo_labels'))
        event = type('Pick', (), {'artist': artist, 'ind': [0]})()
        w.analysis_view._picked(event)
        self.shot('49-inspect-a-candidate')
        with self.picker('50-export-chart-png-pdf-svg', WORK / 'prediction.svg', save=True):
            w.analysis_view._choose_figure()
        with self.picker('51-export-prediction-table', WORK / 'model-predictions.csv', save=True):
            w.analysis_view._choose_predictions()
        self.menu('52-file-menu', 0)
        with self.picker('53-export-measured-results', WORK / 'measured-results.csv', save=True):
            w.export_observed()
        self.load('01_quickstart', 'pending-practice.chembo.json')
        w.tabs.setCurrentIndex(1)
        w.pending.selectRow(0)
        self.shot('54-select-pending-condition')
        w.pending_to_observed()
        self.shot('55-move-condition-to-results')
        self.load('01_quickstart', 'pending-practice.chembo.json')
        w.pending.selectRow(0)
        w.withdraw_pending()
        w.tabs.setCurrentIndex(1)
        self.shot('56-withdraw-pending-condition')
        self.load('01_quickstart')
        w.run(operation='analyze')
        w.tabs.setCurrentIndex(w.log_tab)
        self.shot('57-calculation-log-and-cancel')
        w.cancel_run()
        self.wait()
        self.shot('58-cancelled-records-preserved')
        self.modal('59-about-and-scientific-licenses', w.about)

        self.load('01_quickstart', 'gryffin-project.chembo.json')
        self.shot('60-gryffin-native-engine')
        self.load('01_quickstart', 'atlas-project.chembo.json')
        self.shot('61-atlas-native-engine')
        p = self.load('01_quickstart', 'gryffin-project.chembo.json')
        p['objectives'].append({'name': 'synthetic_cost', 'goal': 'min', 'tolerance': .2})
        for index, row in enumerate(p['observations'], 1):
            row['synthetic_cost'] = index
        w.set_project(p)
        w.findChild(QScrollArea).verticalScrollBar().setValue(10000)
        self.shot('62-gryffin-objective-priorities')
        self.load('01_quickstart')
        self.modal('63-built-in-workflow-examples', w.load_example)

        self.load('01_quickstart')
        self.shot('64-english-interface')
        shutil.copyfile(OUTPUT / '64-english-interface.png', ROOT / 'docs/screenshots/SynthBO-preview-en.png')
        shutil.copyfile(OUTPUT / '64-english-interface.png', ROOT / 'docs/screenshots/SynthBO-preview.png')
        set_language('zh-CN', persist=False)
        QApplication.processEvents()
        w.grab().save(str(RESULTS / 'chinese-interface.png'))
        set_language('en', persist=False)
        manifest = {'product': 'SynthBO', 'version': __version__, 'data_status': 'SYNTHETIC',
                    'capture': 'Actual Qt widgets, actual worker output, English practice data',
                    'platform': 'macOS; shared app controls also apply to Windows; native file pickers differ',
                    'screenshots': self.records, 'real_worker_checks': self.model_checks}
        (ROOT / 'docs/screenshots/SCREENSHOTS.json').write_text(json.dumps(manifest, indent=2))
        print('Screenshot capture complete:', len(self.records), flush=True)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(exist_ok=True)
    shutil.copytree(ROOT / 'examples/tutorial/en', WORK, dirs_exist_ok=True)
    set_language('en', persist=False)
    original_exec = QApplication.exec
    status = [1]

    def start():
        window = next(w for w in QApplication.topLevelWidgets() if isinstance(w, desktop.Window))
        try:
            Capture(window).execute()
            status[0] = 0
        except Exception:
            traceback.print_exc()
        finally:
            if window.process:
                window.cancel_run()
            window.dirty = False
            QApplication.quit()

    def run_app(self):
        QTimer.singleShot(150, start)
        return original_exec()

    QApplication.exec = run_app
    desktop.main()
    return status[0]


if __name__ == '__main__':
    raise SystemExit(main())

import statistics

from textual.app import App, ComposeResult
from textual.widgets import ListItem, ListView, Label  # , Input, Button, ProgressBar, Static
from textual.screen import Screen
from textual.containers import Vertical, Container

import variables as common


class CPUResults(Screen):
    def __init__(self):
        super().__init__()
        self.cpu_label = Label()
        self.pcore_label = Label()

    def compose(self) -> ComposeResult:
        yield Vertical(
            self.cpu_label,
            self.pcore_label,
            id='dialog'
        )

    def on_screen_resume(self) -> None:
        try: pcore = round(statistics.mean(common.cpu_pcore), 1)
        except: pcore = 0
        self.cpu_label.update(F"CPU Single-Thread Score:   {common.cpu_score}")
        self.pcore_label.update(F"CPU Multiple-Thread Score: {pcore}")
        del pcore

    def on_key(self, event):
        if event.key == "q":
            self.app.switch_screen("results")


class RAMResults(Screen):
    def __init__(self):
        super().__init__()
        self.ram_label = Label()

    def compose(self) -> ComposeResult:
        yield Vertical(
            self.ram_label,
            id='dialog'
        )

    def on_screen_resume(self):
        self.ram_label.update(F"RAM Score: {common.ram_score}")

    def on_key(self, event):
        if event.key == "q":
            self.app.switch_screen("results")


class GPUResults(Screen):
    def __init__(self):
        super().__init__()
        self.gpu_label = Label()

    def compose(self) -> ComposeResult:
        yield Vertical(
            self.gpu_label,
            id="dialog"
        )

    def on_screen_resume(self) -> None:
        self.gpu_label.update(F"GPU Benchmark FPS: {common.gpu_score} FPS")

    def on_key(self, event):
        self.app.switch_screen("results")


class EthernetResults(Screen):
    def __init__(self):
        super().__init__()
        self.download_label = Label()
        self.upload_label = Label()
        self.ping_label = Label()

    def compose(self) -> ComposeResult:
        yield Vertical(
            self.download_label,
            self.upload_label,
            self.ping_label,
            id='dialog'
        )

    def on_screen_resume(self):
        self.download_label.update(F"Download Rate: {common.download} Mbps")
        self.upload_label.update(F"Upload Rate:.. {common.upload} Mbps")
        self.ping_label.update(F"Ping:......... {common.ping} ms")

    def on_key(self, event):
        if event.key == 'q':
            self.app.switch_screen('results')


class HDDResults(Screen):
    def __init__(self):
        super().__init__()
        self.read_label = Label()
        self.write_label = Label()

    def compose(self) -> ComposeResult:
        yield Vertical(
            self.read_label,
            self.write_label,
            id='dialog'
        )

    def on_screen_resume(self):
        self.read_label.update (F"Read Rate:   {common.hdd_read} MB/s")
        self.write_label.update(F"Write Rate:  {common.hdd_write} MB/s")

    def on_key(self, event):
        if event.key == 'q': self.app.switch_screen('results')


class SaveResults(Screen):
    def compose(self) -> ComposeResult: ...

    def on_key(self, event):
        if event.key == 'q':
            self.app.switch_screen('results')

class BenchmarkResults(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Label("Benchmark"),
            ListView(
                ListItem(Label("CPU Results"), id='cpu'),
                ListItem(Label("RAM Results"), id='ram'),
                ListItem(Label("GPU Results"), id='gpu'),
                ListItem(Label("HDD Results"), id='hdd'),
                ListItem(Label("Speed Test Results"), id='int'),
                ListItem(Label("Save to a file"), id='save'),
                ListItem(Label("Return"), id='exit'),
                id='menu-list'
            ),
            id='dialog'
        )

    def on_list_view_selected(self, event):
        choice = event.item.id
        if choice == 'cpu': self.app.switch_screen('cpu_results')
        elif choice == 'ram': self.app.switch_screen('ram_results')
        elif choice == 'gpu': self.app.switch_screen('gpu_results')
        elif choice == 'hdd': self.app.switch_screen('hdd_results')
        elif choice == 'int': self.app.switch_screen('int_results')
        elif choice == 'save': self.app.switch_screen('save_results')
        elif choice == 'exit': self.app.switch_screen('StartScreen')


    def on_key(self, event):
        if event.key == "q":
            self.app.switch_screen("StartScreen")

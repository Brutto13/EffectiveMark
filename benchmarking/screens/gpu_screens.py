from textual.app import ComposeResult
from textual.widgets import ListItem, ListView, Label
from textual.screen import Screen
from textual.containers import Container

from benchmarking.sources.gpu_benchmark import *
import variables as common


class GPUSelect(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Label("Run GPU Benchmark"),
            ListView(
                ListItem(Label("Yes"), id="Y"),
                ListItem(Label("No"), id="N"),
                id="menu-list"
            ),
            id="dialog"
        )

    def on_list_view_selected(self, event):
        if event.item.id == "Y": self.app.switch_screen("GPUArithmeticTest")
        elif event.item.id == "N": self.app.switch_screen("StartScreen")
        # elif event.item.id == "llm": self.app.switch_screen("LLMTest")


class GPUArithmeticTest(Screen):
    def __init__(self):
        super().__init__()
        self.timer = None

    def compose(self) -> ComposeResult:
        yield Container(
            Label("GPU Arithmetic Benchmark in progress, Please wait..."),
            id="dialog"
        )

    def on_show(self):
        # threading.Thread(target=start_gpu_benchmark, daemon=True).start()
        self.app.call_later(start_gpu_benchmark)
        self.timer = self.set_interval(0.5, self.chk_res)

    def chk_res(self):
        if common.gpu_score != common.init:
            self.timer.stop()
            self.app.switch_screen("results")

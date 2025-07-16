import psutil
import random
import multiprocessing as mp
from textual.app import Screen, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Label, ProgressBar, Button

from stability.sources.ram_testing import ram_worker


class RAMTest(Screen):
    def __init__(self):
        super().__init__()
        self.passes = mp.Value('i', 0)
        # self.progress_bar = ProgressBar(total=100)
        self.passes_label = Label()
        self.usage_bar = ProgressBar(total=100, show_eta=False)
        self.cpu_bar = ProgressBar(total=100, show_eta=False)
        self.terminate = mp.Event()
        self.timer = self.set_interval(0.5, self.update_ram_screen)

    def compose(self) -> ComposeResult:
        yield Container(
            Label("RAM Stability Test"),
            Horizontal(Label("Test Passes"), self.passes_label),
            Horizontal(Label("CPU Usage "), self.cpu_bar),
            Horizontal(Label("RAM Usage "), self.usage_bar),
            Button("Abort Test"),
            id='dialog'
        )

    def update_ram_screen(self):
        self.passes_label.update(" " + str(self.passes.value))
        self.usage_bar.update(progress=psutil.virtual_memory().percent)
        self.cpu_bar.update(progress=psutil.cpu_percent(.1))

    def run_test(self):
        self.proc = mp.Process(target=ram_worker, args=(self.passes, self.terminate), name='RAM Tester')
        self.proc.start()

    def on_button_pressed(self, event):
        self.proc.terminate()
        self.proc.join(1)
        self.app.switch_screen('StartScreen')

    def on_screen_resume(self):
        self.call_later(self.run_test)


class RAMError(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Label("RAM Read/Write Error Detected"),
            Button("Exit"),
            id='dialog'
        )

    def on_button_pressed(self):
        self.app.switch_screen("StartScreen")

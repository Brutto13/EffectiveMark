import psutil
import random
import multiprocessing as mp
from textual.app import Screen, ComposeResult
from textual.color import Gradient
from textual.containers import Container, Horizontal
from textual.widgets import Label, ProgressBar, Button

from stability.sources.ram_testing import ram_worker


class RAMTest(Screen):
    CSS = """
    /*Progress bar colors*/
    ProgressBar.cyan > .bar {
        background: cyan;
    }
    
    ProgressBar.green > .bar {
        background: green;
    }

    ProgressBar.yellow > .bar {
        background: yellow;
    }

    ProgressBar.orange > .bar {
        background: orange;
    }

    ProgressBar.red > .bar {
        background: red;
    }
    """

    def __init__(self):
        super().__init__()
        self.passes = mp.Value('i', 0)
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
        ram_usage = psutil.virtual_memory().percent
        self.passes_label.update(" " + str(self.passes.value))
        self.usage_bar.update(progress=ram_usage)
        self.cpu_bar.update(progress=psutil.cpu_percent(.1))

        # Remove all possible color classes first
        self.usage_bar.remove_class("cyan")
        self.usage_bar.remove_class("green")
        self.usage_bar.remove_class("yellow")
        self.usage_bar.remove_class("orange")
        self.usage_bar.remove_class("red")

        # Add class based on value
        if ram_usage >= 95:
            self.usage_bar.add_class("red")
        elif ram_usage >= 80:
            self.usage_bar.add_class("orange")
        elif ram_usage >= 50:
            self.usage_bar.add_class("yellow")
        elif ram_usage >= 30:
            self.usage_bar.add_class("green")
        elif ram_usage >= 10:
            self.usage_bar.add_class("cyan")

        self.usage_bar.refresh()

    def run_test(self):
        self.proc = mp.Process(target=ram_worker, args=(self.passes, self.terminate), name='RAM Tester')
        self.proc.start()

    def on_button_pressed(self, event):
        self.proc.terminate()
        self.proc.join(1)
        self.app.switch_screen('StabilityScreen')

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

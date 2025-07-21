import psutil

from statistics import mean, StatisticsError
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, ProgressBar, Button, Header
from textual.containers import Container, Horizontal

# Internal imports
from stability.sources.cpu_testing import *


class CPUTest(Screen):
    def __init__(self):
        super().__init__()
        # self.usage_bar = ProgressBar(total=100, show_eta=False)
        self.freq_bar = ProgressBar(total=5000, show_eta=False, show_percentage=False)
        self.temp_bar = ProgressBar(total=100, show_eta=False, show_percentage=False)
        self.processes = []
        self.terminate = []
        self.timer = self.app.set_timer(0.1, self.update_screen)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("CPU Stability Testing"),
            Horizontal(Label("CPU Avg Frequency [MHz]   "), self.freq_bar),
            # Horizontal(Label("CPU Frequency [Mhz]"), self.freq_bar),
            Horizontal(Label("CPU Avg Temperature [*C]  "), self.temp_bar),
            Button("Abort Test"),
            id='dialog'
        )

    def multi_cpu(self, cores: int = -1) -> None:
        # Check if custom number of processes is set (cores=...)
        # otherwise set count of processes equal to number of CPU cores
        if cores == -1: cores = os.cpu_count()

        for _ in range(cores):
            stop = mp.Event()
            self.terminate.append(stop)
            proc = mp.Process(target=worker, args=(stop,))
            proc.start()
            self.processes.append(proc)

    def update_screen(self):
        try:
            self.freq_bar.update(progress=mean(get_cpu_frequencies()))
            self.temp_bar.update(progress=mean(get_cpu_temperatures()))
        except: pass

    def on_screen_resume(self) -> None:
        self.app.call_later(self.multi_cpu)

    def on_button_pressed(self, event):
        for proc in self.processes:
            proc.terminate()
            proc.join(1)

        self.app.switch_screen("StabilityScreen")

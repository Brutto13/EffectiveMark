import asyncio
import os
import psutil
import multiprocessing as mp

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Label, ProgressBar, Button
from textual.containers import Container, Horizontal

# Internal imports
from stability.sources.cpu_testing import worker


class CPUTest(Screen):
    def __init__(self):
        super().__init__()
        self.usage_bar = ProgressBar(total=100, show_eta=False)
        self.temp_bar = ProgressBar(total=100, show_eta=False)
        self.processes = []
        self.terminate = []

    def compose(self) -> ComposeResult:
        yield Container(
            Label("CPU Stability Testing"),
            Horizontal(Label("CPU Usage [%]       "), self.usage_bar),
            Horizontal(Label("CPU Temperature [*C]"), self.temp_bar),
            Button("Abort Test"),
            id='dialog'
        )

    def multi_cpu(self, cores: int = -1) -> None:
        # Check if custom number of processes is set (cores=...)
        # otherwise set count of processes equal to number of CPU cores
        if cores == -1: cores = os.cpu_count()

        for _ in range(cores+1):
            stop = mp.Event()
            self.terminate.append(stop)
            proc = mp.Process(target=worker, daemon=True, args=(stop,))
            proc.start()
            self.processes.append(proc)

    def on_screen_resume(self) -> None:
        self.app.call_later(self.multi_cpu)

    def on_button_pressed(self, event):
        for proc in self.processes:
            proc.terminate()
            proc.join(1)

        self.app.switch_screen("StabilityScreen")




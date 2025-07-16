import asyncio
import time
import os
import psutil
import multiprocessing as mp

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Label, ProgressBar, Button
from textual.containers import Container, Horizontal

# Internal imports
from stability.sources.cpu_testing import worker, get_cpu_temperature_from_dll


class CPUTest(Screen):
    def __init__(self):
        super().__init__()
        self.usage_bar = ProgressBar(total=100, show_eta=False)
        # self.freq_bar = ProgressBar(total=5000, show_eta=False, show_percentage=False)
        self.temp_bar = ProgressBar(total=100, show_eta=False, show_percentage=False)
        self.processes = []
        self.terminate = []
        self.timer = self.app.set_timer(0.1, self.update_screen)

    def compose(self) -> ComposeResult:
        yield Container(
            Label("CPU Stability Testing"),
            Horizontal(Label("CPU Usage [%]       "), self.usage_bar),
            # Horizontal(Label("CPU Frequency [Mhz]"), self.freq_bar),
            Horizontal(Label("CPU Temperature [*C]"), self.temp_bar),
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
        self.usage_bar.update(progress=psutil.cpu_percent(0.1))
        # self.freq_bar.update(progress=psutil.cpu_freq().current)
        self.temp_bar.update(progress=get_cpu_temperature_from_dll())
        # psutil.cpu_percent()

    def on_screen_resume(self) -> None:
        self.app.call_later(self.multi_cpu)

    def on_button_pressed(self, event):
        for proc in self.processes:
            proc.terminate()
            proc.join(1)

        self.app.switch_screen("StabilityScreen")

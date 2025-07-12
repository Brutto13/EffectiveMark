import asyncio

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label, Switch, ProgressBar, Button
from textual.screen import Screen
from textual.containers import Horizontal, Container, Grid, Vertical

from sources.cpu_benchmark import *
from sources.ram_benchmark import *
from sources.gpu_benchmark import *
from sources.hdd_benchmark import *
from sources.eth_benchmark import *

import variables as common

cpu = ram = gpu = hdd = False
modes = []

class CombinedTest(Screen):
    def compose(self) -> ComposeResult:
        yield Grid(
            Horizontal(
                Container(Label("CPU Test"), Switch(id='cpu_switch'), id='checkbox1'),
                Container(Label("RAM Test"), Switch(id='ram_switch'), id='checkbox2')
            ),
            Horizontal(
                Container(Label("GPU Test"), Switch(id='gpu_switch'), id='checkbox1'),
                Container(Label("HDD Benchmark"), Switch(id='hdd_switch'), id='checkbox2')
            ),
            Button("Start Combined Benchmark"),
            id='dialog2'
        )

    def on_button_pressed(self):
        global cpu, ram, gpu, hdd, modes
        cpu = self.query_one('#cpu_switch', Switch).value
        ram = self.query_one('#ram_switch', Switch).value
        gpu = self.query_one('#gpu_switch', Switch).value
        hdd = self.query_one('#hdd_switch', Switch).value
        modes = [cpu, ram, gpu, hdd]
        self.app.push_screen(CombinedRunning())

    def on_key(self, event):
        if event.key == 'q': self.app.switch_screen("StartScreen")


class CombinedRunning(Screen):
    def __init__(self):
        super().__init__()
        self.total = modes.count(True)
        self.status = Label()
        self.progress = ProgressBar(total=self.total)

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Combined Benchmark Running"),
            self.status,
            id='dialog'
        )

    def update_progress(self):
        self.progress.advance(1)

    def on_screen_resume(self):
        self.call_later(self.launch_benchmarks)

    async def launch_benchmarks(self):
        await self.mount(self.progress)
        if cpu:
            self.status.update("Starting CPU Benchmark")
            common.cpu_score, _ = await asyncio.to_thread(raw_cpu_benchmark, 2e7)

        if ram:
            self.status.update("Starting CPU Benchmark")
            common.ram_score = await asyncio.to_thread(ram_benchmark)

        if gpu:
            self.status.update("Starting CPU Benchmark")
            await asyncio.to_thread(start_gpu_benchmark)

        if hdd:
            self.status.update("Starting CPU Benchmark")
            common.hdd_read, common.hdd_write = await asyncio.to_thread(hdd_benchmark)

        self.app.switch_screen("results")

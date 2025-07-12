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
        self.app.switch_screen('CombinedRunning')

    def on_key(self, event):
        if event.key == 'q': self.app.switch_screen("StartScreen")


class CombinedRunning(Screen):
    def __init__(self):
        super().__init__()
        self.total = modes.count(True)
        # self.status = Label()
        self.step = 0

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Combined Benchmark Running"),
            Label("This may take a while"),
            id='dialog'
        )

    def on_screen_resume(self):
        self.call_later(self.start_benchmark)

    def start_benchmark(self):
        if cpu: common.cpu_score, _ = raw_cpu_benchmark(2e7)
        if ram: common.ram_score = ram_benchmark()
        if gpu: start_gpu_benchmark()
        if hdd: common.hdd_read, common.hdd_write = hdd_benchmark()
        self.app.switch_screen('results')

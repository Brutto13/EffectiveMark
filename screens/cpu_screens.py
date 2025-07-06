import asyncio
from sources.cpu_benchmark import *

from textual.app import App, ComposeResult
from textual.widgets import ListItem, ListView, Label  # , Input, Button, ProgressBar, Static
from textual.screen import Screen
from textual.containers import Vertical, Container

# Globals
cpu_score: float | str = "N/A"

class CPU_SingleThread_Loading(Screen):
    async def ExecuteCPUBenchmark(self):
        global cpu_score
        score, _ = await asyncio.to_thread(raw_cpu_benchmark, iterations=int(2e7))
        cpu_score = score
        del _
        # cpu_score = await asyncio.to_thread(cpu_benchmark, cores=run_threads)
        await self.app.switch_screen("results")

    def on_screen_resume(self): asyncio.create_task(self.ExecuteCPUBenchmark())

    def compose(self) -> ComposeResult:
        yield Container(Label("CPU Benchmark in progress, Please wait..."), id="dialog")

class CPU_Select(Screen):
    def compose(self) -> ComposeResult:
        # items = [ListItem(Label(str(x+1)), id="a"+str(x+1)) for x in range(CPU_CORES-1, -1, -1)]
        # items.append(ListItem(Label("Cancel"), id="exit"))
        yield Container(
            Label("Select number of threads"),
            ListView(
                ListItem(Label("Single Thread Benchmark"), id='single'),
                # ListItem(Label("Full CPU benchmark"), id='full'),
                ListItem(Label("Cancel"), id="exit"),
                id="menu-list"),
            id="dialog",
        )

    def on_key(self, event):
        if event.key == "q":
            self.app.switch_screen("StartScreen")

    def on_list_view_selected(self, event):
        if event.item.id == "exit": self.app.switch_screen("StartScreen")
        elif event.item.id == "single": self.app.switch_screen("InProgress")
        elif event.item.id == "full": self.app.switch_screen("FullProgress")
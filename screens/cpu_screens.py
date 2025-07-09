import asyncio
import os
import threading

from sources.cpu_benchmark import *

from textual.app import ComposeResult
from textual.widgets import ListItem, ListView, Label
from textual.screen import Screen
from textual.containers import Container

import variables as common


class CPU_SingleThread_Loading(Screen):
    async def ExecuteCPUBenchmark(self):
        common.cpu_score, _ = await asyncio.to_thread(raw_cpu_benchmark, iterations=int(2e7))
        del _
        # cpu_score = await asyncio.to_thread(cpu_benchmark, cores=run_threads)
        await self.app.switch_screen("cpu_results")

    def on_screen_resume(self): asyncio.create_task(self.ExecuteCPUBenchmark())

    def compose(self) -> ComposeResult:
        yield Container(Label("CPU Benchmark in progress, Please wait..."), id="dialog")


class CPU_MultiThread_Loading(Screen):
    def __init__(self):
        super().__init__()
        self.num_proc = os.cpu_count()
        self.threads_done = 0
        self.done_event = threading.Event()
        self.lock = threading.Lock()

    def compose(self) -> ComposeResult:
        yield Container(
            Label("CPU Multi-Threading Benchmark in progress, please wait..."),
            id="dialog"
        )

    def on_screen_resume(self):
        self.threads_done = 0
        self.done_event.clear()

        for _ in range(self.num_proc):
            threading.Thread(target=self.worker, daemon=True).start()

        # Monitor completion
        threading.Thread(target=self.watchdog, daemon=True).start()

    def worker(self):
        score, _ = raw_cpu_benchmark(2e7)
        common.cpu_pcore.append(score)
        del _
        with self.lock:
            self.threads_done += 1
            if self.threads_done == self.num_proc:
                self.done_event.set()

    def watchdog(self):
        self.done_event.wait()
        self.app.switch_screen("cpu_results")




class CPU_Select(Screen):
    def compose(self) -> ComposeResult:
        # items = [ListItem(Label(str(x+1)), id="a"+str(x+1)) for x in range(CPU_CORES-1, -1, -1)]
        # items.append(ListItem(Label("Cancel"), id="exit"))
        yield Container(
            Label("Select number of threads"),
            ListView(
                ListItem(Label("Single Thread Benchmark"), id='single'),
                ListItem(Label("Multi Threads Benchmark"), id='full'),
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

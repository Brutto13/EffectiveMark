import asyncio
import os

from multiprocessing import Process, Manager
from benchmarking.sources.cpu_benchmark import *

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
        await self.app.switch_screen("results")

    def on_screen_resume(self): asyncio.create_task(self.ExecuteCPUBenchmark())

    def compose(self) -> ComposeResult:
        yield Container(Label("CPU Benchmark in progress, Please wait..."), id="dialog")


def worker(scores):
    start = time.perf_counter()
    for i in range(int(1e7)):
        result = sqrt(abs(sin(i))+1)+log(abs(cos(i))+1)-log(sqrt(i+1))
    end = time.perf_counter()
    elapsed = end - start
    score = round(100000/elapsed, 1)
    scores.append(score)

class CPU_MultiThread_Loading(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Label("CPU Multi-Threading Benchmark in progress, please wait..."),
            id="dialog"
        )

    def on_screen_resume(self):
        self.manager = Manager()
        self.shared_scores = self.manager.list()
        self.timer = self.set_interval(0.5, self.chk_value)
        self.launch_processes()

    def launch_processes(self):
        for _ in range(os.cpu_count()):
            p = Process(target=worker, args=(self.shared_scores,))
            p.start()

    def chk_value(self):
        if len(self.shared_scores) == os.cpu_count():
            common.cpu_pcore[:] = list(self.shared_scores)
            self.timer.stop()
            # self.app.call_from_thread(partial(self.app.switch_screen, "cpu_results"))
            self.app.switch_screen("results")



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

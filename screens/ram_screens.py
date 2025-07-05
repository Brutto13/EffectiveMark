import asyncio

from textual.app import ComposeResult
from textual.widgets import ListItem, ListView, Label
from textual.screen import Screen
from textual.containers import Container

from sources.ram_benchmark import *
import variables as common


class RAMConfirm(Screen):

    def compose(self) -> ComposeResult:
        yield Container(
            Label("Run RAM Benchmark"),
            ListView(
                ListItem(Label("Yes"), id="Y"),
                ListItem(Label("No"), id="N"),
                id="menu-list"
            ),
            id="dialog"
        )

    def on_list_view_selected(self, event):
        if event.item.id == "Y":
            self.app.switch_screen("RAMProgress")
            # asyncio.create_task(self.ExecuteRAMBenchmark())
        elif event.item.id == "N":
            self.app.switch_screen("StartScreen")

class RAMProgress(Screen):
    async def ExecuteRAMBenchmark(self):
        # global common.ram_score
        common.ram_score = await asyncio.to_thread(ram_benchmark)
        # self.app.switch_screen("results")
        await self.app.switch_screen("results")

    def on_mount(self):
        asyncio.create_task(self.ExecuteRAMBenchmark())

    def compose(self):
        yield Container(Label("RAM Benchmark in progress, Please wait..."), id="dialog")

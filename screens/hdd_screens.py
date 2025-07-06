import asyncio

from textual import events
from textual.app import ComposeResult
from textual.widgets import ListItem, ListView, Label
from textual.screen import Screen
from textual.containers import Container, Vertical

from sources.hdd_benchmark import hdd_benchmark
import variables as common

class HDDConfirm(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Label("Run HDD Benchmark?"),
            ListView(
                ListItem(Label("Yes"), id="Y"),
                ListItem(Label("No"), id="N"),
                id="menu-list"
            ),
            id="dialog"
        )

    def on_list_view_selected(self, event):
        if event.item.id == "Y": self.app.switch_screen("hdd-benchmark")
        elif event.item.id == "N": self.app.switch_screen("StartScreen")


class HDDPermissionError(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Failed to run HDD Benchmark"),
            Label("Error Details: PermissionError:"),
            Label("Not enough permissions to read/write files"),
            Label("Run application as admin and try again"),
            id="dialog"
        )

    def _on_key(self, event: events.Key) -> None:
        if event.key == "q": self.app.switch_screen("StartScreen")


class HDDBenchmark(Screen):
    async def run_benchmark(self):
        common.hdd_read, common.hdd_write = await asyncio.to_thread(hdd_benchmark, size_gb=0.1)
        if not common.hdd_read: await self.app.switch_screen("hdd-error")
        else: await self.app.switch_screen("results")

    def compose(self) -> ComposeResult:
        yield Container(
            Label("HDD Benchmark Running, Please wait..."),
            id="dialog"
        )

    def on_screen_resume(self): asyncio.create_task(self.run_benchmark())

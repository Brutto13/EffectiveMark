import asyncio

from textual.app import ComposeResult
from textual.widgets import ListItem, ListView, Label, Header
from textual.screen import Screen
from textual.containers import Container

from benchmarking.sources.eth_benchmark import *

import variables as common

class SpeedConfirm(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("Run Connection Speed Test?"),
            ListView(
                ListItem(Label("Yes"), id="Y"),
                ListItem(Label("No"), id="N"),
                id="menu-list"
            ),
            id="dialog"
        )

    def on_list_view_selected(self, event):
        if event.item.id == "Y": self.app.switch_screen("SpeedProgress")
        elif event.item.id == "N": self.app.switch_screen("StartScreen")


class SpeedProgress(Screen):
    async def ExecuteSpeedTest(self):
        common.download, common.upload, common.ping = await asyncio.to_thread(eth_benchmark)
        await self.app.switch_screen("results")

    def on_show(self):
        asyncio.create_task(self.ExecuteSpeedTest())

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(Label("Measuring Connection Speed"), id="dialog")

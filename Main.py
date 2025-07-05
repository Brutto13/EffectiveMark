# UI Imports
from textual.app import App, ComposeResult
from textual.widgets import ListItem, ListView, Label  # , Input, Button, ProgressBar, Static
from textual.screen import Screen
# from textual.reactive import reactive
from textual.containers import Vertical, Container

# General Imports
import psutil
import os
import sys
import asyncio

# CPU-related imports

# Ethernet-Related tests
import speedtest

# GPU-related imports
import moderngl
import moderngl_window as mglw
import threading
import GPUtil

# Internal files imports
from sources.gpu_benchmark import *
from sources.ram_benchmark import *
from sources.eth_benchmark import *

from screens.cpu_screens import *
from screens.gpu_screens import *

# globals
CPU_CORES = os.cpu_count()
CPU_FREQC = psutil.cpu_freq().current
RAM_DETEC = round(psutil.virtual_memory().total/(1024**3), 1)
GPU_NAME0 = GPUtil.getGPUs()[0].name

cpu_score: float | str = "N/A"
gpu_score: float | str = "N/A"
ram_score: float | str = "N/A"
download:  float | str = "N/A"
upload:    float | str = "N/A"
ping:      float | str = "N/A"



# Communications
run_threads: int = 1


class SpeedConfirm(Screen):
    def compose(self) -> ComposeResult:
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
        await asyncio.to_thread(eth_benchmark)
        self.app.switch_screen("results")

    def on_show(self):
        asyncio.create_task(self.ExecuteSpeedTest())

    def compose(self) -> ComposeResult:
        yield Container(Label("Measuring Connection Speed"), id="dialog")


class SystemOverview(Screen):
    def compose(self):
        yield Vertical(
            Label(F"CPU Cores Detected: {CPU_CORES}"),
            Label(F"CPU Stock Frequency: {CPU_FREQC}MHz"),
            Label(F"RAM Detected: {RAM_DETEC}GB"),
            Label(F"GPU0 Name: {GPU_NAME0}"),
            id="dialog"
        )

    def on_key(self, event):
        if event.key == "q":
            self.app.pop_screen()


class BenchmarkResults(Screen):
    def __init__(self):  #, cpu_score, ram_score, ethernet: tuple[float, float, float]):
        # Ethernet: DWNL-UPLD-PING
        super().__init__()
        # Initialize label placeholders (they'll be assigned in compose)
        self.cpu_label = Label(F"CPU Benchmark Score:  N/A")
        self.ram_label = Label(F"RAM Benchmark Score:  N/A")
        self.gpu_label = Label(F"GPU Benchmark FPS:..  N/A FPS")
        self.download_label = Label(F"Download Rate:...... N/A Mbps")
        self.upload_label = Label(F"Upload Rate:......... N/A Mbps")
        self.ping_label = Label(F"Ping:............... N/A ms")

    def compose(self) -> ComposeResult:
        yield Vertical(
            self.cpu_label,
            self.ram_label,
            self.gpu_label,
            self.download_label,
            self.upload_label,
            self.ping_label,
            id="dialog"
        )

    def on_screen_resume(self):
        global cpu_score, ram_score, download, upload, ping, gpu_score
        self.cpu_label.update(F"CPU Benchmark Score: {cpu_score}")
        self.ram_label.update(F"RAM Benchmark Score: {ram_score}")
        self.gpu_label.update(F"GPU Benchmark FPS:...{gpu_score} FPS")
        self.download_label.update(F"Download Rate:.......{download} Mbps")
        self.upload_label.update(F"Upload Rate:.........{upload} Mbps")
        self.ping_label.update(F"Ping:................{ping} ms")
    # def on_show(self):
        # self.cpu_label.update(F"CPU Benchmark Score: {self.cpu_score}")
        # self.ram_label.update(F"RAM Benchmark Score: {self.ram_score}")

    def on_key(self, event):
        if event.key == "q":
            self.app.switch_screen("StartScreen")

class StartScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Effective Mark V1.2")
        yield Container(ListView(
            ListItem(Label("1. System Overview"), id="sys"),
            ListItem(Label("2. Run CPU Benchmark"), id="cpu"),
            ListItem(Label("3. Run RAM Benchmark"), id="ram"),
            ListItem(Label("4. Run GPU Benchmark"), id="gpu"),
            ListItem(Label("5. Run Connection Benchmark"), id="eth0"),
            ListItem(Label("6. Benchmark Results"), id="res"),
            ListItem(Label("7. Exit"), id="off"),
            id="menu-list"
        ),
        id="dialog")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        choice = event.item.id

        if choice == "sys": self.app.push_screen("SystemOverview")  # System Overview
        else:
            # self.app.exit()
            if choice == "cpu":    self.app.switch_screen("CPUConfirm")
            elif choice == "ram":  self.app.switch_screen("RAMConfirm")
            elif choice == "res":  self.app.switch_screen("results")
            elif choice == "eth0": self.app.switch_screen("SpeedConfirm")
            elif choice == "gpu":  self.app.switch_screen("GPUSelect")
            elif choice == "off":  sys.exit(0)

        # elif choice=="cpu": self.app.push_screen() #CPU Benchmark
        # elif choice=="ram": self.app.push_screen() #RAM Benchmark
        # elif choice=="off": quit()

class LauncherApp(App):
    SCREENS = {
        "StartScreen": StartScreen,
        "SystemOverview": SystemOverview,
        "InProgress": CPU_SingleThread_Loading,
        "results": BenchmarkResults,
        "CPUConfirm": CPU_Select,
        "RAMConfirm": RAMConfirm,
        "RAMProgress": RAMProgress,
        "SpeedConfirm": SpeedConfirm,
        "SpeedProgress": SpeedProgress,
        "GPUArithmeticTest": GPUArithmeticTest,
        "GPUSelect": GPUSelect
    }

    CSS = """
    
    Screen {
        background: #3C3C3C;
        /*background: blue;*/
        
    }
    
    #dialog {
        background: grey;
        border: round lightgrey;
        padding: 2;
        align: center middle;
        width: 50%;
        height: 40%;
    }
    
    StartScreen, SystemOverview, CPU_Select, CPU_SingleThread_Loading, RAMConfirm, RAMProgress, SpeedConfirm, SpeedProgress, BenchmarkResults, GPUSelect, GPUArithmeticTest {
        align: center middle;
    }

    Button {
        width: 100%;
    }
    
    #menu-list {
        width: 100%;
    }

    ListItem {
        background: grey;
        border: none;
        content-align: center middle;
    }

    ListView:focus ListItem.--highlight {
        background: cadetblue;
        color: black;
    }
    
    """

    def on_mount(self):
        self.push_screen(StartScreen())

    # def compose(self) -> ComposeResult:
    #     yield Container(StartScreen(), id="dialog")

if __name__ == "__main__":
    import multiprocessing as mp
    mp.set_start_method("spawn")
    mp.freeze_support()
    LauncherApp().run()
    # app = LauncherApp()
    # result = app.run()


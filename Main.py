# UI Imports
from textual.app import App, ComposeResult
from textual.widgets import ListItem, ListView, Label  # , Input, Button, ProgressBar, Static
from textual.screen import Screen
from textual.containers import Vertical, Container

# General Imports
import psutil
import os
import sys

# CPU-related imports
import subprocess

# GPU-related imports
import GPUtil

# Internal files imports
from screens.cpu_screens import *
from screens.gpu_screens import *
from screens.ram_screens import *
from screens.eth_screens import *
from screens.hdd_screens import *
import variables as common

import subprocess

try: print(sys._MEIPASS)
except: pass

def get_cpu_name():
    try:
        output = subprocess.check_output(
            "wmic cpu get Name", shell=True
        ).decode(errors="ignore").split("\n")[1].strip()
        return output or "Unknown"
    except Exception as e:
        return f"Error: {e}"


# Constants
CPU_NAME0 = get_cpu_name()
CPU_CORES = os.cpu_count()
CPU_FREQC = psutil.cpu_freq().current
RAM_DETEC = round(psutil.virtual_memory().total/(1024**3), 1)
try: GPU_NAME0 = GPUtil.getGPUs()[0].name
except IndexError: GPU_NAME0 = F"Integrated Graphics ({CPU_NAME0})"


# Communications
run_threads: int = 1

class SystemOverview(Screen):
    def compose(self):
        yield Vertical(
            Label(F"CPU Name:  {CPU_NAME0}"),
            Label(F"CPU Cores: {CPU_CORES}"),
            Label(F"GPU Name:  {GPU_NAME0}"),
            Label(F"RAM Total: {RAM_DETEC} GB"),
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
        self.hdd_read_label = Label(F"HDD Read Rate:...... N/A MB/s")
        self.hdd_write_label = Label(F"HDD Write Rate:..... N/A MB/s")

    def compose(self) -> ComposeResult:
        yield Vertical(
            self.cpu_label,
            self.ram_label,
            self.gpu_label,
            self.hdd_read_label,
            self.hdd_write_label,
            self.download_label,
            self.upload_label,
            self.ping_label,
            id="dialog"
        )

    def on_screen_resume(self):
        # global cpu_score, ram_score, download, upload, ping, gpu_score
        self.cpu_label.update(F"CPU Benchmark Score: {common.cpu_score}")
        self.ram_label.update(F"RAM Benchmark Score: {common.ram_score}")
        self.gpu_label.update(F"GPU Benchmark FPS:.. {common.gpu_score} FPS")
        self.download_label.update(F"Download Rate:...... {common.download} Mbps")
        self.upload_label.update(F"Upload Rate:........ {common.upload} Mbps")
        self.ping_label.update(F"Ping:............... {common.ping} ms"),
        self.hdd_read_label.update(F"HDD Read Rate:...... {round(common.hdd_read, 1)} MB/s")
        self.hdd_write_label.update(F"HDD Write Rate:..... {round(common.hdd_write, 1)} MB/s")

    # def on_show(self):
        # self.cpu_label.update(F"CPU Benchmark Score: {self.cpu_score}")
        # self.ram_label.update(F"RAM Benchmark Score: {self.ram_score}")

    def on_key(self, event):
        if event.key == "q":
            self.app.switch_screen("StartScreen")


class StartScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Effective Mark V1.0")
        yield Container(ListView(
            ListItem(Label("1. System Overview"), id="sys"),
            ListItem(Label("2. Run CPU Benchmark"), id="cpu"),
            ListItem(Label("3. Run RAM Benchmark"), id="ram"),
            ListItem(Label("4. Run GPU Benchmark"), id="gpu"),
            ListItem(Label("5. Run Connection Benchmark"), id="eth0"),
            ListItem(Label("6. Run HDD Benchmark"), id="hdd"),
            ListItem(Label("7. Benchmark Results"), id="res"),
            ListItem(Label("8. Exit"), id="off"),
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
            elif choice == "hdd":  self.app.switch_screen("HDDConfirm")
            elif choice == "off":  sys.exit(0)


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
        "GPUSelect": GPUSelect,
        "HDDConfirm": HDDConfirm,
        "hdd-benchmark": HDDBenchmark,
        "hdd-error": HDDPermissionError
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
        height: 50%;
    }
    
    StartScreen, SystemOverview, CPU_Select, CPU_SingleThread_Loading, RAMConfirm, RAMProgress, SpeedConfirm, SpeedProgress, BenchmarkResults, GPUSelect, GPUArithmeticTest, HDDConfirm, HDDBenchmark, HDDPermissionError {
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
        /* background: cadetblue;*/
        color: white;
        /* color: black;*/
    }
    
    """

    def on_mount(self):
        self.push_screen(StartScreen())


if __name__ == "__main__":
    LauncherApp().run()

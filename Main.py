# UI Imports
from textual.app import ComposeResult, App
from textual.widgets import ListItem, ListView, Label
from textual.screen import Screen
from textual.containers import Container

# General Imports
import psutil

# CPU-related imports
import subprocess

# GPU-related imports
import GPUtil

# Internal files imports
from benchmarking.screens.cpu_screens import *
from benchmarking.screens.ram_screens import *
from benchmarking.screens.gpu_screens import *
from benchmarking.screens.eth_screens import *
from benchmarking.screens.hdd_screens import *
from benchmarking.screens.results_screen import *
from benchmarking.screens.combined_screen import *

from stability.screens.cpu_screens import *
from stability.screens.ram_screens import *
from stability.sources.cpu_testing import try_fetch_dll


import variables as common

def get_cpu_name():
    try:
        output = subprocess.check_output(
            "wmic cpu get Name", shell=True
        ).decode(errors="ignore").split("\n")[1].strip()
        return output or "Unknown"
    except Exception:
        return "Not available"


class SystemOverview(Screen):
    def __init__(self):
        super().__init__()
        self.table = DataTable(cursor_type='none')

    def compose(self):
        yield Container(
            self.table,
            id='dialog'
        )

    def on_screen_resume(self):
        ROWS = [
            ("Device", "Property", ""),
            ("CPU", "Name", F"{CPU_NAME0}"),
            ("",    "Cores", F"{CPU_CORES}"),
            ("",    "Frequency", F"{round(CPU_FREQC, -1)} MHz"),
            ("RAM", "Capacity", F"{RAM_DETEC} GB"),
            ("GPU", "Name", F"{GPU_NAME0}")
        ]

        table = self.query_one(DataTable)
        try:
            for col in ROWS[0]:
                table.add_column(col, key=col)
        except Exception:
            pass

        # Update content (Delete and re-append)
        table.clear(columns=False)
        for row in ROWS[1:]:
            table.add_row(*row)

    def on_key(self, event):
        if event.key == "q":
            self.app.switch_screen('AppStart')


class BenchmarkStart(Screen):
    def compose(self) -> ComposeResult:
        yield Container(ListView(
            ListItem(Label("1. System Overview"), id="sys"),
            ListItem(Label("2. Run CPU Benchmark"), id="cpu"),
            ListItem(Label("3. Run RAM Benchmark"), id="ram"),
            ListItem(Label("4. Run GPU Benchmark (deprecated)"), id="gpu"),
            ListItem(Label("5. Run Internet Speed Test"), id="eth0"),
            ListItem(Label("6. Run HDD Read/Write Speed test"), id="hdd"),
            ListItem(Label("7. Benchmark Results"), id="res"),
            ListItem(Label("8. Run Combined Test"), id='cmb'),
            ListItem(Label("9. Return"), id="off"),
            id="menu-list"
        ),
        id="dialog")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        choice = event.item.id

        if choice == "sys":    self.app.switch_screen("SystemOverview")  # System Overview
        elif choice == "cpu":  self.app.switch_screen("CPUConfirm")
        elif choice == "ram":  self.app.switch_screen("RAMConfirm")
        elif choice == "res":  self.app.switch_screen("results")
        elif choice == "eth0": self.app.switch_screen("SpeedConfirm")
        elif choice == "gpu":  self.app.switch_screen("GPUSelect")
        elif choice == "hdd":  self.app.switch_screen("HDDConfirm")
        elif choice == "cmb":  self.app.switch_screen("Combined")
        elif choice == "off":  self.app.switch_screen("AppStart")


class StabilityCheck(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            ListView(
                ListItem(Label("CPU Stability Test"), id='cpu'),
                ListItem(Label("RAM Stability Test"), id='ram'),
                ListItem(Label("GPU Stability Test"), id='gpu'),
                ListItem(Label("Return"), id='off'),
                id='menu-list'
            ),
            id='dialog'
        )

    def on_list_view_selected(self, event):
        choice = event.item.id
        if choice == 'cpu': self.app.switch_screen('CPUStability')
        elif choice == 'ram': self.app.switch_screen('RAMStability')
        elif choice == 'gpu': pass
        elif choice == 'off': self.app.switch_screen('AppStart')


class Start(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Effective Mark V1.1")
        yield Container(
            ListView(
                ListItem(Label("System Overview"), id='sys'),
                ListItem(Label("Benchmarks"), id='benchmark'),
                ListItem(Label("Stability Tests"), id='tests'),
                ListItem(Label("Exit App"), id='off'),
                id='menu-list'
            ),
            id='dialog'
        )

    def on_list_view_selected(self, event):
        choice = event.item.id
        if choice == "sys": self.app.switch_screen("SystemOverview")
        elif choice == "benchmark": self.app.switch_screen("StartScreen")
        elif choice == "tests": self.app.switch_screen("StabilityScreen")
        elif choice == "off": self.app.exit()


class MissingDLL(Screen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Failed to load OpenHardwareMonitor.dll"),
            Horizontal(Button("Continue", id='ok')),
            id='dialog'
        )

    def on_button_pressed(self, event):
        self.app.switch_screen('AppStart')
        # elif choice == 'off': quit()


class LauncherApp(App):
    SCREENS = {
        "StartScreen": BenchmarkStart,
        "StabilityScreen": StabilityCheck,
        "SystemOverview": SystemOverview,
        "AppStart": Start,
        "InProgress": CPU_SingleThread_Loading,
        "FullProgress": CPU_MultiThread_Loading,
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
        "hdd-error": HDDPermissionError,
        "Combined": CombinedTest,
        "CombinedRunning": CombinedRunning,
        "CPUStability": CPUTest,
        "RAMStability": RAMTest,
        "RAMError": RAMError
    }

    CSS = """
    Screen {
        /*background: #3C3C3C;*/
        background: darkblue;
        align: center middle;
    }
    
    #table-container {
        margin: 100 100;
    }
    
    DataTable {
        background: grey;
        color: black;
        border: round heavy black;
    }
    
    /*    
    DataTable.header-cell {
        color: red;
    }
    */
    
    Checkbox {
        color: grey;
    }
    
    #checkbox1, #checkbox2 {
        content-align: center middle;
        border: round black;
        min-height: 5;
    }
    
    Button {
        max-height: 3;
        width: 100%;
    }
    
    #dialog {
        background: grey;
        border: round lightgrey;
        padding: 2;
        align: center middle;
        width: 50%;
        height: 50%;
        layout: vertical;
    }
    
    #dialog2 {
        background: grey;
        border: round lightgrey;
        padding: 2;
        align: center middle;
        width: 50%;
        height: 70%;
        layout: vertical;
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
        color: white;
    }
       
    """

    def on_mount(self):
        if common.dll_found: self.push_screen(Start())
        else: self.push_screen(MissingDLL())


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    common.dll_found = try_fetch_dll()

    # Constants
    CPU_NAME0 = get_cpu_name()
    CPU_CORES = os.cpu_count()
    CPU_FREQC = psutil.cpu_freq().current
    RAM_DETEC = round(psutil.virtual_memory().total / (1024 ** 3), 1)

    # Try to get GPU info. IGFX fallback on error
    try: GPU_NAME0 = GPUtil.getGPUs()[0].name
    except IndexError: GPU_NAME0 = "Integrated Graphics"

    LauncherApp().run()

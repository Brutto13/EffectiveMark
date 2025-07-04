# Unstable packages
import numpy as np
import psutil
import asyncio
import moderngl
from textual.app import App, ComposeResult
from textual.widgets import ListItem, ListView, Label, Input, Button, ProgressBar, Static
from textual.screen import Screen
from textual.reactive import reactive
from textual.containers import Vertical, Container

# General Imports (external: psutil)
import time
import os
import sys
import asyncio
# CPU-related imports

from math import sin, cos, log, sqrt

# Ethernet-Related tests (external: "speedtest-cli")
import speedtest

import multiprocessing as mp
from methods import *

# GPU-related imports
import moderngl
import moderngl_window as mglw
import threading

# globals
CPU_CORES = os.cpu_count()
CPU_FREQC = psutil.cpu_freq().current
RAM_DETEC = round(psutil.virtual_memory().total/(1024**3), 1)

cpu_score: float | str = "N/A"
ram_score: float | str = "N/A"
download:  float | str = "N/A"
upload:    float | str = "N/A"
ping:      float | str = "N/A"

gpu_score: float | str = "N/A"

# Communications
run_threads: int = 1

def eth_benchmark():
    global download
    global upload
    global ping

    st = speedtest.Speedtest()
    st.get_best_server()
    download = round(st.download()/1e6, 1)  # Unit: Mbps
    upload = round(st.upload()/1e6, 1)  # Unit: Mbps
    ping = round(st.results.ping, 1)  # Unit: ms



def ram_benchmark(size: int=2e9):
    testlist = []
    writestart = time.perf_counter()
    for i in range(int(size)):
        testlist.append(7)
    writeend = time.perf_counter()
    writetime = writeend-writestart

    readstart = time.perf_counter()
    x = sum(testlist)
    readend = time.perf_counter()

    readtime = readend-readstart

    return round((1e5/writetime)*(1e5/readstart), 1)

# CPU Tests
class CPU_SingleThread_Loading(Screen):
    async def ExecuteCPUBenchmark(self):
        global cpu_score
        score, _ = await asyncio.to_thread(raw_cpu_benchmark, iterations=int(2e7))
        cpu_score = score
        del _
        # cpu_score = await asyncio.to_thread(cpu_benchmark, cores=run_threads)
        self.app.push_screen(BenchmarkResults(cpu_score, ram_score, (download, upload, ping)))

    def on_show(self): asyncio.create_task(self.ExecuteCPUBenchmark())

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


# RAM tests
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
        global ram_score
        ram_score = await asyncio.to_thread(ram_benchmark)
        # self.app.switch_screen("results")
        self.app.push_screen(BenchmarkResults(cpu_score, ram_score, (download, upload, ping)))

    def on_show(self):
        asyncio.create_task(self.ExecuteRAMBenchmark())

    def compose(self):
        yield Container(Label("RAM Benchmark in progress, Please wait..."), id="dialog")

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
        self.app.push_screen(BenchmarkResults(cpu_score, ram_score, (download, upload, ping)))

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
            id="dialog"
        )

    def on_key(self, event):
        if event.key == "q":
            self.app.pop_screen()


class GPUSelect(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Label("Run GPU Benchmark"),
            ListView(
                ListItem(Label("Yes"), id="Y"),
                ListItem(Label("No"), id="N"),
                id="menu-list"
            ),
            id="dialog"
        )

    def on_list_view_selected(self, event):
        if event.item.id == "Y": self.app.switch_screen("GPUArithmeticTest")
        elif event.item.id == "N": self.app.switch_screen("StartScreen")
        # elif event.item.id == "llm": self.app.switch_screen("LLMTest")

def generate_grid_triangles(grid_size=100, quad_size=0.02):
    """
    Tworzy siatkę quadów, każdy quad to 2 trójkąty, razem 6 wierzchołków na quad.
    grid_size - liczba quadów w jednym wierszu/kolumnie
    quad_size - wielkość boku quada
    """
    vertices = []
    start = -1.0
    for y in range(grid_size):
        for x in range(grid_size):
            # pozycja lewego dolnego rogu quada
            x0 = start + x * quad_size
            y0 = start + y * quad_size
            x1 = x0 + quad_size
            y1 = y0 + quad_size

            # dwa trójkąty na quad
            vertices.extend([
                x0, y0,
                x1, y0,
                x0, y1,

                x1, y0,
                x1, y1,
                x0, y1,
            ])
    return np.array(vertices, dtype='f4')

class GPUStressTest(mglw.WindowConfig):
    # gl_version = (3, 3)
    title = "EffectiveMark V1.2 - GPU Render Test"
    window_size = (900, 850)
    resource_dir = "."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        vertex_shader = """
                #version 330
                in vec2 in_position;
                void main() {
                    gl_Position = vec4(in_position, 0.0, 1.0);
                }
                """

        fragment_shader = """
                #version 330
                out vec4 f_color;

                // Funkcja obciążająca GPU
                float heavyCalc(float x) {
                    float v = x;
                    for (int i = 0; i < 1000000; i++) {
                        v = exp(sin(cos(log(v+1))) + sqrt(abs(cos(sin(v*1.1)))) + log(sqrt(abs(v))+1));
                        v = mod(v, 1.0);
                    }
                    return v;
                }

                void main() {
                    float val = heavyCalc(gl_FragCoord.x * 0.01);
                    f_color = vec4(val, val * 0.5, 1.0 - val, 1.0);
                }
                """

        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        vertices = generate_grid_triangles(grid_size=100, quad_size=0.02)
        self.vbo = self.ctx.buffer(vertices.tobytes())
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, "in_position")

    def on_render(self, time: float, frame_time: float) -> None:
        global gpu_score
        self.ctx.clear(0.0, 0.0, 0.0)
        self.vao.render(mode=moderngl.TRIANGLES)

        self.frame_count += 1
        elapsed = time.time() - self.start_time
        if elapsed >= self.test_duration:
            fps = round(self.frame_count / elapsed, 1)
            # print(f"Benchmark zakończony! Średni FPS: {fps:.2f}")
            gpu_score = fps
            self.wnd.close()


def start_gpu_benchmark(): mglw.run_window_config(GPUStressTest)


class GPUArithmeticTest(Screen):

    def compose(self) -> ComposeResult:
        yield Container(
            Label("GPU Arithmetic Benchmark in progress, Please wait..."),
            id="dialog"
        )

    def on_show(self):
        threading.Thread(target=start_gpu_benchmark, daemon=True).start()

class BenchmarkResults(Screen):
    def __init__(self):  #, cpu_score, ram_score, ethernet: tuple[float, float, float]):
        # Ethernet: DWNL-UPLD-PING
        super().__init__()
        global cpu_score, ram_score, download, upload, ping, gpu_score
        self.cpu_score = cpu_score
        self.gpu_score = gpu_score
        self.ram_score = ram_score
        self.download  = download
        self.upload    = upload
        self.ping      = ping

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(F"CPU Benchmark Score: {self.cpu_score}"),
            Label(F"GPU Benchmark Score: {self.gpu_score}"),
            Label(F"RAM Benchmark Score: {self.ram_score}"),
            Label(F"Download Rate:.......{self.download} Mbps"),
            Label(F"Upload Rate:.........{self.upload} Mbps"),
            Label(F"Ping:................{self.ping} ms"),
            id="dialog"
        )

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
        background: green;
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


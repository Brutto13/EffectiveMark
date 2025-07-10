import os
from statistics import mean
from textual.app import App, ComposeResult
from textual.widgets import DataTable
from textual.screen import Screen
from textual.containers import Vertical, Container, Horizontal
from textual.coordinate import Coordinate

import variables as common


class BenchmarkResults(Screen):
    def __init__(self):
        super().__init__()
        self.table = DataTable(cursor_type='none')

    def compose(self) -> ComposeResult:
        yield Container(
            self.table,
            id='dialog'
        )

    def on_screen_resume(self) -> None:

        try:
            cpu_pcore = round(mean(common.cpu_pcore), 1)
        except:
            cpu_pcore = 0

        # try: del self.table
        # except AttributeError: pass
        # finally: self.table = DataTable(cursor_type='none')
        ROWS = [
            ("Device", "Test Type", "Result"),
            ("CPU", "1 Thread", F"{common.cpu_score}"),
            ("", F"{os.cpu_count()} Threads", F"{cpu_pcore}"),
            ("RAM", "", F"{common.ram_score}"),
            ("GPU", "", F"{common.gpu_score}"),
            ("HDD/SSD", "Read", F"{common.hdd_read} MB/s"),
            ("", "Write", F"{common.hdd_write} MB/s"),
            ("Internet", "Receive", F"{common.download} Mbps"),
            ("", "Send", F"{common.upload} Mbps"),
            ("", "Ping", F"{common.ping} ms"),
        ]

        table = self.query_one(DataTable)
        try:
            for col in ROWS[0]:
                table.add_column(col, key=col)
        except Exception: pass

        # Update content (Delete and re-append)
        table.clear(columns=False)
        for row in ROWS[1:]:
            table.add_row(*row)

    def on_list_view_selected(self, event):
        choice = event.item.id
        if choice == 'cpu': self.app.switch_screen('cpu_results')
        elif choice == 'ram': self.app.switch_screen('ram_results')
        elif choice == 'gpu': self.app.switch_screen('gpu_results')
        elif choice == 'hdd': self.app.switch_screen('hdd_results')
        elif choice == 'int': self.app.switch_screen('int_results')
        elif choice == 'save': self.app.switch_screen('save_results')
        elif choice == 'exit': self.app.switch_screen('StartScreen')


    def on_key(self, event):
        if event.key == "q":
            self.app.switch_screen("StartScreen")


def ram_worker(passes, terminate_event):
    # def run_test(self):
    # passes = 0
    terminated = False
    while not terminated:
        # number = random.randint(256, 511)
        count = int(9e8)
        in_ram = [56] * count

        value = sum(in_ram)
        # if value != 56 * count:
        #     assert False
        # else:
        with passes.get_lock():
            passes.value += 1

        if terminate_event.is_set():
            terminated = True

    del in_ram, count

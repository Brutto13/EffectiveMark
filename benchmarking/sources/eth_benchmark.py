import speedtest


def eth_benchmark():
    st = speedtest.Speedtest()
    st.get_best_server()
    download = round(st.download()/1e6, 1)  # Unit: Mbps
    upload = round(st.upload()/1e6, 1)  # Unit: Mbps
    ping = round(st.results.ping, 1)  # Unit: ms
    return download, upload, ping

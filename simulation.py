import os
import subprocess
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tqdm import tqdm

sns.set_style(style='ticks')
plt.rcParams['font.size'] = 14

save_path = 'data/chapter4/'
algorithms = [
    # 'TcpNewReno',
    # 'TcpHybla',
    # 'TcpHighSpeed',
    # 'TcpHtcp',
    # 'TcpVegas',
    # 'TcpScalable',
    # 'TcpVeno',
    'TcpBic',
    # 'TcpYeah',
    # 'TcpIllinois',
    # 'TcpWestwood'.
]

if not os.path.exists(save_path):
    os.mkdir(save_path)


def make_command(
        algorithm=None, prefix_name=None, tracing=None,
        duration=None, error_p=None, bandwidth=None, delay=None,
        access_bandwidth=None, access_delay=None,
        data=None, mtu=None, flow_monitor=None, pcap_tracing=None):

    cmd = './waf --run "chapter4-base'
    if algorithm:
        cmd += ' --transport_prot={}'.format(algorithm)
    if prefix_name:
        cmd += ' --prefix_name={}'.format(prefix_name)
    if tracing:
        cmd += ' --tracing={}'.format(tracing)
    if duration:
        cmd += ' --duration={}'.format(duration)
    if error_p:
        cmd += ' --error_p={}'.format(error_p)
    if bandwidth:
        cmd += ' --bandwidth={}'.format(bandwidth)
    if delay:
        cmd += ' --delay={}'.format(delay)
    if access_bandwidth:
        cmd += ' --access_bandwidth={}'.format(access_bandwidth)
    if access_delay:
        cmd += ' --access_delay={}'.format(access_delay)
    if data:
        cmd += ' --data={}'.format(data)
    if mtu:
        cmd += ' --mtu={}'.format(mtu)
    if flow_monitor:
        cmd += ' --flow_monitor={}'.format(flow_monitor)
    if pcap_tracing:
        cmd += ' --pcap_tracing={}'.format(pcap_tracing)
    cmd += '"'

    return cmd


def read_data(prefix_name, metric, duration):
    file_name = '{}{}.data'.format(prefix_name, metric)
    data = pd.read_table(
        file_name, names=['sec', 'value'], delimiter=' ')
    data = data[data.sec <= duration].reset_index(
        drop=True)

    if duration > data.sec.max():
        tail = data.tail(1)
        tail.sec = duration
        data = pd.concat([data, tail])
    return data


def plot_metric(
        metric, x_max, y_label, y_max=None,
        y_deno=1, x_ticks=False):

    plt.step(
        metric.sec, metric.value/y_deno,
        c='k', where='pre')
    plt.xlim(0, x_max)
    plt.ylabel(y_label)

    if y_max:
        plt.ylim(0, y_max)

    if x_ticks:
        plt.xlabel('time[s]')
    else:
        plt.xticks([])


def plot_cong_state(
        cong_state,
        x_max,
        y_label,
        x_ticks=False
    ):

    new_state = {0: 0, 1: 1, 3: 2, 4: 3}

    plt.fill_between(
        [0, x_max],
        [0, 0],
        [1, 1],
        facecolor='gray')

    for target_state in range(4):
        for sec, state in cong_state.values:
            if new_state[state] == target_state:
                color = 'gray'
            else:
                color = 'white'

            plt.fill_between(
                [sec, x_max],
                [target_state, target_state],
                [target_state+1, target_state+1],
                facecolor=color)

    for i in range(1, 4):
        plt.plot([0, x_max], [i, i], 'k-')

    plt.xlim(0, x_max)
    plt.ylim(0, 4)
    plt.yticks(
        [0.5, 1.5, 2.5, 3.5],
        ['open', 'disorder', 'recovery', 'loss'])
    plt.ylabel(y_label)

    if x_ticks:
        plt.xlabel('time[s]')
    else:
        plt.xticks([])


def plot_algorithm(algo, duration, save_path):
    path = '{}{}/'.format(save_path, algo)

    cwnd = read_data(path, 'cwnd', duration)
    ssth = read_data(path, 'ssth', duration)
    rtt = read_data(path, 'rtt', duration)
    cong_state = read_data(path, 'cong-state', duration)

    plt.figure(figsize=(12, 12))
    plt.subplot(4, 1, 1)
    plot_metric(cwnd, duration, 'cwnd[byte]')
    plt.title(algo)
    plt.subplot(4, 1, 2)
    plot_metric(
        ssth, duration, 'ssth[byte]',
        y_max=cwnd['value'].max())
    plt.subplot(4, 1, 3)
    plot_metric(rtt, duration, 'rtt[s]')
    plt.subplot(4, 1, 4)
    plot_cong_state(
        cong_state, duration, 'cong-state',
        x_ticks=True)

    plt.savefig('{}04_{}.png'.format(
        save_path, algo.lower()))


def execute_and_plot(
        algo, duration, save_path=save_path, error_p=None,
        bandwidth=None, delay=None, access_bandwidth=None,
        access_delay=None, data=None, mtu=None,
        flow_monitor=None, pcap_tracing=None):

    path = '{}{}/'.format(save_path, algo)
    if not os.path.exists(path):
        os.mkdir(path)

    cmd = make_command(
        algorithm=algo, tracing=True,
        duration=duration, prefix_name=path,
        error_p=error_p, bandwidth=bandwidth, delay=delay,
        access_bandwidth=access_bandwidth,
        access_delay=access_delay,
        data=data, mtu=mtu, flow_monitor=flow_monitor,
        pcap_tracing=pcap_tracing)

    subprocess.check_output(cmd, shell=True).decode()
    plot_algorithm(algo, duration, save_path)


def main():
    for algo in tqdm(algorithms, desc='Algotirhms'):
        execute_and_plot(algo=algo, duration=20)


if __name__ == '__main__':
    main()

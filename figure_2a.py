import matplotlib.pyplot as plt

def load_QoS_file(filename):
    dic = {}
    latency = []
    throughput = []
    batch = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines[1:]:
            lst = line.split(",")
            batch.append(float(lst[0]))
            latency.append(float(lst[1])/60)
            throughput.append(float(lst[2]))
    dic["batch"] = batch
    dic["latency"] = latency
    dic["throughput"] = throughput
    return dic

def latency_plot():
    dic_GPU_70B_4k = load_QoS_file("data/GPU_70B_4k.csv")
    dic_GPU_70B_8k = load_QoS_file("data/GPU_70B_8k.csv")
    dic_GPU_70B_16k = load_QoS_file("data/GPU_70B_16k.csv")
    dic_GPU_70B_32k = load_QoS_file("data/GPU_70B_32k.csv")

    font=24

    # matplotlib.rcParams['font.family'] = 'Times New Roman'
    # matplotlib.rcParams['font.weight'] = 'bold'

    plt.figure(figsize=(10, 8))

    plt.plot(dic_GPU_70B_4k["batch"], dic_GPU_70B_4k["latency"], marker='o', linestyle='-', color='Red', label="Context=4k")
    plt.plot(dic_GPU_70B_8k["batch"], dic_GPU_70B_8k["latency"], marker='o', linestyle='-', color='Blue', label="Context=8k")
    plt.plot(dic_GPU_70B_16k["batch"], dic_GPU_70B_16k["latency"], marker='o', linestyle='-', color='Green', label="Context=16k")

    # Llama2-70B SLA
    # https://mlcommons.org/2024/03/mlperf-llama2-70b/
    # 512 Prefill + 3584 Decoding
    SLA = (2 + 3584 * 0.2) / 60

    plt.plot([0, 128], [SLA, SLA], linestyle='--', color='Black', label="SLA")
    plt.legend(loc="upper left", fontsize=font)
    plt.tick_params(axis='x', labelsize=font)
    plt.tick_params(axis='y', labelsize=font)
    plt.xlabel('Batch Size', fontsize=font)
    plt.ylabel('Query Latency (min)', fontsize=font)
    plt.savefig('figure_2a.pdf')

latency_plot()
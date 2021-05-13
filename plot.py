import json
import matplotlib.pyplot as plt


def roll_avg(row, N):
	cumsum, moving_aves = [0], []
	for i, x in enumerate(row, 1):
		cumsum.append(cumsum[i - 1] + x)
		if i >= N:
			moving_ave = (cumsum[i] - cumsum[i - N]) / N
			# can do stuff with moving_ave here
			moving_aves.append(moving_ave)
	return moving_aves


def plot_runs():
	fig, ax = plt.subplots(nrows=1, ncols=2)
	with open("logs/best_costs.jsonl", "r") as fcosts:
		costs = []
		for line in fcosts:
			costs.append(json.loads(line))
	with open("logs/unique_pitches.jsonl", "r") as fpitches:
		pitches = []
		for line in fpitches:
			pitches.append(roll_avg(json.loads(line), 20))
	datas = [costs, pitches]
	titles = ["best costs", "unique pitches"]
	for i, (data, title) in enumerate(zip(datas, titles)):
		ax[i].title.set_text(title)
		for row in data:
			ax[i].plot(range(len(row)), row)
	plt.show()


def plot_final_costs():
	with open("logs/final_costs.jsonl", "r") as fcosts:
		costs = []
		for line in fcosts:
			costs = json.loads(line)
			break
	plt.bar(range(len(costs)), costs)
	plt.suptitle("Final costs")
	plt.show()


if __name__ == '__main__':
	plot_runs()

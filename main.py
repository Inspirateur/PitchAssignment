import dummy_data as dummy
from evolutionary_solver import solve


def main():
	dummy.generate()
	solve("dummy_pitches.csv", "dummy_wishes.csv")


if __name__ == "__main__":
	main()

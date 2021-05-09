import dummy_data as dummy
from solver import solve


def main():
	dummy.make_pitches()
	dummy.make_wishes()
	solve("dummy_pitches.csv", "dummy_wishes.csv")


if __name__ == "__main__":
	main()

import argparse

import scraper


def save_data(dataset):
    dataset.to_csv("./data/dataset.csv", mode="w")
    print("Dataset saved.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("hour", type=int)
    parser.add_argument("min", type=int)
    parser.add_argument("-d", type=int, default=None)
    parser.add_argument("-m", type=int, default=None)
    parser.add_argument("-y", type=int, default=None)
    args = parser.parse_args()
    dataset = scraper.scrape_time_series(args.hour, args.min, args.d, args.m, args.y)
    save_data(dataset)


if __name__ == "__main__":
    main()

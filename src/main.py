import scraper


def save_data(dataset):
    with open("./data/dataset.csv", "w") as csvfile:
        dataset.to_csv(csvfile)
    print("Cached.")


def main():
    dataset = scraper.scrape_time_series(0, 0, 21, 7, 2018)
    save_data(dataset)


if __name__ == "__main__":
    main()

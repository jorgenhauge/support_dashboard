import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import argparse


class DataLogger:
    def __init__(self) -> None:
        self._format_string: str = "%H:%M:%S"
        self._labels = ["u_dag", "kl_slett", "varighet", "tilfredshet"]
        self._converters = {
            "u_dag": str,
            "kl_slett": lambda ts: pd.to_datetime(ts),
            "varighet": lambda ts: pd.to_datetime(ts),
            "tilfredshet": int,
        }
        self.data = self._get_data()

    def _get_data(self):
        p = pathlib.Path(__file__).parent / "support_uke_24.xlsx"
        filename = p.absolute()
        data_xlsx: pd.DataFrame = pd.read_excel(
            filename,
            names=self._labels,
            converters=self._converters,
        )
        return data_xlsx

    @property
    def weekdays(self):
        return self.data["u_dag"]

    @property
    def at_time(self):
        return self.data["kl_slett"]

    @property
    def durations(self):
        return self.data["varighet"]

    @property
    def score(self):
        return self.data["tilfredshet"]

    def inquiries(self, _from: str, _to: str):
        return self.at_time.between(_from, _to)

    def __str__(self) -> str:
        return f"""Number of inquiries: {self.weekdays.value_counts()}
            Number of inquiries(08:00 - 10:00): {self.inquiries("08:00", "10:00").value_counts()},
            (10:00 - 12:00): {self.inquiries("10:00", "12:00").value_counts()},
            (12:00 - 14:00): {self.inquiries("12:00", "14:00").value_counts()},
            (12:00 - 14:00): {self.inquiries("14:00", "16:00").value_counts()}
            Longest inquire time: {self.durations.max().time():"%H:%M:%S"}
            Shortest inquire time: {self.durations.min().time():"%H:%M:%S"}
            Mean inquire time: {self.durations.mean().time():"%H:%M:%S"}
            """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(data={self.data}, format_string={self._format_string})"


def main():
    dl = DataLogger()
    parser = argparse.ArgumentParser(
        prog="support_dashboard", description="Support dashboard customer inquiries"
    )
    parser.add_argument(
        "--weekday-inquiries-per-day",
        help="Show number of customer inquiries for each day",
        action="store_true",
    )
    parser.add_argument(
        "--shortest-inquiry-time",
        help="Show shortest customer inquiry time",
        action="store_true",
    )
    parser.add_argument(
        "--longest-inquiry-time",
        help="Show longest customer inquiry time",
        action="store_true",
    )
    parser.add_argument(
        "--mean-inquiries-time",
        help="Show mean customer inquiries time for the week",
        action="store_true",
    )
    parser.add_argument(
        "--inquiries-between",
        help="Show number of customer inquiries between hours",
        action="store_true",
    )
    parser.add_argument(
        "--net-promoter-score",
        help="Show net promoter score for customer inquiries",
        action="store_true",
    )
    parser.add_argument(
        "-pp",
        "--pie-plot",
        help="Show pie plot for customer inquiries between hours",
        action="store_true",
    )
    args = parser.parse_args()

    if args.weekday_inquiries_per_day:
        print(dl.weekdays.value_counts())

    if args.shortest_inquiry_time:
        print(f'Shortest inquiry time: {dl.durations.min().time():"%H:%M:%S"}')

    if args.longest_inquiry_time:
        print(f'Longest inquiry time: {dl.durations.max().time():"%H:%M:%S"}')

    if args.mean_inquiries_time:
        print(f'Mean inquiries time: {dl.durations.mean().time():"%H:%M:%S"}')

    if args.inquiries_between:
        labels = [
            "08:00 -> 10:00",
            "10:00 -> 12:00",
            "12:00 -> 14:00",
            "14:00 -> 16:00",
        ]
        i = [
            int(dl.inquiries("08:00", "10:00").sum()),
            int(dl.inquiries("10:00", "12:00").sum()),
            int(dl.inquiries("12:00", "14:00").sum()),
            int(dl.inquiries("14:00", "16:00").sum()),
        ]
        print(dict(zip(labels, i)))

    if args.net_promoter_score:
        detractors = dl.score.between(1, 6, inclusive="both").sum()
        passives = dl.score.between(7, 8, inclusive="both").sum()
        promoters = dl.score.between(9, 10, inclusive="both").sum()
        total = dl.score.notna().sum()
        nps = ((promoters - detractors) / total) * 100
        print(f"NPS: {nps:.2f} %")
        # print(f"DETRACTORS: {(detractors / total) * 100:.2f} %")
        # print(f"PASSIVES: {(passives / total) * 100:.2f} %")
        # print(f"PROMOTERS: {(promoters / total) * 100:.2f} %")

    if args.pie_plot:
        fig1, ax1 = plt.subplots()
        ax1.set_title("Support dashboard customer inquiries")
        plt.pie(
            i,
            labels=labels,
        )
        plt.legend(
            i,
            loc="upper left",
            labels=labels,
            title="Number of inquiries between hours",
        )
        plt.show()


if __name__ == "__main__":
    main()

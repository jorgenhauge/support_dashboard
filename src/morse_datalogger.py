import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import argparse
import typing


class DataLogger:
    def __init__(self) -> None:
        self._format_string: str = "%H:%M:%S"
        self._labels = ["u_dag", "kl_slett", "varighet", "tilfredshet"]
        self._converters: typing.Mapping = {
            "u_dag": str,
            "kl_slett": lambda ts: pd.to_datetime(ts),
            "varighet": lambda ts: pd.to_datetime(ts),
            "tilfredshet": int,
        }
        self.data = self._get_data()

    def _get_data(self):
        try:
            p = pathlib.Path(__file__).parent / "support_uke_24.xlsx"
            filename = p.absolute()
            data_xlsx: pd.DataFrame = pd.read_excel(
                filename,
                names=self._labels,
                converters=self._converters,
            )
            return data_xlsx
        except FileNotFoundError as e:
            raise e

    def __str__(self) -> str:
        return f"{self._format_string},{self._labels},{self._converters},{self.data}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(data={self.data}, format_string={self._format_string})"


def main():
    dl = DataLogger()
    parser = argparse.ArgumentParser(
        prog="support_dashboard", description="Support dashboard customer inquiries"
    )
    parser.add_argument(
        "--weekday-inquiries-per-day",
        help="Bar plot number of customer inquiries for each day",
        action="store_true",
    )
    parser.add_argument(
        "--shortest-and-longest-inquiry-time",
        help="Print shortest and longest customer inquiry time",
        action="store_true",
    )
    parser.add_argument(
        "--mean-inquiry-time",
        help="Print mean customer inquiry time for the week",
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
        s = dl.data["u_dag"].value_counts()
        s.plot(kind="bar", ylabel="Number of inquiries per day")
        plt.show()

    if args.shortest_and_longest_inquiry_time:
        print(f'Shortest inquiry time: {dl.data["varighet"].min().time():"%H:%M:%S"}')
        print(f'Longest inquiry time: {dl.data["varighet"].max().time():"%H:%M:%S"}')       

    if args.mean_inquiry_time:
        print(f'Mean inquiry time: {dl.data["varighet"].mean().time():"%H:%M:%S"}')

    if args.inquiries_between:
        labels = [
            "08:00 -> 10:00",
            "10:00 -> 12:00",
            "12:00 -> 14:00",
            "14:00 -> 16:00",
        ]
        t = dl.data["kl_slett"]
        i = [
            int(t.between("08:00", "10:00").sum()),
            int(t.between("10:00", "12:00").sum()),
            int(t.between("12:00", "14:00").sum()),
            int(t.between("14:00", "16:00").sum()),
        ]
        print(dict(zip(labels, i)))

    if args.net_promoter_score:
        s = dl.data["tilfredshet"]
        detractors = s.between(1, 6, inclusive="both").sum()
        passives = s.between(7, 8, inclusive="both").sum()
        promoters = s.between(9, 10, inclusive="both").sum()
        total = s.notna().sum()
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

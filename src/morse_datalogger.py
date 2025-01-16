import pandas as pd
import matplotlib.pyplot as plt
import typing
import pathlib
import argparse


class DataLogger:
    def __init__(self) -> None:
        self._format_string: str = "%H:%M:%S"
        self._labels = ["u_dag", "kl_slett", "varighet", "score"]
        self._converters = {
            "u_dag": str,
            "kl_slett": lambda ts: pd.to_datetime(ts),
            "varighet": lambda ts: pd.to_datetime(ts),
            "score": str,
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

    def inquiries(self, _from: str, _to: str):
        return self.at_time.between(_from, _to)

    def __str__(self) -> str:
        return f"""Antall henvendelser: {self.weekdays.value_counts()}
            Antall henvendelser mellom(08:00 - 10:00): {self.inquiries("08:00", "10:00").value_counts()},
            (10:00 - 12:00): {self.inquiries("10:00", "12:00").value_counts()},
            (12:00 - 14:00): {self.inquiries("12:00", "14:00").value_counts()},
            (12:00 - 14:00): {self.inquiries("14:00", "16:00").value_counts()}
            Lengste samtaletid: {self.durations.max().time():"%H:%M:%S"}
            Korteste samtaletid: {self.durations.min().time():"%H:%M:%S"}
            Gjennomsnittlig samtaletid: {self.durations.mean().time():"%H:%M:%S"}
            """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(data={self.data}, format_string={self._format_string})"


def main():
    parser = argparse.ArgumentParser(
        prog="support_dashboard", description="Support dashboard customer inquiries"
    )
    parser.add_argument(
        "-pp",
        "--pie-plot",
        help="Show pie plot for customer inquiries between hours",
        action="store_true",
    )
    args = parser.parse_args()
    dl = DataLogger()
    labels = ["08:00 -> 10:00", "10:00 -> 12:00", "12:00 -> 14:00", "14:00 -> 16:00"]
    i = [
        int(dl.inquiries("08:00", "10:00").sum()),
        int(dl.inquiries("10:00", "12:00").sum()),
        int(dl.inquiries("12:00", "14:00").sum()),
        int(dl.inquiries("14:00", "16:00").sum()),
    ]
    print(dict(zip(labels, i)))
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

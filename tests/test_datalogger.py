from morse_datalogger import DataLogger
from unittest.mock import patch
import datetime
import pandas as pd


def test_is_initializable():
    with patch.object(pd, "read_excel") as mock_read_excel:
        mock_read_excel.return_value = pd.DataFrame({"test_id": [1, 2, 3, 4, 5]})
        dl = DataLogger()
        assert isinstance(dl, DataLogger)


def test_get_data() -> None:
    with patch.object(pd, "read_excel") as mock_read_excel:
        mock_read_excel.return_value = pd.DataFrame({"test_id": [1, 2, 3, 4, 5]})
        dl = DataLogger()
        pd.testing.assert_frame_equal(
            dl.data, pd.DataFrame({"test_id": [1, 2, 3, 4, 5]})
        )


def test_sum_inquries_between() -> None:
    ts = pd.date_range(
        start=pd.Timestamp("08:00:00"), end=pd.Timestamp("16:00:00"), freq="1min"
    )
    test_ids = [i for i in range(len(ts))]
    with patch.object(pd, "read_excel") as mock_read_excel:
        mock_read_excel.return_value = pd.DataFrame(
            {"test_id": test_ids, "kl_slett": ts}
        )
        dl = DataLogger()
        return_value_sum: int = dl.sum_inquries_between(
            start_time=datetime.time(hour=8, minute=00).isoformat(),
            end_time=datetime.time(hour=10, minute=00).isoformat(),
        )
        assert return_value_sum == 121

def test_min_inquiry_time() -> None:
    ts = pd.date_range(
        start=pd.Timestamp("00:00:10"), end=pd.Timestamp("01:00:01"), freq="1s"
    )
    test_ids = [i for i in range(len(ts))]
    with patch.object(pd, "read_excel") as mock_read_excel:
        mock_read_excel.return_value = pd.DataFrame(
            {"test_id": test_ids, "varighet": ts}
        )
        dl = DataLogger()
        return_value_min: str = dl.min_inquiry_time
        assert return_value_min == "h00:m00:s10"

def test_max_inquiry_time() -> None:
    ts = pd.date_range(
        start=pd.Timestamp("00:00:10"), end=pd.Timestamp("01:00:01"), freq="1s"
    )
    test_ids = [i for i in range(len(ts))]
    with patch.object(pd, "read_excel") as mock_read_excel:
        mock_read_excel.return_value = pd.DataFrame(
            {"test_id": test_ids, "varighet": ts}
        )
        dl = DataLogger()
        return_value_max: str = dl.max_inquiry_time
        assert return_value_max == "h01:m00:s01"

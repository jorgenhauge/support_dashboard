from morse_datalogger import DataLogger
from unittest.mock import patch, PropertyMock
import pandas as pd
import matplotlib.pyplot as plt


def test_initialize_and_attributes():
    dl = DataLogger()
    assert isinstance(dl, DataLogger)


def test_get_data() -> None:
    dl = DataLogger()
    with patch.object(pd, "read_excel") as mock_read_excel:
        mock_read_excel.return_value = "Bar"
        data = dl._get_data()
        print(data)
        assert data == "Bar"


@patch.object(DataLogger, "weekdays", new_callable=PropertyMock)
def test_weekday(mock_weekdays) -> None:
    test_data = [
        "Mandag",
        "Tirsdag",
        "Onsdag",
        "Torsdag",
        "Fredag",
    ]
    mock_weekdays.return_value = test_data
    dl = DataLogger()
    assert dl.weekdays == test_data


@patch.object(DataLogger, "at_time", new_callable=PropertyMock)
def test_at_time(mock_at_time) -> None:
    test_data = [
        "08:04:16",
        "08:04:16",
        "08:04:16",
        "08:04:16",
        "08:04:16",
    ]
    mock_at_time.return_value = test_data
    dl = DataLogger()
    assert dl.at_time == test_data


@patch.object(DataLogger, "durations", new_callable=PropertyMock)
def test_durations(mock_durations) -> None:
    test_data = [
        "08:04:16",
        "08:04:16",
        "08:04:16",
        "08:04:16",
        "08:04:16",
    ]
    mock_durations.return_value = test_data
    dl = DataLogger()
    assert dl.durations == test_data


@patch.object(DataLogger, "score", new_callable=PropertyMock)
def test_score(mock_score) -> None:
    test_data = [
        6,
        10,
        4,
        3,
        9,
    ]
    mock_score.return_value = test_data
    dl = DataLogger()
    assert len(dl.score) == len(test_data)

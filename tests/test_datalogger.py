from morse_datalogger import DataLogger
from unittest.mock import patch
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

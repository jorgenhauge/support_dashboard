from morse_datalogger import DataLogger
from unittest.mock import patch, PropertyMock
import pandas as pd
import pytest


def test_is_initializable():
    with patch.object(pd, "read_excel") as mock_read_excel:
        mock_read_excel.return_value = pd.DataFrame({"test_id": [1, 2, 3, 4, 5]})
        dl = DataLogger()
        assert isinstance(dl, DataLogger)


def test_get_data() -> None:
    with patch.object(pd, "read_excel") as mock_read_excel:
        mock_read_excel.return_value = pd.DataFrame({"test_id": [1, 2, 3, 4, 5]})
        dl = DataLogger()
        return_data = dl._get_data()
        pd.testing.assert_frame_equal(
            return_data, pd.DataFrame({"test_id": [1, 2, 3, 4, 5]})
        )

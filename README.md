# support-dashboard
Python fundamentals, py1010
support-dashboard is a Python library for dealing with the morse_datalogger file.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install support-dashboard.

```bash
pip install support-dashboard

```

## Run tests

```bash
support_dashboard$ pytest
pytest
======================================================================================= test session starts ========================================================================================
platform linux -- Python 3.12.3, pytest-8.3.3, pluggy-1.5.0
rootdir: /home/jorgen/src/support_dashboard
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.9.0
collected 5 items                                                                                                                                                                                  

tests/test_datalogger.py .....                                                                                                                                                               [100%]

======================================================================================== 5 passed in 0.56s =========================================================================================

```
## Usage

```bash
support-dashboard -h
usage: support_dashboard [-h] [--weekday-inquiries-per-day] [--shortest-and-longest-inquiry-time] [--mean-inquiry-time] [--inquiries-between] [--plot] [--net-promoter-score]

Support dashboard customer inquiries

options:
  -h, --help            show this help message and exit
  --weekday-inquiries-per-day
                        Bar plot number of customer inquiries for each day
  --shortest-and-longest-inquiry-time
                        Print shortest and longest customer inquiry time
  --mean-inquiry-time   Print mean customer inquiry time for the week
  --inquiries-between   Show number of customer inquiries between hours
  --net-promoter-score  Show net promoter score for customer inquiries

inquiries:
  --plot                Show pie plot for customer inquiries between hours

```

## Example usage

```bash
support-dashboard --shortest-and-longest-inquiry-time
Shortest inquiry time: h00:m00:s59
Longest inquiry time: h00:m11:s28
```
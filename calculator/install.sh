#!/bin/bash
pip install -r ./requirements.txt

ln ./MoneyCalculator.py /usr/bin/finance

chmod +x /usr/bin/finance

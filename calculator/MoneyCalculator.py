#!/bin/python3
from moneyed import Money, USD
import argparse
import requests


class financial():
    
  def __init__(self):
    # The CoinDesk API price lookup endpoint.
    self.api="https://api.coindesk.com/v1/bpi/currentprice.json"

    # The entirety of the call response
    self.data = requests.get(self.api).json()

    # The actual price in USD, formatted for use with the Money object.
    self.price = self.data["bpi"]["USD"]["rate"].replace(",","")


  def DollarsToCents(self, amount):
    """ Take a given Dollar amount and convert it to Pennies. """
    return Money(amount, USD).get_amount_in_sub_unit()


  def PriceOfBitcoin(self):
    """ To get the price of bitcoin, we simply look it up.
    Then, we convert that number into pennies. """
    # One unit of bitcoin, in USD as cents.
    return self.DollarsToCents(self.price)


  def BitcoinToSatoshi(self):
    """ To calculate the cost of a satoshi in USD
    we divide the price of bitcoin by 100,000,000. """
    # One unit of Satoshi, in USD as cents.
    return self.PriceOfBitcoin() / 100000000


  def BuyInCost(self, amount):
    """ Evaluate the buy-in price for your holdings. """
    return self.DollarsToCents(amount) * self.BitcoinToSatoshi()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  parser.add_argument( "-B", "--bitcoin",
                       help="Return the current price of Bitcoin.",
                       action="store_true"                          )

  parser.add_argument( "-C", "--cost",
                       help="Return the current buy-in cost of a certain amount of USD." )

  parser.add_argument( "-D", "--dollars",
                       help="Convert a Dollar amount to Pennies as an integer." )

  parser.add_argument( "-S", "--satoshi",
                       help="Return the price of a single satoshi in USD.",
                       action="store_true"                                  )

  parser.add_argument( "-T", "--testing",
                       help="Functionality testing suite.",
                       action="store_true"                  )


  args = parser.parse_args()

  finance = financial()


  if args.bitcoin: print(finance.PriceOfBitcoin())
  if args.cost: print(finance.BuyInCost(args.cost))
  if args.dollars: print(finance.DollarsToCents(args.dollars))
  if args.satoshi: print(finance.BitcoinToSatoshi())
  if args.testing:
    try:
      assert finance.DollarsToCents(1) == 100, "Should evaluate to 100."
      assert finance.PriceOfBitcoin(), "Should evaluate True."
      print("All facilities passed!")

    except Exception as error:
      print(error)

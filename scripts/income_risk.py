# -*- coding: utf-8 -*-
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

# Calculate income & risk V.S. order number
class Income_Risk(object):
    def __init__(self, d=20, h=12, rate=1.1, orders_safe_min=8, orders_safe_max=35, risk_rate_safe=0.005, orders_init=10, orders_adding=0, orders_is_expected=False):
        self.d = d          # Number of working days
        self.h = h          # Working hours
        self.rate = rate    # System expected/safe ratio

        self.orders_safe_min = orders_safe_min  # Min orders_safe (Day 0)
        self.orders_safe_max = orders_safe_max  # Max orders_safe (Day inf)
        self.orders_is_expected = orders_is_expected # orders_actual = orders_expected

        self.risk_rate_safe = risk_rate_safe

        self.orders_init = orders_init          # Actual number of orders at Day 0
        self.orders_adding = orders_adding      # Number of adding orders

    # Calc safe order numbers
    def Orders_safe(self, d):
        X = 2 * self.orders_safe_min - self.orders_safe_max
        Y = 2 * (self.orders_safe_max - self.orders_safe_min)
        return np.floor(X+Y/(1+np.exp((-d+1)/10)))

    # Expected order numbers by the system
    # def Orders_expected(self, orders_safe):
        # return np.ceil(orders_safe * self.rate)
    def Orders_expected(self, d):
        X = 2 * 8 - 35
        Y = 2 * (35 - 8)
        return np.floor(X+Y/(1+np.exp((-d+1)/10)))

    # Actual order numbers
    def Orders_actual(self):
        return self.orders_init + self.orders_adding

    # Average safe time per order
    def Time_per_order(self, orders):
        return self.h/orders

    # Calc actual risk rate
    def Risk_rate_actual(self, orders_actual):
        time_actual = self.Time_per_order(orders_actual)
        self.risk_rate_dangerous = self.risk_rate_safe + (self.time_safe - self.time_expected)/1000

        if (time_actual > self.time_safe):
            return self.risk_rate_safe
        else:
            return self.risk_rate_dangerous

    # Calc actual risk
    def Risk_actual(self, orders_actual):
        risk_rate_actual = self.Risk_rate_actual(orders_actual)
        return 1-np.power(1-risk_rate_actual, orders_actual)

    # Calc total income
    def Total_income(self, orders_actual, orders_expected):
        time_actual = self.Time_per_order(orders_actual)
        if orders_actual < orders_expected:
            return ((8-np.power(50, time_actual-self.time_expected))*orders_actual)/10
        else:
            return 8*np.tanh((orders_actual - orders_expected)/20)+32

    # Main function
    def main(self):
        orders_safe = self.Orders_safe(self.d)
        self.time_safe = self.Time_per_order(orders_safe)

        # orders_expected = self.Orders_expected(orders_safe)
        orders_expected = self.Orders_expected(self.d)
        self.time_expected = self.Time_per_order(orders_expected)

        if self.orders_is_expected:
            orders_actual = orders_expected
        else:
            orders_actual = self.Orders_actual()

        self.risk_actual_init = self.Risk_actual(self.orders_init)
        self.total_income_init = self.Total_income(self.orders_init, orders_expected)
        self.risk_actual = self.Risk_actual(orders_actual)
        self.total_income = self.Total_income(orders_actual, orders_expected)

    # For debug
    def test(self):
        orders_safe = self.Orders_safe(self.d)
        self.time_safe = self.Time_per_order(orders_safe)
        orders_expected = self.Orders_expected(self.d)
        self.time_expected = self.Time_per_order(orders_expected)        

        # plt.figure()
        order_list = np.arange(10,101,10)
        risk_list = []
        for order in order_list:
            risk_list.append(self.Risk_actual(order))
        # plt.plot(order_list, risk_list)
        print(dict(zip(order_list,risk_list)))
        plt.xlabel("Order num")
        plt.ylabel("Risk actual")
        # plt.legend(bbox_to_anchor=(1,1), fontsize=8)
        plt.tight_layout()
        # plt.show()

# income_risk=Income_Risk(orders_safe_min=2,orders_safe_max=29)
# income_risk.test()

# -*- coding: utf-8 -*-
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt


def Plot_orders_safe(user_num):
    plt.figure()

    xlist = np.arange(1, 51, 1)

    for user in np.arange(1, user_num + 1, 1):
        ylist = []
        os_min = np.floor(np.random.normal(8, 3))
        if os_min < 0:
            os_min = 0
        os_max = np.floor(np.random.normal(35, 3))
        if os_max < 0:
            os_max = 0
        income_risk = Income_Risk(orders_safe_min=os_min, orders_safe_max=os_max)
        for d in xlist:
            ylist.append(income_risk.Orders_safe(d))
        plt.plot(xlist, ylist, label=str(int(user))[:2])
    # Expected
    ylist = []
    os_min = 14
    os_max = 41
    income_risk = Income_Risk(orders_safe_min=os_min, orders_safe_max=os_max)
    for d in xlist:
        ylist.append(income_risk.Orders_safe(d))
    plt.plot(xlist, ylist, "k-.", linewidth=2, label="Expected")
    # O
    ylist = []
    os_min = 2
    os_max = 29
    income_risk = Income_Risk(orders_safe_min=os_min, orders_safe_max=os_max)
    for d in xlist:
        ylist.append(income_risk.Orders_safe(d))
    plt.plot(xlist, ylist, "r", linewidth=2, label="Orlando")

    plt.xlabel("Day")
    plt.ylabel("Safe Order Num")
    plt.legend(bbox_to_anchor=(1, 1), title="ID", fontsize=8)
    plt.tight_layout()
    plt.show()


def Plot_Risk_day():
    plt.figure()
    xlist = np.arange(0, 101, 1)

    for day in range(1, 25, 1):
        ylist = []
        for x in xlist:
            income_risk = Income_Risk(
                d=day, orders_safe_min=2, orders_safe_max=29, orders_adding=x
            )
            income_risk.main()
            ylist.append(income_risk.risk_actual)
        plt.plot(xlist, ylist, label=str(int(day)))
    # ylist=[]
    # for x in xlist:
    #     income_risk = Income_Risk(d=x,orders_safe_min=2, orders_safe_max=29,orders_is_expected=True)
    #     income_risk.main()
    #     ylist.append(income_risk.risk_actual)
    # plt.plot(xlist,ylist,'k-.',linewidth=2,label='Expected')
    plt.xlabel("Adding Order Num")
    plt.ylabel("Risk")
    plt.title("Effects of Order Num on Risk for Orlando")
    plt.legend(bbox_to_anchor=(1, 1), title="Day", fontsize=8)
    plt.tight_layout()
    plt.show()

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from re import S


import backtrader as bt
import backtrader.indicators as btind

class SmashDay(bt.Strategy):
    params = (
        # Slow MA Period
        ('ma_period', 50)
        # Pip size
        ('pip_size', 0.00001)
        # Stop Loss in Pips
        ('sl', 300)
        # Moving Average type to use
        ('_movav', btind.MovAv.EMA)
    )
    
    def log(self, txt, dt=None):
        """
        Logging function for this strategy to keep 
        track of prices in the dataset
        """
        if self.p.printout:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [bt.Order.Submitted, bt.Order.Accepted]:
            return  # Await further notifications

        if order.status == order.Completed:
            if order.isbuy():
                buytxt = 'BUY COMPLETE, %.2f' % order.executed.price
                self.log(buytxt, order.executed.dt)
            else:
                selltxt = 'SELL COMPLETE, %.2f' % order.executed.price
                self.log(selltxt, order.executed.dt)

        elif order.status in [order.Expired, order.Canceled, order.Margin]:
            self.log('%s ,' % order.Status[order.status])
            pass  # Simply log

        # Allow new orders
        self.orderid = None
    
    def __init__(self) -> None:
        self.ema_fast = self.p._movav(self.p.ma_period)
        self.ema_slow = self.p._movav(350)
        # self.close_data = self.datas[0].close
        # self.low_data = self.datas[0].low
        # self.high_data = self.datas[0].high
        

        # Keep track of pending orders and price/commission
        self.stop_loss_diff = self.p.pip_size*self.p.sl
        self.order_id = None
        self.buyprice = None
        self.buycomm = None
        self.sellprice = None
        self.sellcom = None

    def next(self):
        # Log the closing and low price of current series
        # self.log('Close, %.2f' % self.close_data[0])
        # self.log('Low, %.2f' % self.low_data[0])
        # self.log('High, %.2f' % self.high_data[0])

        if not self.order_id:

        ########## Entry Logic ##########
            # Buy Logic
            if self.data.close[-1] > self.ema_slow and self.data.close[-1] > self.ema_fast and\
                self.data.close[-1] > self.data.close[-20] and self.data.close[-1] < self.data.low[-2]:
                
                if self.data.close[0] > self.data.high[-1]:
                    main_order = self.buy(transmit=False)
                    stop_loss = self.sell(price=main_order.price - (self.p.pip_size*self.p.sl) , size=main_order.size, 
                        exectype=bt.Order.Stop, transmit=True, parent=main_order)
                
            # Sell Logic
            if self.data.close[-1] < self.ema_slow and self.data.close[-1] < self.ema_fast and\
                self.data.close[-1] < self.data.close[-20] and self.data.close[-1] > self.data.high[-2]:

                if self.data.close[0] < self.data.low[-1]:
                    main_order = self.sell(transmit=False)
                    stop_loss = self.buy(price=main_order.price + (self.p.pip_size*self.p.sl) , size=main_order.size, 
                        exectype=bt.Order.Stop, transmit=True, parent=main_order)
        ################################

        else:
        ########## Exit Logic ##########
            # Buy Logic
            if self.orderData.isbuy():
                if self.data.close[-1] < min(self.data.close.get(ago=0, size=20)):
                    pass

        ################################
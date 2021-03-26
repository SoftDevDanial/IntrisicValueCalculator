"""
    Programmer: Mohd Danial Saufi Bin Ezani
    Date: 7/15/2020
    Program Aim: Calculate Intrisic Value for US STOCK

"""
import finviz as fv
from yahooquery import Ticker
import pandas as pd


#### Power Declaration ####
Power = {
        'M': 6,
        'B': 9,
        'Million' : 6,
        'Billion' : 9
}

class IntrisicValScript():
    
    def __init__(self, ticks):
        self.ticks = ticks
    def text_to_num(self , text):
        if text[-1] in Power:
            num, magnitude = text[:-1], text[-1]
            return float(num) * 10 ** Power[magnitude]
        else:
            return float(text)

    def num_to_text(self,num):
        div = num/1000000
        if div >= 1 and div < 1000:
            return str(round(div)) + "M"
        elif div >= 1000:
            return str(round(div)/1000) + "B"
        else:
            return num

    def calcIntVal(self):
        outst_shrs_list = []
        Eps_1to5y_list = []
        discount_rate_list = []
        last_close_list = []
        intrisic_per_share_list = []
        for tick in self.ticks:
            
                #### Retrieve Stock ####
                stock_yq = Ticker(tick)
                stock_fv = fv.get_stock(tick)

                #### Cash Flow ####
                cash_fl = stock_yq.cash_flow(frequency="a")
                op_cash = cash_fl.tail(1).loc[:,"OperatingCashFlow"]

                #### Balance Sheet ####
                bal_sheet = stock_yq.balance_sheet(frequency = "q")
                
                if "TotalDebt" in bal_sheet:
                    total_debt = bal_sheet.tail(1).loc[:,"TotalDebt"]
                else:
                    total_debt = 0
                cash_short_term_investment = bal_sheet.tail(1).loc[:,"CashCashEquivalentsAndShortTermInvestments"]

                #### Growth Rate ####
                try:
                    Eps_1to5y = float(stock_fv["EPS next 5Y"].strip(' \t\n\r%'))
                except ValueError:
                    Eps_1to5y = 0

                if Eps_1to5y >= 15:
                    Eps_6to10y = 15
                else:
                    Eps_6to10y = Eps_1to5y

                #### Last Close ####
                last_close = stock_yq.price[tick]["regularMarketPrice"]

                #### Outstanding Shares ###
                outst_shrs = self.text_to_num(stock_fv["Shs Outstand"])

                #### Discount Rate ####
                try:
                    beta = float(stock_fv["Beta"])
                except ValueError:
                    beta = 0
                risk_free_rate = 0.64
                mrkt_risk_prem = 5
                discount_rate = round(risk_free_rate + beta * mrkt_risk_prem,1)


                #### Present Value of 10 year Cash Flows ####
                PV_10y_CF_li = [] 
                for x in range(10):
                    if x == 0:
                        Op_cash_flow_proj = op_cash * (1+(Eps_1to5y/100))  
                    elif x > 5:
                        Op_cash_flow_proj = op_cash * (1+(Eps_6to10y /100))
                    else:
                        Op_cash_flow_proj = Op_cash_flow_proj * (1+(Eps_1to5y/100))

                    if x == 0:
                        discount_factor = (1/(1+discount_rate/100))
                    else:
                        discount_factor = (discount_factor/(1+discount_rate/100))
                
                    Op_cash_flow_proj_discounted = Op_cash_flow_proj * discount_factor
                    PV_10y_CF_li.append(Op_cash_flow_proj_discounted)

                PV_10y_CF = sum(PV_10y_CF_li)

                #### Intrinsic Value before cash/debt ####
                if outst_shrs != 0:
                    intrisic_bfr_cash_dbt = round(PV_10y_CF/outst_shrs,2)
                else:
                    intrisic_bfr_cash_dbt = 0

                #### Less Debt per Share ####
                if outst_shrs != 0:
                    less_dbt_per_shr = round(total_debt/outst_shrs,2)
                else:
                    less_dbt_per_shr = 0

                #### Plus (+) Cash Per Share ####
                if outst_shrs != 0:
                    plus_cash_per_shr = round(cash_short_term_investment/outst_shrs,2)
                else:
                    plus_cash_per_shr = 0

                #### Final Intrinsic Value Per Share ####
                intrisic_per_share = intrisic_bfr_cash_dbt - less_dbt_per_shr + plus_cash_per_shr

                #### Discount/Premium ####
                #discount_premium = (last_close - intrisic_per_share)/intrisic_per_share

                outst_shrs_list.append(self.num_to_text(outst_shrs))
                Eps_1to5y_list.append(Eps_1to5y)
                discount_rate_list.append(discount_rate)
                last_close_list.append(last_close)
                intrisic_per_share_list.append(round(intrisic_per_share.get(tick),2))

        data = {'symbol' : self.ticks, 'outst_shrs': outst_shrs_list ,'Eps_1to5y': Eps_1to5y_list , 'discount_rate': discount_rate_list , 'last_close': last_close_list ,'intrisic_per_share' : intrisic_per_share_list}
        df = pd.DataFrame.from_dict(data)
        return df
    
#### Used for Debugging Back End code ####
def main():
    myList = ['AAPL' , 'MSFT' , 'ATVI' , 'AMZN' , 'TTWO' , 'RMBL' , 'VRNA' , 'SALM' , 'COHN' , 'AUTO' , 'VCNX' , 'SCYX']
    op = IntrisicValScript(myList).calcIntVal()
    print(op)


if __name__ == '__main__':
    main()

























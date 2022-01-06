from invest_parser import investingParser
from finviz_parser import finvizParser
from pdf_generator import gen_pdf
import pandas as pd
import sqlite3
from sqlite3 import Error

# Create SQL Connection 
def create_connection(database_file):
    connect_sql = None
    try:    
        connect_sql = sqlite3.connect(database_file)
    except Error as err:    
        print(err)
    finally:
        if connect_sql:
            connect_sql.close()

invest_pars = investingParser()
finviz_parser = finvizParser()

#Get pandas DataDrame with Ethereum data
invest_data = invest_pars.getDataInvesting('https://ru.investing.com/crypto/ethereum/eth-usd-historical-data')
invest_pars.driver_close()

#Save pandas df in SQL
create_connection('data/invest_sqlite')
connectSql = sqlite3.connect('data/invest_sqlite')
cursorSql = connectSql.cursor()
invest_data.to_sql('invest_sqlite', connectSql)
connectSql.close()

minus_count = 0
for i in invest_data['Change']:
    if '-' in i:
        minus_count = minus_count+1
    else:pass
del invest_data['Size']
del invest_data['Change']
fig = invest_data.plot()
fig.figure.savefig('fig/fig.png')

# Get Screenshot from Finviz
finviz_parser.getDataFinviz()
finviz_parser.driver_close()

# Some simple examples of work with analyzed data 
price_mean = invest_data['Price'].mean()
len_df = len(invest_data)-1
date_start = invest_data['Date'][0]
date_end = invest_data['Date'][len_df]
part_len = len_df/2
difference_num = len_df-minus_count
if difference_num > part_len:
    change_sub = 'negative'
else:
    change_sub = 'positive'

# Generatie report in pdf format
gen_pdf(price_mean, date_start, date_end, change_sub)




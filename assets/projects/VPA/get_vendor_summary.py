import sqlite3
import pandas as pd
import logging
from ingestion_db import ingest_db

logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

def create_vendor_summary(conn) :
    '''this function will merge the different tables to get the overall vendor summary and adding new columns in the resultant data'''
    vendor_sales_summary = pd.read_sql_query("""with FreightSummary as(
                                   select VendorNumber, SUM(Freight) as FreightCost
                                   from vendor_invoice
                                   Group By VendorNumber),

                                   PurchaseSummary as(
                                   select p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice,
                                   pp.Price as ActualPrice, pp.Volume, SUM(p.Quantity) as TotalPurchaseQuantity, SUM(p.Dollars) as TotalPurchaseDollars
                                   from purchases p join purchase_prices pp
                                   on p.Brand = pp.Brand
                                   where p.PurchasePrice > 0
                                   Group By p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume),

                                   SalesSummary as(
                                   select VendorNo, Brand, SalesPrice, SUM(SalesQuantity) as TotalSalesQuantity,
                                   SUM(SalesDollars) as TotalSalesDollars, SUM(ExciseTax) as TotalExciseTax
                                   from sales
                                   Group By VendorNo, Brand)
                                   
                                   select
                                   ps.VendorName,
                                   ps.VendorNumber,
                                   ps.Brand,
                                   ps.Description,
                                   ps.ActualPrice,
                                   ps.PurchasePrice,
                                   ps.Volume,
                                   ss.SalesPrice,
                                   ss.TotalSalesQuantity,
                                   ss.TotalSalesDollars,
                                   ss.TotalExciseTax,
                                   ps.TotalPurchaseQuantity,
                                   ps.TotalPurchaseDollars,
                                   fs.FreightCost
                                   from PurchaseSummary ps LEFT JOIN SalesSummary ss
                                   on ps.VendorNumber = ss.VendorNo and ps.Brand = ss.Brand
                                   LEFT JOIN FreightSummary fs
                                   on ps.VendorNumber = fs.VendorNumber
                                   Order By ps.TotalPurchaseDollars DESC""", conn)
    return vendor_sales_summary

def clean_data(df):
    '''this function will clean the data'''
    # changing datatype to float
    df['Volume'] = df['Volume'].astype('float64')

    # filling missing value with 0
    df.fillna(0, inplace = True)

    # removing spaces form categorical columns
    df['VendorName'] = df['VendorName'].str.strip()

    # creating new columns for better analysis
    vendor_sales_summary['GrossProfit'] = vendor_sales_summary['TotalSalesDollars'] - vendor_sales_summary['TotalPurchaseDollars']
    vendor_sales_summary['ProfitMargin'] = (vendor_sales_summary['GrossProfit'] / vendor_sales_summary['TotalSalesDollars'])*100
    vendor_sales_summary['StockTurnover'] = vendor_sales_summary['TotalSalesQuantity'] /vendor_sales_summary['TotalPurchaseQuantity']
    vendor_sales_summary['SalesPurchaseRatio'] = vendor_sales_summary['TotalSalesDollars'] / vendor_sales_summary['TotalPurchaseDollars']

    return df

if __name__ == '__main__':
    # creating database connection
    conn = sqlite3.connect('inventory.db')

    logging.info('Creating Vendor Summary Table...')
    summary_df = create_vendor_summary(conn)
    logging.info(summary_df.head())

    logging.info('Cleaning Data...')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info('Ingestion data...')
    ingest_db(clean_df, 'vendor_sales_summary', conn)
    logging.info('Completed')
import pandas as pd 
import numpy as np 


def extract_features(features, data):
	# 新增'CompetitionOpen'和'PromoOpen'特征,计算某天某店铺的竞争对手已营业时间和店铺已促销时间，用月为单位表示
	features.extend(['CompetitionOpen', 'PromoOpen'])
	data['CompetitionOpen'] = 12 * (data.Year - data.CompetitionOpenSinceYear) + (data.Month - data.CompetitionOpenSinceMonth)
	data['PromoOpen'] = 12 * (data.Year - data.Promo2SinceYear) + (data.WeekOfYear - data.Promo2SinceWeek) / 4.0
	data['CompetitionOpen'] = data.CompetitionOpen.apply(lambda x: x if x > 0 else 0)
	data['PromoOpen'] = data.PromoOpen.apply(lambda x: x if x > 0 else 0)

	# 将'PromoInterval'特征转化为'IsPromoMonth'特征,表示某天某店铺是否处于促销月，1表示是，0表示否
	features.append('IsPromoMonth')
	month2str = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sept', 10: 'Oct',
				 11: 'Nov', 12: 'Dec'}
	data['monthStr'] = data.Month.map(month2str)
	data.loc[data.PromoInterval == 0, 'PromoInterval'] = ''
	data['IsPromoMonth'] = 0
	for interval in data.PromoInterval.unique():
		if interval != '':
			for month in interval.split(','):
				data.loc[(data.monthStr == month) & (data.PromoInterval == interval), 'IsPromoMonth'] = 1

	# calculate average sales per store, customers per store, customer median and sales per customers
	features.extend(['AvgSales', 'AvgCustomers', 'AvgSalesPerCustomer', 'MedianCustomers'])

	train_df = data[data['DataSetFlag'] == 1]

	TotalSalesPerStore = train_df.groupby([train_df['Store']])['Sales'].sum()
	TotalCustomersPerStore = train_df.groupby([train_df['Store']])['Customers'].sum()
	TotalOpenStores = train_df.groupby([train_df['Store']])['Open'].count()
	MedianCustomers = train_df.groupby([train_df['Store']])['Customers'].median()

	#2 compute averages
	AvgSales = TotalSalesPerStore / TotalOpenStores
	AvgCustomers = TotalCustomersPerStore / TotalOpenStores
	AvgSalesPerCustomer = AvgSales / AvgCustomers

	#3 merge the averages into data
	data = pd.merge(data, AvgSales.reset_index(name='AvgSales'), how='left', on=['Store'])
	data = pd.merge(data, AvgCustomers.reset_index(name='AvgCustomers'), how='left', on=['Store'])
	data = pd.merge(data, AvgSalesPerCustomer.reset_index(name='AvgSalesPerCustomer'), how='left', on=['Store'])
	data = pd.merge(data, MedianCustomers.reset_index(name='MedianCustomers'), how='left', on=['Store'])

	# calculate number of schoolholidays this week, last week and next week
	features.extend(['HolidaysThisWeek', 'HolidaysLastWeek', 'HolidaysNextWeek'])

	HolidaysCount = data.groupby(['Store','Year','WeekOfYear'])['SchoolHoliday'].sum().reset_index(name='HolidaysThisWeek')
	HolidaysCount['HolidaysLastWeek'] = 0
	HolidaysCount['HolidaysNextWeek'] = 0

	for store_id in HolidaysCount.Store.unique().tolist():
		store_lgt = len(HolidaysCount[HolidaysCount['Store'] == store_id])
		HolidaysCount.loc[1:store_lgt-1, 'HolidaysLastWeek'] = HolidaysCount.loc[0:store_lgt-2, 'HolidaysThisWeek'].values
		HolidaysCount.loc[0:store_lgt-2, 'HolidaysNextWeek'] = HolidaysCount.loc[1:store_lgt-1, 'HolidaysThisWeek'].values

	data = pd.merge(data, HolidaysCount, how='left', on=['Store', 'Year', 'WeekOfYear'])

	# calculate average and median sales and customers per store per day of week
	features.extend(['AvgSalesPerDow', 'medianSalesPerDow', 'AvgCustomersPerDow', 'MedianCustomersPerDow'])

	AvgSalesPerDow = train_df.groupby(['Store', 'DayOfWeek'])['Sales'].mean()
	medianSalesPerDow = train_df.groupby(['Store', 'DayOfWeek'])['Sales'].median()
	AvgCustomersPerDow = train_df.groupby(['Store', 'DayOfWeek'])['Customers'].mean()
	MedianCustomersPerDow = train_df.groupby(['Store', 'DayOfWeek'])['Customers'].median()

	# merge
	data = pd.merge(data, AvgSalesPerDow.reset_index(name='AvgSalesPerDow'), how='left', on=['Store', 'DayOfWeek'])
	data = pd.merge(data, AvgCustomersPerDow.reset_index(name='AvgCustomersPerDow'), how='left', on=['Store', 'DayOfWeek'])
	data = pd.merge(data, medianSalesPerDow.reset_index(name='medianSalesPerDow'), how='left', on=['Store', 'DayOfWeek'])
	data = pd.merge(data, MedianCustomersPerDow.reset_index(name='MedianCustomersPerDow'), how='left', on=['Store', 'DayOfWeek'])

	data.fillna(0, inplace=True)

	features.extend(['Store','CompetitionDistance','Promo','Promo2', 'StoreType','Assortment','StateHoliday', 'SchoolHoliday', 'Year','Month','WeekOfYear','DayOfWeek','DayOfMonth', 'DayOfYear'])

	return data


	







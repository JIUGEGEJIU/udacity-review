import pandas as pd 
import numpy as np 

def data_preprocess(train, test, store):

	# 将两个表统一处理所以加入一个标识位
	train['DataSetFlag'] = 1
	test['DataSetFlag'] = 0
	train_test = pd.concat([train, test])

	# 去掉所有训练数据中销售额为0的项
	# train_test = train_test.loc[~((train_test['DataSetFlag'] == 1) & (train_test['Open'] == 0))]
	# train_test = train_test.loc[~((train_test['DataSetFlag'] == 1) & (train_test['Sales'] == 0))]
	train_test = train_test.loc[~((train_test['DataSetFlag'] == 1) & (train_test['Open'] == 0))]
	train_test = train_test.loc[~((train_test['DataSetFlag'] == 1) & (train_test['Sales'] == 0))]
	# 开业但是没有一个顾客的情况，可能是数据录入错误。有极少顾客但是销售额为零的情况也去掉，可能正处于开业当天
	# 所以我们排除了所有开业且销售额为0的项
	# 为了减小特殊数据点导致得过拟合，排除掉销售额大于35000或者顾客数大于5000的情况
	# train_test = train_test.loc[(train_test['DataSetFlag'] == 0) & (train_test['Sales'] > 0) & (train_test['Sales'] <= 35000) & (train_test['Customers'] <= 5000)]
	# train_test = train_test.loc[~((train_test['DataSetFlag'] == 1) & (train_test['Sales'] > 35000))]
	# train_test = train_test.loc[~((train_test['DataSetFlag'] == 1) & (train_test['Customers'] > 5000))]


	# 将所有StateHoliday 0整型值转换为'0'
	train_test.loc[train_test['StateHoliday'] == 0, 'StateHoliday'] = '0'

	# 日期处理
	train_test["Year"] = train_test["Date"].dt.year
	train_test["Month"] = train_test["Date"].dt.month
	train_test["DayOfMonth"] = train_test["Date"].dt.day
	train_test["WeekOfYear"] = train_test["Date"].dt.weekofyear
	train_test["DayOfYear"] = train_test["Date"].dt.dayofyear

	# 将所有测试数据集Open缺失值设为1
	train_test.loc[train_test['Open'].isnull(), 'Open'] = 1

	# 编码
	train_test['StateHoliday'] = train_test['StateHoliday'].astype('category').cat.codes
	train_test['DayOfWeek'] = train_test['DayOfWeek'].astype('category').cat.codes


	#store["CompetitionDistance"].fillna(0, inplace=True)
	# 所有store数据的空值填充0
	store["CompetitionDistance"].fillna(0, inplace=True)
	# 所有store数据的"CompetitionSince..."填充为1900/01
	# store["CompetitionOpenSinceYear"][(store["CompetitionDistance"] != 0) & (store["CompetitionOpenSinceYear"].isnull())] = 1900
	# store["CompetitionOpenSinceMonth"][(store["CompetitionDistance"] != 0) & (store["CompetitionOpenSinceMonth"].isnull())] = 1

	# 编码
	store['Assortment'] = store['Assortment'].astype('category').cat.codes
	store['StoreType'] = store['StoreType'].astype('category').cat.codes

	# 三个数据集进行合并
	merged_df = pd.merge(train_test, store, how='left', on='Store')

	# 所有其他缺失值填充为0
	merged_df.fillna(0, inplace=True)

	return merged_df



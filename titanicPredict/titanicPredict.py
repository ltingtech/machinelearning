# -*-coding:utf-8 -*-

import re
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing

warnings.filterwarnings('ignore')
#%matplotlib inline

def viewData():
	train_data, test_data = loadData()
	sns.set_style('whitegrid')
	print train_data.head()  #输出数据的前5行(pandas默认5行)，类似的用法有tail()函数
	
	train_data.info()
	print("-" * 40)
	test_data.info()
	'''
	train_data['Survived'].value_counts().plot.pie(autopct = '%1.2f%%')	
	plt.savefig('result/survived_ratio.png')
	plt.close()
	'''
	#对Embarked属性进行缺失值处理，isnull()返回一个true/false的布尔型数组
	# dropna()会把值等于null的数据去掉，mode()会返回出现最多的数据，注意返回的是一个数组
	train_data.Embarked[train_data.Embarked.isnull()] = train_data.Embarked.dropna().mode().values
	#对于船舱号，直接定义一个表示缺失的值，因为可能缺失值本身就代表了一个意思
	train_data['Cabin'] = train_data.Cabin.fillna('U0')  # train_data.Cabin[train_data.Cabin.isnull()] = 'U0'

#加载数据
def loadData():
	train_data = pd.read_csv('data/train.csv')
	test_data = pd.read_csv('data/test.csv')
	return train_data, test_data

def predictAgeAttr(train_data):
	age_df = train_data[['Age', 'Survived', 'Fare', 'Parch', 'SibSp', 'Pclass']]
	age_df_notnull = age_df.loc[(train_data['Age'].notnull())]
	age_df_isnull = age_df.loc[(train_data['Age'].isnull())]  #结果类型 <class 'pandas.core.frame.DataFrame'>
	'''
	print age_df_notnull
	print ('-' * 40)
	print age_df_isnull
	'''
	X = age_df_notnull.values[:, 1:]
	Y = age_df_notnull.values[:, 0]
	RFR = RandomForestRegressor(n_estimators=1000, n_jobs=-1)
	RFR.fit(X, Y)
	predictAges = RFR.predict(age_df_isnull.values[:, 1:])
	'''
	print ('-' * 40)
	print 'predict age result'
	print predictAges
	'''
	# train_data.loc[train_data['Age'].isnull(), ['Age']] 提取出满足条件的行的对应的列
	train_data.loc[train_data['Age'].isnull(), ['Age']] = predictAges

def filterNullData(train_data):
	train_data.Embarked[train_data.Embarked.isnull()] = train_data.Embarked.dropna().mode().values
	train_data['Cabin'] = train_data.Cabin.fillna('U0')
	predictAgeAttr(train_data)

def attrAnalysis(train_data):
	'''
	#观察sex跟survived的关系
	print train_data.groupby(['Sex', 'Survived'])['Survived'].count()
	train_data[['Sex', 'Survived']].groupby(['Sex']).mean().plot.bar()
	plt.savefig('sex_survived.png')
	plt.close()
	
	# 观察pclass跟survived的关系
	print train_data.groupby(['Pclass', 'Survived'])['Pclass'].count()
	train_data[['Pclass', 'Survived']].groupby(['Pclass']).mean().plot.bar()
	plt.savefig('result/Pclass_survived.png')
	plt.close()	
	train_data[['Sex', 'Pclass', 'Survived']].groupby(['Sex', 'Pclass']).mean().plot.bar()
	plt.savefig('result/sex_pclass_survived.png')
	plt.close()
	print train_data.groupby(['Sex', 'Pclass', 'Survived'])['Survived'].count()
	# 分析年龄的关心
	fig, ax = plt.subplots(1, 2, figsize=(18, 8))
	sns.violinplot("Pclass", "Age", hue="Survived", data=train_data, split=True, ax=ax[0])   #设置split=True表示根据hue拆分两个量，然后画小提琴图
	ax[0].set_title('Pclass and Age vs Survived');
	ax[0].set_yticks(range(0, 110, 10))
	
	sns.violinplot("Sex", "Age", hue="Survived", data=train_data, split=True, ax=ax[1])
	ax[1].set_title('Sex and Age vs Survived')
	ax[1].set_yticks(range(0, 110, 10))
	plt.savefig('result/age_survived.png')
	plt.close()
	#观察age的在整体数据集中的分布
	plt.figure(figsize=(12, 5))
	plt.subplot(121)
	train_data['Age'].hist(bins=70)
	plt.xlabel('Age')
	plt.ylabel('Num')
	
	plt.subplot(122)
	train_data.boxplot(column='Age', showfliers=False)
	plt.savefig('result/age_distribution_total.png')
	plt.close()
	
	facet = sns.FacetGrid(train_data, hue='Survived', aspect=4)
	facet.map(sns.kdeplot, 'Age', shade=True)
	facet.set(xlim=(0, train_data['Age'].max()))
	facet.add_legend()
	plt.savefig('result/age_survived_total.png')
	plt.close()
	
	fig, axis1 = plt.subplots(1, 1, figsize=(18, 4))
	train_data["Age_int"] = train_data["Age"].astype(int)
	average_age = train_data[['Age_int', 'Survived']].groupby(['Age_int'], as_index=False).mean()
	sns.barplot(x='Age_int', y='Survived', data=average_age) 
	plt.savefig('result/age_survived_average.png')
	plt.close()
	
	# 按年龄段分析
	bins = [0, 12, 18, 65, 100]
	train_data['Age_group'] = pd.cut(train_data['Age'], bins)
	by_age = train_data.groupby(['Age_group'])['Survived'].mean()   #也可写成train_data.groupby(['Age_group'])['Survived']
	by_age.plot(kind='bar')
	plt.savefig('result/age_group_survived.png')
	plt.close()	
	
	train_data['Title'] = train_data['Name'].str.extract('([A-Za-z]+\.)', expand=False)
	pd.crosstab(train_data['Title'], train_data['Sex'])
	train_data[['Title', 'Survived']].groupby(['Title']).mean().plot.bar()
	plt.savefig('result/title_group_survived.png')
	plt.close()
	'''	
	'''
	fig, axis1 = plt.subplots(1, 1, figsize=(18, 4))
	train_data['Name_length'] = train_data['Name'].apply(len)
	name_length = train_data[['Name_length', 'Survived']].groupby(['Name_length'], as_index=False).mean()
	sns.barplot(x='Name_length', y='Survived', data=name_length)
	plt.savefig('result/name_length_survived.png')
	plt.close()
	'''
	'''
	#观察有无兄弟姐妹对生存的影响
	sibsp_df = train_data[train_data['SibSp'] != 0]
	no_sibsp_df = train_data[train_data['SibSp'] == 0]
	plt.figure(figsize=(10, 5))
	plt.subplot(121)
 	sibsp_df['Survived'].value_counts().plot.pie(labels=['No Survived', 'Survived'], autopct = '%1.1f%%')
	plt.xlabel('sibsp')
	
	plt.subplot(122)
	no_sibsp_df['Survived'].value_counts().plot.pie(labels=['No Survived', 'Survived'], autopct = '%1.1f%%')
	plt.xlabel('no_sibsp')
	plt.savefig('result/sibsp_survived_pie.png')
	plt.close()	
	'''
	'''
	#有无父母子女对存活的影响
	parch_df = train_data[train_data['Parch'] != 0]
	no_parch_df = train_data[train_data['Parch'] == 0]
	plt.figure(figsize=(10, 5))
	plt.subplot(121)
	parch_df['Survived'].value_counts().plot.pie(labels=['No Survived', 'Survived'], autopct='%1.1f%%')
	plt.xlabel('parch')
	plt.subplot(122)
	no_parch_df['Survived'].value_counts().plot.pie(labels=['No Survived', 'Survived'], autopct='%1.1f%%')
	plt.xlabel('no parch')
	plt.savefig('result/parch_survived_pie.png')
	plt.close()	
	'''
	'''
	# 父母亲友数量对生存的影响
	fig, ax = plt.subplots(1, 2, figsize=(18, 8))
	train_data[['SibSp', 'Survived']].groupby(['SibSp']).mean().plot.bar(ax=ax[0])
	ax[0].set_title('SibSp and Survived')
	train_data[['Parch', 'Survived']].groupby(['Parch']).mean().plot.bar(ax=ax[1])
	ax[1].set_title('Parch and Survived')
	plt.savefig('result/sibps_parch_num_survived.png')
	plt.close()
	'''
	'''
	train_data['Family_Size'] = train_data['SibSp'] + train_data['Parch'] + 1
	train_data[['Family_Size', 'Survived']].groupby(['Family_Size']).mean().plot.bar()
	plt.savefig('result/family_size_survived.png')
	plt.close()
	'''
	'''
	plt.figure(figsize=(10, 5))
	train_data['Fare'].hist(bins = 70)
	plt.savefig('result/fare_hist.png')
	plt.close()
	'''
	'''
	train_data.boxplot(column = 'Fare', by = 'Pclass', showfliers=False)
	plt.savefig('result/fare_pclass.png')
	plt.close()
	'''
	'''
	train_data.loc[train_data.Cabin.isnull(), 'Cabin'] = 'U0'
	train_data['HasCabin'] = train_data['Cabin'].apply(lambda x: 0 if x=='U0' else 1)
	train_data[['HasCabin', 'Survived']].groupby(['HasCabin']).mean().plot.bar()
	plt.savefig('result/cabin_survived.png')
	plt.close()
	'''

	train_data['CabinLetter'] = train_data['Cabin'].map(lambda x : re.compile('([a-zA-Z]+)').search(x).group())
	#print train_data['CabinLetter']
	train_data['CabinLetter'] = pd.factorize(train_data['CabinLetter'])[0]
	#print train_data['CabinLetter']
	'''
	train_data[['CabinLetter', 'Survived']].groupby(['CabinLetter']).mean().plot.bar()
	plt.savefig('result/cabin_letter_survived.png')
	plt.close()
	'''

def convertAttr(train_data):
	embark_dummies = pd.get_dummies(train_data['Embarked'])
	train_data = train_data.join(embark_dummies)
	train_data.drop(['Embarked'], axis=1, inplace=True) # 删除列
	#embark_dummies = train_data[['S', 'C', 'Q']]
	#print	embark_dummies.head()
	print train_data[['Cabin']].head()
	
	#对年龄进行变量缩放
	assert np.size(train_data['Age']) == 891
	scaler = preprocessing.StandardScaler()
	train_data['Age_scaled'] = scaler.fit_transform(train_data['Age'].values.reshape(-1, 1))
	print train_data['Age_scaled'].head()

	#对船票进行分箱离散化操作
	train_data['Fare_bin'] = pd.qcut(train_data['Fare'], 5)
	#print train_data['Fare_bin'].head()
	#离散化后利用factorize或dummies化
	train_data['Fare_bin_id'] = pd.factorize(train_data['Fare_bin'])[0]
	print train_data['Fare_bin_id'].head()
	fare_bin_dummies_df = pd.get_dummies(train_data['Fare_bin']).rename(columns=lambda x: 'Fare_' + str(x))
	train_data = pd.concat([train_data, fare_bin_dummies_df], axis=1)
	print fare_bin_dummies_df.head()

	print train_data.head()

	return train_data


#特征工程
def featureEngining(train_data, test_data):
	train_df_org = train_data
	test_df_org = test_data
	test_df_org['Survived'] = 0
	print test_df_org['Survived'].head()
	combined_train_test = train_df_org.append(test_df_org)
	PassengerId = test_df_org['PassengerId']
	#print combined_train_test['Embarked'].mode()  # 获取众数
	combined_train_test['Embarked'].fillna(combined_train_test['Embarked'].mode().iloc[0], inplace=True)	
	# factorize 离散化
	#combined_train_test['Embarked'] = pd.factorize(combined_train_test['Embarked'])[0]	
	#print combined_train_test['Embarked'].head()
	emb_dummies_df = pd.get_dummies(combined_train_test['Embarked'], prefix=combined_train_test[['Embarked']].columns[0]) # 指定新增列名的前缀	
	combined_train_test = pd.concat([combined_train_test, emb_dummies_df], axis=1)
	#print combined_train_test.head(i)
	# 对sex特征进行处理
	#combined_train_test['Sex'] = pd.factorize(combined_train_test['Sex'])[0]
	sex_dummies_df = pd.get_dummies(combined_train_test['Sex'], prefix=combined_train_test[['Sex']].columns[0])	
	combined_train_test = pd.concat([combined_train_test, sex_dummies_df], axis=1)
	#print combined_train_test.head()
	#print combined_train_test['Name']
	
	#对称呼进行处理
	combined_train_test['Title'] = combined_train_test['Name'].map(lambda x : re.compile(", (.*?)\.").findall(x)[0])	
	#print combined_train_test['Title']
	title_dict = {}
	title_dict.update(dict.fromkeys(['Capt', 'Col', 'Major', 'Dr', 'Rev'], 'Officer'))
	title_dict.update(dict.fromkeys(['Don', 'Sir', 'the Countess', 'Dona', 'Lady'], 'Royalty'))
	title_dict.update(dict.fromkeys(['Mme', 'Ms', 'Mrs'], 'Mrs'))
	title_dict.update(dict.fromkeys(['Mlle', 'Miss'], 'Miss'))
	title_dict.update(dict.fromkeys(['Mr'], 'Mr'))
	title_dict.update(dict.fromkeys(['Master','Jonkheer'], 'Master'))
	combined_train_test['Title'] = combined_train_test['Title'].map(title_dict)
	#print combined_train_test['Title']
	#combined_train_test['Title'] = pd.factorize(combined_train_test['Title'])[0]
	#print combined_train_test['Title']
	title_dummies_df = pd.get_dummies(combined_train_test['Title'], prefix=combined_train_test[['Title']].columns[0])
	combined_train_test = pd.concat([combined_train_test, title_dummies_df], axis=1)
	#print combined_train_test.head()

	#把名字长度作为一个特征
	combined_train_test['Name_length'] = combined_train_test['Name'].apply(len)
	print combined_train_test.head()


#viewData()
train_data, test_data = loadData()
#predictAgeAttr(train_data)
#filterNullData(train_data)
#attrAnalysis(train_data)
#train_data = convertAttr(train_data)
#print train_data['Age'].describe()
featureEngining(train_data, test_data)


















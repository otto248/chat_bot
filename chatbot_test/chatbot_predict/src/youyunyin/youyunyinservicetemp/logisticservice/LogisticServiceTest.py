import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import warnings
import time
import sklearn
from sklearn.linear_model import  LogisticRegressionCV,LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model.coordinate_descent import ConvergenceWarning


## 设置属性防止中文乱码
mpl.rcParams['font.sans-serif'] = [u'SimHei']
mpl.rcParams['axes.unicode_minus'] = False

## 拦截异常
warnings.filterwarnings(action = 'ignore', category=ConvergenceWarning)

class LogisticServiceTest:
    def __init__(self,path,ssname,lrname):
        self.path=path
        self.path = 'C:\\Users\\wushzh\\Desktop\\rule\\text2.csv'
        self.ssname=ssname
        self.lrname=lrname

    def train(self):
        names = ['id', 'Clump Thickness', 'Uniformity of Cell Size', 'Uniformity of Cell Shape',
                 'Marginal Adhesion', 'Single Epithelial Cell Size', 'Bare Nuclei',
                 'Bland Chromatin', 'Normal Nucleoli', 'Mitoses', 'Class']
        names = ['bstotal', 'operatype', 'nettotal', 'txtotal', 'Class']
        path=self.path

        df = pd.read_csv(path, header=None, names=names)
        df = pd.read_csv(path, header=None, names=names)

        datas = df.replace('?', np.nan).dropna(how='any')  # 只要有列为空，就进行删除操作
        datas.head(5)  ## 显示一下

        # 1. 数据提取以及数据分隔
        ## 提取
        X = datas[names[0:4]]
        Y = datas[names[4]]

        ## 分隔
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)

        # 2. 数据格式化(归一化)
        ss = StandardScaler()
        X_train = ss.fit_transform(X_train)  ## 训练模型及归一化数据

        # 3. 模型构建及训练
        ## penalty: 过拟合解决参数,l1或者l2

        ## solver: 参数优化方式
        ### 当penalty为l1的时候，参数只能是：liblinear(坐标轴下降法)；
        ### 当penalty为l2的时候，参数可以是：lbfgs(拟牛顿法)、newton-cg(牛顿法变种)

        ## multi_class: 分类方式参数；参数可选: ovr(默认)、multinomial；这两种方式在二元分类问题中，效果是一样的；在多元分类问题中，效果不一样
        ### ovr: one-vs-rest， 对于多元分类的问题，先将其看做二元分类，分类完成后，再迭代对其中一类继续进行二元分类
        ### multinomial: many-vs-many（MVM）,对于多元分类问题，如果模型有T类，我们每次在所有的T类样本里面选择两类样本出来，
        #### 不妨记为T1类和T2类，把所有的输出为T1和T2的样本放在一起，把T1作为正例，T2作为负例，
        #### 进行二元逻辑回归，得到模型参数。我们一共需要T(T-1)/2次分类

        ## class_weight: 特征权重参数
        lr = LogisticRegressionCV(fit_intercept=True, Cs=np.logspace(-2, 2, 20), cv=2, penalty='l2', solver='lbfgs',
                                  tol=0.01)
        lr.fit(X_train, Y_train)

        # 4. 模型效果获取
        r = lr.score(X_train, Y_train)
        print("R值（准确率）：", r)
        print("稀疏化特征比率：%.2f%%" % (np.mean(lr.coef_.ravel() == 0) * 100))
        print("参数：", lr.coef_)
        print("截距：", lr.intercept_)

        # 5. 模型相关信息保存
        ## 引入包
        from sklearn.externals import joblib
        ## 要求文件夹必须存在
        joblib.dump(ss, self.ssname)  ## 将标准化模型保存
        joblib.dump(lr, self.lrname)  ## 将模型保存

        return self.lrname

        # # 模型加载
        # ## 引入包
        # from sklearn.externals import joblib
        # # ssname="ss.model"
        # oss = joblib.load(self.ssname)
        # # lrname="lr.model"
        # olr = joblib.load(self.lrname)
        #
        # # 数据预测
        # ## a. 预测数据格式化(归一化)
        # X_test = oss.transform(X_test)  # 使用模型进行归一化操作
        # ## b. 结果数据预测
        # Y_predict = olr.predict(X_test)


    def notEmpty(s):
        return s != ''

    def processor(self):
        result = dict()
        try:
            name = self.train()
            result['state'] = "True"
            result['message'] = "模型保存完成，模型名称;"+name+"完成时间"+ time.localtime(time.time())
        except Exception as e:
            message = str(e)
            result['state'] = "False"
            result['message'] = message

        return result

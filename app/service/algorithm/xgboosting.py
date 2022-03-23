import os
import numpy as np
from xgboost import XGBRegressor
import pickle
from app.service.algorithm import *

def xgb_train(filepath_input, filepath_output, learning_rate=0.05, max_depth=5, n_estimators=500):
    # 建立一个默认的xgboost回归模型
    reg = XGBRegressor(learning_rate=learning_rate, max_depth=max_depth, n_estimators=n_estimators)
    # 　eta默认值为0.1，而且更小的步长更利于现在的数据，但由于无 法确定对于其他数据会有怎么样的效果，所以通常对eta不做调整 ，即便调整，一般只会在[0.01,0.2]之间变动。
    #           迭代决策树时的步长，又叫学习率。eta越大，迭代的速度越快，算法的极限很快被达到，有可能无法收敛到真正的最佳。 越小，越有可能找到更精确的最佳值，更多的空间被留给了后面建立的树，但迭代速度会比较缓慢。
    # max_depth [默认 6]: 和 GBM 中的参数相同，这个值为树的最大深度。这个值也是用来避免过拟合的。max_depth 越大，模型会学到更具体更局部的样本。需要使用 CV 函数来进行调优。 典型值：3-10
    # n_estimators是集成中弱估计器的数量，即树的个数。使用参数学习曲线观察n_estimators对模型的影响。
    # 获取训练数据
    train_X, train_y, fn = read_data(filepath=filepath_input)
    # 训练拟合模型
    reg.fit(pd.DataFrame(np.array(train_X.values)), train_y)
    # 保存模型到fn中
    model_name = fn_auto_generate(kpi_name=fn, time_type="%Y%m%d", file_type="dat")
    if not os.path.exists(filepath_output):
        os.makedirs(filepath_output)
    output_model_name = os.path.join(filepath_output, model_name)
    pickle.dump(reg, open(output_model_name, "wb"))
    print("save model successful!")


# if __name__ == '__main__':
#     fp_input = "D:/Users/EB/AppData/Local/PycharmProjects/smeAIOps_0812/data/caps_SCPAS10_20191001-07.csv"
#     # train_X, train_y, fn = predata(filepath=fp_input)
#     # x = pd.DataFrame(np.array())
#     model_op = "D:/Users/EB/AppData/Local/PycharmProjects/smeAIOps_0812/model_base/caps_SCA"
#     xgb_train(filepath_input=fp_input, filepath_output=model_op)
#     # print(x.shape)
#     # print(x.head())
#     # print(train_y.shape)
#     # print(fn)


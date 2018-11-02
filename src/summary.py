### 智能面试（性格）###

import os, sys, re, math
import pandas as pd
from pandas import DataFrame
import seaborn as sns
print("最新数据文件名:",os.listdir("./智能面试"))

df_general = pd.read_excel("./智能面试/27837517_2_Java开发答案素材收集（通用部分）_176_176.xls")
index = df_general["用户名"]
general_cols = []
general_cols_simple = []
count = 0
for question in df_general.columns:
#     print(question)
    if question[-1] == "？" or question[-2] == "？":
        count += 1
        general_cols.append(question)
        general_cols_simple.append("q" + str(count))
df_general = df_general.loc[:, general_cols]
df_general.columns = general_cols_simple
df_general.index = index

def what_is_the_general_question(q):
    return general_cols[general_cols_simple.index(q)]

df_general.head()

df_question = pd.read_excel("./智能面试/27837517_2_Java开发答案素材收集（通用部分）_176_176.xls")
index = df_question["用户名"]
question_cols = []
question_cols_simple = []
count = 0
for question in df_question.columns:
    if question[0] == "【":
        count += 1
        question_cols.append(question)
        question_cols_simple.append("q" + str(count))
df_question = df_question.loc[:, question_cols]
df_question.columns = question_cols_simple
df_question.index = index
df_question.head()

def what_is_the_question(q):
    return question_cols[question_cols_simple.index(q)]

df_score = pd.read_excel("./智能面试/团队长打分名单  - fix.xlsx")
df_score = df_score.iloc[0:187,:]
index = df_score["被评分人"]
df_score.index = index
df_score = df_score.iloc[:,1:]
df_score["评分人"] = df_score["评分人"].fillna(method="ffill")
df_score = df_score.dropna()
def text_to_score(text):
    return int(re.findall("[(\d+)]", text)[0])

ability_cols = df_score.columns[2:]
for ability in ability_cols:
    df_score[ability] = df_score[ability].apply(lambda x:text_to_score(x))
del df_score["被评分人"]

df = pd.concat([df_question, df_score], axis=1)
df = df.dropna()
for ability in ['学习能力', "创造力", "执行力", "责任心", "团队合作", "不敏感性（是否能很好地应对批评）"]:
    boss_mean = df[ability].groupby(df["评分人"]).mean()
    for name in df.index:
        df[ability][name] = 1 if df[ability][name] > boss_mean[df["评分人"][name]] else 0
df.head()

def plot(feature, ability):
#     print(feature, ability)
    feature_mean = df[ability].groupby(df[feature]).mean()
    feature_count = df[ability].groupby(df[feature]).count()
    feature_df = DataFrame(index=feature_mean.index)
    feature_df["mean"] = feature_mean
    feature_df["count"] = feature_count
    try:
        feature_df.index = feature_df.index.astype(int)
    except:
        pass
    print(feature_df.sort_index())
    sns.factorplot(data=df, x=feature, y=ability, kind="bar")

question = "q6"
ability = "创造力"
print(what_is_the_question(question))
# for ability in ['学习能力', "创造力", "执行力", "责任心", "团队合作", "不敏感性（是否能很好地应对批评）"]:
#     plot(question, ability)
plot(question, ability)

def match_general_question(q, re_list):
    print("问题:", what_is_the_general_question(q))
    sr = df_general[q]
    sr_match = sr.copy()
    sr_match[:] = False
    for pattern in re_list:
        is_match = sr.apply(lambda x: len(re.findall(pattern, x))>0)
        sr_match += is_match
    print("匹配率：", str(round(len(sr_match[sr_match])/len(sr_match) * 100, ndigits=2)) + "%")
    print(sr[sr_match == False])

re_list = ["平安", "互.*金|金.*互", "大平台", "大|龙头|顶尖", "发展", "平台", "独角兽", "金融", "推荐|介绍","发展|成长|价值|锻炼", "前景","行业", "知名|名气", "挑战", "稳定", "转岗", "近", "喜欢"]
match_general_question("q1", re_list)

re_list = ["[0-9一两三]个?多?半?(小时)(.+分钟)?|\d+分钟", "浦东", "黄浦", "静安", "徐汇", "杨浦", "虹口", "闵行", "普陀", "闸北", "青浦", "宝山", "松江", "嘉定", "长宁"]
match_general_question("q4", re_list)






### 智能面试（非技术部分）###

import os, sys, re, math
import pandas as pd
from pandas import DataFrame
import seaborn as sns
print("最新数据文件名:",os.listdir("./智能面试"))

df_general = pd.read_excel("./智能面试/27837517_2_Java开发答案素材收集（通用部分）_176_176.xls")
index = df_general["用户名"]
general_cols = []
general_cols_simple = []
count = 0
for question in df_general.columns:
#     print(question)
    if question[-1] == "？" or question[-2] == "？":
        count += 1
        general_cols.append(question)
        general_cols_simple.append("q" + str(count))
df_general = df_general.loc[:, general_cols]
df_general.columns = general_cols_simple
df_general.index = index

def what_is_the_general_question(q):
    return general_cols[general_cols_simple.index(q)]

df_general.head()

df_question = pd.read_excel("./智能面试/27837517_2_Java开发答案素材收集（通用部分）_176_176.xls")
index = df_question["用户名"]
question_cols = []
question_cols_simple = []
count = 0
for question in df_question.columns:
    if question[0] == "【":
        count += 1
        question_cols.append(question)
        question_cols_simple.append("q" + str(count))
df_question = df_question.loc[:, question_cols]
df_question.columns = question_cols_simple
df_question.index = index
df_question.head()

def what_is_the_question(q):
    return question_cols[question_cols_simple.index(q)]

df_score = pd.read_excel("./智能面试/团队长打分名单  - fix.xlsx")
df_score = df_score.iloc[0:187,:]
index = df_score["被评分人"]
df_score.index = index
df_score = df_score.iloc[:,1:]
df_score["评分人"] = df_score["评分人"].fillna(method="ffill")
df_score = df_score.dropna()
def text_to_score(text):
    return int(re.findall("[(\d+)]", text)[0])

ability_cols = df_score.columns[2:]
for ability in ability_cols:
    df_score[ability] = df_score[ability].apply(lambda x:text_to_score(x))
del df_score["被评分人"]
# df_score.head()

df = pd.concat([df_question, df_score], axis=1)
df = df.dropna()
for ability in ['学习能力', "创造力", "执行力", "责任心", "团队合作", "不敏感性（是否能很好地应对批评）"]:
    boss_mean = df[ability].groupby(df["评分人"]).mean()
    for name in df.index:
        df[ability][name] = 1 if df[ability][name] > boss_mean[df["评分人"][name]] else 0
df.head()

def plot(feature, ability):
#     print(feature, ability)
    feature_mean = df[ability].groupby(df[feature]).mean()
    feature_count = df[ability].groupby(df[feature]).count()
    feature_df = DataFrame(index=feature_mean.index)
    feature_df["mean"] = feature_mean
    feature_df["count"] = feature_count
    try:
        feature_df.index = feature_df.index.astype(int)
    except:
        pass
    print(feature_df.sort_index())
    sns.factorplot(data=df, x=feature, y=ability, kind="bar")

question = "q6"
ability = "创造力"
print(what_is_the_question(question))
# for ability in ['学习能力', "创造力", "执行力", "责任心", "团队合作", "不敏感性（是否能很好地应对批评）"]:
#     plot(question, ability)
plot(question, ability)

q = "q4"
re_list = ["[0-9一两三]?个?多?半?(小时)(.+分钟)?|\d+分钟"]
["浦东", "黄浦", "静安", "徐汇", "杨浦", "虹口", "闵行", "普陀", "闸北", "青浦", "宝山", "松江", "嘉定", "长宁"]

print("问题:", what_is_the_general_question(q))
sr = df_general[q]
sr_match = sr.copy()
sr_match = False
for pattern in re_list:
    is_match = sr.apply(lambda x: len(re.findall(pattern, x))>0)
    sr_match += is_match

print("匹配率：", str(round(len(sr_match[sr_match])/len(sr_match) * 100, ndigits=2)) + "%")
print(sr[sr_match == False])



### 智能面试（非技术部分）###

import os, sys, re, math
import pandas as pd
from pandas import DataFrame
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
print("最新数据文件名:",os.listdir("./智能面试"))

df_general = pd.read_excel("./智能面试/27837517_2_Java开发答案素材收集（通用部分）_176_176.xls")
index = df_general["用户名"]
general_cols = []
general_cols_simple = []
count = 0
for question in df_general.columns:
#     print(question)
    if question[-1] == "？" or question[-2] == "？":
        count += 1
        general_cols.append(question)
        general_cols_simple.append("q" + str(count))
df_general = df_general.loc[:, general_cols]
df_general.columns = general_cols_simple
df_general.index = index

def what_is_the_general_question(q):
    return general_cols[general_cols_simple.index(q)]

def match_general_question(q, re_list):
    print("问题:", what_is_the_general_question(q))
    sr = df_general[q]
    sr = sr.astype(str)
    sr_match = sr.copy()
    sr_match[:] = False
    for pattern in re_list:
        is_match = sr.apply(lambda x: len(re.findall(pattern, x))>0)
        sr_match += is_match
    print("匹配率：", str(round(len(sr_match[sr_match])/len(sr_match) * 100, ndigits=2)) + "%")
    print("\n", sr[sr_match == False].values)

def score_general_question(q, re_dict):
    lst_5 = re_dict[5]
    lst_4 = re_dict[4]
    lst_3 = re_dict[3]
    lst_2 = re_dict[2]
    lst_1 = re_dict[1]

# 你为什么考虑应聘陆金所？
re_list = ["平安", "互.*金|金.*互", "大平台", "大|龙头|顶尖|吸引|好|优秀|不错|慕名", "发展", "平台", "独角兽", "金融", "推荐|介绍","发展|成长|价值|锻炼", "前景","行业", "知名|名气", "挑战", "稳定", "转岗", "近", "喜欢"]
match_general_question("q1", re_list)

# 你有没有用过陆金所APP？你对陆金所APP有什么建议吗？
re_list = ["没用过|没有", "用过|有|用"]
match_general_question("q2", re_list)

# 您是否有同步应聘其他公司或者收到其他公司的offer，方便透露有哪些公司吗？
re_list = ["没", "不方便", "无|否", "有", "阿里|饿了么|美团|蚂蚁|携程|拼多多"]
match_general_question("q3", re_list)

# 你住在哪个区？来公司上班路上需要多久时间？
re_list = ["[0-9一两三]个?多?半?(小时)(.+分钟)?|\d+分钟", "浦东", "黄浦", "静安", "徐汇", "杨浦", "虹口", "闵行", "普陀", "闸北", "青浦", "宝山", "松江", "嘉定", "长宁"]
match_general_question("q4", re_list)

# 你是如何看待加班问题的？
re_list = ["正常", "接受|愿意|必须加班", "不加班", "减少加班", "常态|普遍|不可避免|正常", "需", "偶尔|偶然|适度|合理|一定程度", "紧急|项目|情况|突发", "必要", "不排斥|可以加班", "自己|自愿", "效率|低效", "费|补偿|无偿|有偿", "调休", "无意义|无节制|抵制|没有必要", "长时间", "尽量|适当", "身体|健康|家人|家庭|生活|父母"]
match_general_question("q5", re_list)

# 如果你和主管想法不一致，这种情况怎么处理？
re_list = ["沟通|协商|交流|协调|探讨", "服从|顺从|妥协|尊重|谦让|遵从|主管意见为|听从", "求同存异", "主管|领导|上级", "坚持|保留", "发表|说明|讨论|提出|阐述|分析|讲解|说服|表达|讲道理"]
match_general_question("q6", re_list)

# 请问你如何看待测试和开发的关系？如果发生矛盾你会如何处理？
re_list = ["沟通|协商|商量|协调|协作|支持|和谐|换位|兄弟|左右手|互补|共生|相互|互相", "就事论事", "对事", "不会", "需求", "保险|保障|保证", "站在对方角度", "合作", "讨论", "如果", "解决", "相辅相成", "配合", "具体", "上级|领导"]
match_general_question("q7", re_list)

# 你最近有看过什么技术方面的书或文章吗？
re_list = ["机器学习", "AI|ai|人工智能", "深度学习", "区块", "没有|无", "虚拟机", "模型|编程|源码|模式", "JMM|jvm|spring|Spring|java|Java"]
match_general_question("q8", re_list)

问题: 你最近有看过什么技术方面的书或文章吗？
匹配率： 64.77%

 ['docker' 'nature论文，及gitlab最新技术的项目跟进' '看过' '在看JAVA方面的技术书籍' 'TiDB'
 '看一些架构及JVM优化方便的书' '有' '会看些技术文章' '看过不少关于云计算的文章' '有' '看一些公众号技术文章'
 '有，一些基础原理的书' '最近看过一些系统架构方面的书' 'GO语言相关资料' '最近在研究J.C.U 的实现原理' 'kafka'
 'tensorflow' '有' '有' '有' '设计原本，kafka权威指南。' '有' '大前端开发，vuejs，分布式架构等内容'
 '没时间' '有的，一直在坚持，虽然不擅长这个行业，但既然选择了，就要坚持学习坚持进步。'
 '深入理解计算机系统\ntcp/ip详解\nredis设计与实现\n等等。。。。。。' '小程序相关文档，架构管理类' '不喜欢看。'
 '关注一些好的技术博客' 'docker' '大数据' '一直都会看' '容器相关' '在听极客时间。' '关注一些大咖公众号和一些业界牛的公司'
 'Python相关' '看过。\n开发需要保持技术的敏感度，最近再看kotlin、docker的技术文章。' '很多' '一直在看' '有'
 '有' 'Kafka技术内幕' '有，比较散，基本围绕提高程序员的自我修养看' 'hadoop相关文章' 'G1实现' '人月神话'
 '微信小程序，网站架构' '经常阅览，与时俱进' '代码重构、大规模高并发、面向领域设计' '经常看一些工作相关技术书' '有' '有'
 '有，经常' '密码学原理，go语言' 'docker，mq' '有' '天天看' '有' '有' '很多' 'ReactNative'
 '最近看过python方面的书籍']

# 有没有利用业务时间做过小软件、小程序或者小插件？实现了什样的功能？
re_list = ["没|无", "有|做过", "不方便透露", "功能|用于|实现|自动|爬虫|工具|小程序|自己用", "时间", "偶尔"]
match_general_question("q9", re_list)

问题: 有没有利用业务时间做过小软件、小程序或者小插件？实现了什样的功能？
匹配率： 93.18%

 ['尝试过微信支付的对接，尝试过区块链技术' 'hadoop实验' '经常关注github' '挡板系统等'
 '通过机器学习，预测使用产品的客户数量。' 'nan' 'express,信息管理' '小型情景休闲游戏APP' '看书多，实践少'
 '番茄工作法；提高工作效率；' 'No' '自己动手写简单的Java虚拟机']
​
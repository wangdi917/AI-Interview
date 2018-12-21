
# AI interview
AI面试项目。 由候选人答题，由机器评分。

### Install dependency:
- 需要安装SpaCy模块，具体方法见“Spacy安装命令.txt”。
- [就算点我也未必行](https://github.com/wangdi917/AI-Interview/blob/master/Spacy%EF%BC%88Win%E7%8E%AF%E5%A2%83%EF%BC%89%E5%AE%89%E8%A3%85%E5%91%BD%E4%BB%A4.txt)

### Directory tree:
```
interview-app/
├── data
│   └── Java_Simple.xls 		# Java面试数据
├── src
│   ├── main.py 			# 王博士讳迪写的主程序代码
│   ├── interview_generic.py 		# 普通面试类代码
│   ├── interview_JavaEng.py 		# Java面试类代码
│   ├── log.py 				# 日志代码
│   ├── const.py 			# 常数定义代码
│   └── approaches 			# 王博士讳迪写的Java面试类面试评分代码
├── lib 				# 中文Python自然语言处理模块
│   ├── cc.zh.300.vec.gz
│   ├── zh_core_web_sm-2.0.5.tar.gz
│   └── customized_jieba_dict.txt
├── models 				# 训练生成的模型
├── tests 				# 模型测试
├── settings.ini 			# 环境变量设置
└── README.md

```

### Launch AI interview program: 用规则匹配和自然语言处理为面试者的回答打分
```bash
python main.py
```

Example1:
```
我司：你有没有用过我司的APP？有什么建议吗？
	张某：没有用过，对于乱约类app不是很了解。想了解下是否有类似于伴游性质的交友功能？
	李某：有，我希望有更多美女照片，另外你司app打开登录时间太慢了。
	我司：李某得分+3。

我司：你最近有看过什么技术方面的书或文章吗？
	张某：美工；分布式环境的反PS工具反美颜工具比如丑图秀秀。
	李某：看过AV等方面的书和文章，并且跟进了解了AV图像和影像。
	我司：张某得分+1。

我司：你是如何看待加班问题的？
	刘某：珍惜生命，远离加班……
	我司：负分滚粗！
```
```bash
python main.py
$ [张:3, 李:1, 刘:-1]
```

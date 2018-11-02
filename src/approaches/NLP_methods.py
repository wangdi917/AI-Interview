from __future__ import absolute_import, unicode_literals, print_function, division
import os, sys, argparse
import logging
from autologging import logged
import numpy as np
import pandas as pd
import re
import json
import warnings

from const import *
from configs.config import log_set_from_config, ConfigFactory
# 因为整个项目的main.py需要在\interview-app\src\路径下运行，所以以上import可以实现。


warnings.filterwarnings("ignore")


import spacy
import plac
from spacy import displacy
from spacy.vocab import Vocab
from spacy.attrs import LEMMA
from spacy.tokens import Span
from spacy.symbols import ORTH, LEMMA, POS, TAG


@logged(logging.getLogger("approaches.NLP_Chinese"))

def China_No1():
	try:
		import zh_core_web_sm
		nlp = zh_core_web_sm.load()
		China_No1._log.info("The 'zh_core_web_sm' module has been loaded in order to handle Chinese based on SpaCy.")
	except (ModuleNotFoundError, IOError) as e1:
		China_No1._log.error("The 'zh_core_web_sm' module cannot be loaded!\n{}".format(e1))
		from spacy.lang.zh import Chinese
		nlp = Chinese()
	except Exception as e2:
		China_No1._log.critical("Neither the 'en_core_web_sm' nor the 'zh_core_web_sm' module can be loaded!\n{}\n".format(e2))

	import jieba
	# SETTING_FILE = const.SETTING_FILE
	current_path = os.path.dirname(os.getcwd()) + '/'
	CONFIG = ConfigFactory(SETTING_FILE).load_config()
	jieba_dict_path = CONFIG.get("lib", "jieba_dict_path")
	customized_jieba_dict = current_path + jieba_dict_path + CONFIG.get("lib", "jieba_dict_file")
	try:
		# 因为zh_core_web_sm已经错误地指定了如何分词，所以只能强行让jieba加载自定义字典。频率越高，成词的概率就越大。
		# https://github.com/fxsjy/jieba/issues/14
		jieba.load_userdict(customized_jieba_dict)
		China_No1._log.info("The customized jieba dictionary '{}' has been loaded.\n".format(customized_jieba_dict))
	except Exception as e3:
		China_No1._log.error("The customized jieba dictionary '{}' cannot be loaded!\n{}\n".format(customized_jieba_dict, e3))

	return nlp


# Token是词或标点，所以其属性有attributes、tags、dependencies等等。 Lexeme是word type，没有内容，所以其属性有shape、stop、flags等等。
# Doc是一些Token的序列，Vocab是一些Lexeme的序列，Span是Doc的一个slice，StringStore是把hash值映射成字符串的字典。 所以遍历doc得到token，遍历vocab得到lexeme，lexeme=doc.vocab[token.text]。
# 如果Doc是nlp(u"2018年9月27日")，那么Span(doc,0,1)=''，Span(doc,0,2)='2018'，Span(doc,0,3)='2018年'……


@logged(logging.getLogger("approaches.NLP_methods"))

def tokenize(nlp, s):
	# .pos_包括： NOUN、 VERB、 PRON、 PROPN、 ADJ、 ADV、 ADP、 DET、 CCONJ、 SPACE、 PART、 SYM、 NUM、 X、 INTJ……
	# .tag_包括： NN、 NNS、 VBP、 JJ、 JJR、 PRP、 DT、 IN……
	# 其他判别包括：is_alpha、is_punct、is_digit、like_num、like_email……
	tokenize._log.debug("\nThe outcomes of tokenization '{}' are:".format(s))
	doc = nlp(s)
	for token in doc:
		tokenize._log.debug("\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(token.text, token.lemma_, token.ent_iob, token.ent_iob_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)) # B=3, I=1, O=2, 中文没有I。
	return doc


@logged(logging.getLogger("approaches.NLP_methods"))

def chunk(nlp, s):
	chunk._log.debug("\nThe outcomes of chunking '{}' are:".format(s))
	doc = nlp(s)
	for chunk in doc.noun_chunks:
		chunk._log.debug("\t{}\t{}\t{}\t{}".format(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text))
	return doc
	# text	lemma_	ent_iob_ent_iob_	pos_	tag_	dep_		shape_	is_alpha	is_stop
	# 容器	容器			2	O			X		NN		case:suff	xx		True	False
	# 化		化			2	O			X		SFV		nmod		x		True	False
	# ；		；			2	O			X		CD		nmod		；		False	True
	# 分布式	分布式		2	O			X		NN		nmod		xxx		True	False
	# 环境	环境			2	O			X		NN		det			xx		True	False
	# 的		的			2	O			X		DEC		case:dec	x		True	True
	# 协调	协调			2	O			X		NN		nmod		xx		True	False
	# 工具	工具			2	O			X		NN		nsubj		xx		True	False
	# 比如	比如			2	O			X		VV		ROOT		xx		True	True
	# consulconsul		2	O			X		FW		obj			xxxx	True	False
	# 、		、			2	O			X		EC		punct		、		False	True
	# etcd	etcd		3	B			X		NNP		conj		xxxx	True	False


@logged(logging.getLogger("approaches.NLP_methods"))

def extract_entity(nlp, s):
	extract_entity._log.debug("\nThe outcomes of extraction '{}' are:".format(s))
	doc = nlp(s)
	for ent in doc.ents:
		extract_entity._log.debug("\t{}\t\t{}\t{}\t{}\t{}\t{}".format(ent.text, ent.start_char, ent.end_char, ent.label_, doc[doc.ents.index(ent)].ent_iob_, doc[doc.ents.index(ent)].ent_type_))
	return doc


@logged(logging.getLogger("approaches.NLP_methods"))

def add_entity(nlp, doc, entity_start, entity_stop, l):
	augment = [Span(doc, entity_start, entity_stop, label=doc.vocab.strings[l])]
	doc.ents = list(doc.ents) + augment
	for ent in doc.ents:
		add_entity._log.debug("\t{}\t\t{}\t{}\t{}\t{}\t{}".format(ent.text, ent.start_char, ent.end_char, ent.label_, doc[doc.ents.index(ent)].ent_iob_, doc[doc.ents.index(ent)].ent_type_))
	return doc


@logged(logging.getLogger("approaches.NLP_methods"))

def vectorize(nlp, s, vector_file=None):
	vectorize._log.debug("\nThe outcomes of vectorization '{}' are:".format(s))
	if vector_file is not None:
		nlp = spacy.load(vector_file)
	doc = nlp(s)
	for token in doc:
		vectorize._log.debug("\t{}\t{}\t{}\t{}".format(token.text, token.has_vector, token.vector_norm, token.is_oov))
	return doc


@logged(logging.getLogger("approaches.NLP_methods"))

def similarize(nlp, s, vector_file=None):
	similarize._log.debug("\nThe outcomes of similarity '{}' are:".format(s))
	if vector_file is not None:
		nlp = spacy.load(vector_file)
	doc = nlp(s)
	for token1 in doc:
		for token2 in doc:
			similarize._log.debug("\t{} <=> {} : {}".format(token1.text, token2.text, token1.similarity(token2)))
	return doc


@logged(logging.getLogger("approaches.NLP_methods"))

def separate(nlp, s, stop_file=None):
	separate._log.debug("\nThe outcomes of separation '{}' are:".format(s))
	# 因为需要nlp.remove_pipe()和nlp.add_pipe(SS)，所以必须重新import zh、不能从外部传参进来，否则会有ValueError。泥马这个坑爹bug花了哥一个上午才搞定！泥马坑爹！
	import zh_core_web_sm
	nlp = zh_core_web_sm.load()
	
	from spacy.pipeline import SentenceSegmenter
	def split_on_punctuation(doc):
		punctuation = ",;，；、和与"
		# punctuation = re.compile(r",.:;?!，。：；？！")
		start = 0
		whether_segmenter = False
		for word in doc:
			if whether_segmenter or word.is_space: # and not word.is_space!
				yield doc[start:word.i]
				start = word.i
				whether_segmenter = False
			elif word.text in punctuation:
				whether_segmenter = True
		if start < len(doc):
			yield doc[start:len(doc)]
	
	SS = SentenceSegmenter(nlp.vocab, strategy=split_on_punctuation)
	nlp.add_pipe(SS)
	doc = nlp(s)
	for sent in doc.sents:
		separate._log.debug("\t{}".format(sent.text))
	return doc


@logged(logging.getLogger("approaches.NLP_methods"))

def words_stop():
	words_stop._log.debug("\nThe outcomes of words stop are:")
	from spacy.lang.en.stop_words import STOP_WORDS
	# print (STOP_WORDS)
	STOP_WORDS.add("your_additional_stop_word_here")
	for word in STOP_WORDS:
		lexeme = nlp.vocab[word]
		lexeme.is_stop = True

	nlp.Defaults.stop_words |= {"了", "啊", "吧", "嗯"} # 单个词可以直接.add()
	nlp.Defaults.stop_words -= {"嗯"} # 单个词可以直接.remove()
	for word in nlp.Defaults.stop_words:
		lexeme = nlp.vocab[word]
		lexeme.is_stop = True
	words_stop._log.debug(nlp.Defaults.stop_words)

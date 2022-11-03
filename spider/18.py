# -*- coding: UTF-8 -*-
# 分词测试
import re


punc = '，。、【 】 “”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=&#@￥'
content = '东宝惟金，南木有乔。发辉曾崖，竦干重霄。美哉兹土，世载英髦。育翮幽林，养音九皋。（一章）唐后明扬，汉宗蒲轮。我皇降鉴，思乐怀人。群臣竞荐，旧章惟新。余亦奚贡，曰义与仁。（二章）仁义伊在，惟吴惟潘。心积纯孝，事著艰难。投死如归，淑问若兰。吴实履仁，心力偕单。固此苦节，易彼岁寒。霜寻虽厚，松柏丸丸。（三章）人亦有言，无善不彰。二子徽猷，弥久弥芳。拔丛出类，景行朝阳。谁谓道遐，弘之则光。咨尔庶士，无然怠荒。（四章）江革奉挚，庆禄是荷。姜诗入贡，汉朝咨嗟。勖哉行人，敬尔休嘉。俾是下国，炤辉京华。（五章）伊余朽骀，窃服惧盗。无能礼乐，岂暇声教。顺彼康夷，懿德是好。聊缀所怀，以赠二孝（○《宋书》潘综传。《诗纪》四十五。）。（六章）'
pattern = re.compile('（[^）]*）')
p = pattern.sub('', content)

print(p)
print("*****jieba默认库*****")
import jieba
word_list = [w for w in jieba.cut(p, cut_all=False) if w not in punc]
print(word_list)
print("*****加入意象后的自建库*****")
jieba.load_userdict("image.txt")
# import jieba.posseg as pseg
# word_list = [w.word for w in pseg.cut(p) if w.flag[0] not in ['x', 'w']]
# print(word_list)
word_list = [w for w in jieba.cut(p, cut_all=False) if w not in punc]
print(word_list)

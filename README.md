# 古诗词爬虫和文本挖掘

**爬虫和文本挖掘部分代码和数据开源**

- spider：爬虫和数据清洗代码，文件具体功能见第一行注释
- data：数据整理结果，包括13个朝代的3万多条诗人数据，85万多首诗词数据，10万多条意象数据，近2万首含译注赏析的诗词数据，以及各个朝代不同省市的诗人信息
- topic_model&LSA：主题聚类和推荐模型
- GPT2-Chinese-old_gpt_2：GPT2实现藏头诗生成，含训练好的模型，可以输入格律、风格和藏头字，自动生成藏头诗
- bert2transformer_on_NMT：Bert实现翻译模型，含训练好的模型，输入文言文或者古诗词，会自动生成相应的白话文翻译

由于github文件大小限制，仓库里主要包含代码文件，数据和模型文件存于百度网盘（链接: https://pan.baidu.com/s/1ExaqJ4O35MZP-EQrgoFCIA 提取码: hg5j）


**参考博客：**

- [万字长文！用文本挖掘深度剖析54万首诗歌](https://blog.csdn.net/BF02jgtRS00XKtCx/article/details/108191211)

- [gensim中word2vec使用](https://blog.csdn.net/u010700066/article/details/83070102)

- [最小熵原理（五）：“层层递进”之社区发现与聚类](https://kexue.fm/archives/7006)



**参考代码和语料：**

- https://github.com/kpu/kenlm

- https://github.com/jiaeyan/Jiayan

- https://github.com/rjk-git/bert2transformer_on_NMT

- https://github.com/Morizeyao/GPT2-Chinese

- https://github.com/NiuTrans/Classical-Modern

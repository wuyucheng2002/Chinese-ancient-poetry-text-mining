import argparse
import thulac
import json

from tqdm import tqdm
from keras.preprocessing.text import Tokenizer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_data_path', default='../data/train.json', type=str, required=False, help='原始训练语料')
    parser.add_argument('--vocab_file', default='vocab_processed.txt', type=str, required=False, help='生成vocab链接')
    parser.add_argument('--vocab_size', default=100000, type=int, required=False, help='词表大小')
    args = parser.parse_args()

    lac = thulac.thulac(seg_only=True)
    tokenizer = Tokenizer(num_words=args.vocab_size)
    print('args:\n' + args.__repr__())
    print('This script is extremely slow especially for large corpus. Take a break.')

    f = open(args.raw_data_path, 'r')
    lines = json.load(f)
    for i, line in enumerate(tqdm(lines)):
        lines[i] = lac.cut(line, text=True)

    tokenizer.fit_on_texts(lines)
    vocab = list(tokenizer.index_word.values())
    pre = ['[SEP]', '[CLS]', '[MASK]', '[PAD]', '[UNK]']
    li1 = ['七言律诗', '五言律诗', '七言绝句', '五言绝句']
    li2 = ['黯然神伤', '水天一色', '心系国家', '山川巍峨', '羁旅思乡', '田园躬耕', '鸟语花香', '静悟禅机',
           '金戈铁马', '对酒当歌', '得道修仙', '爱情闺怨', '云游四方', '弹琴阅经', '世事变迁', '送别思旧']
    vocab = pre + li1 + li2 + vocab
    with open(args.vocab_file, 'w', encoding='utf-8') as f:
        for word in vocab[:args.vocab_size + 5 + 4 + 16]:  #
            f.write(word + '\n')


if __name__ == "__main__":
    main()

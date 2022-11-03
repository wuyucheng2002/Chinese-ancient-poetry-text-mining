import torch
import torch.nn.functional as F
from transformers import GPT2LMHeadModel
from tokenizations import tokenization_bert


def is_word(word):
    for item in list(word):
        if item not in 'qwertyuiopasdfghjklzxcvbnm':
            return False
    return True


def _is_chinese_char(char):
    cp = ord(char)
    if ((cp >= 0x4E00 and cp <= 0x9FFF) or  #
            (cp >= 0x3400 and cp <= 0x4DBF) or  #
            (cp >= 0x20000 and cp <= 0x2A6DF) or  #
            (cp >= 0x2A700 and cp <= 0x2B73F) or  #
            (cp >= 0x2B740 and cp <= 0x2B81F) or  #
            (cp >= 0x2B820 and cp <= 0x2CEAF) or
            (cp >= 0xF900 and cp <= 0xFAFF) or  #
            (cp >= 0x2F800 and cp <= 0x2FA1F)):  #
        return True

    return False


def top_k_top_p_filtering(logits, top_k=0, top_p=0.0, filter_value=-float('Inf')):
    assert logits.dim() == 1  # batch size 1 for now - could be updated for more but the code would be less clear
    top_k = min(top_k, logits.size(-1))  # Safety check
    if top_k > 0:
        # Remove all tokens with a probability less than the last token of the top-k
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = filter_value

    if top_p > 0.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
        # Remove tokens with cumulative probability above the threshold
        sorted_indices_to_remove = cumulative_probs > top_p
        # Shift the indices to the right to keep also the first token above the threshold
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0
        indices_to_remove = sorted_indices[sorted_indices_to_remove]
        logits[indices_to_remove] = filter_value
    return logits


def fast_sample_sequence(model, context, length, temperature=1.0, top_k=30, top_p=0.0, device='cpu'):
    inputs = torch.LongTensor(context).view(1, -1).to(device)
    if len(context) > 1:
        _, past = model(inputs[:, :-1], None)[:2]
        prev = inputs[:, -1].view(1, -1)
    else:
        past = None
        prev = inputs
    generate = [] + context
    with torch.no_grad():
        for i in range(length):
            output = model(prev, past=past)
            output, past = output[:2]
            output = output[-1].squeeze(0) / temperature
            filtered_logits = top_k_top_p_filtering(output, top_k=top_k, top_p=top_p)
            next_token = torch.multinomial(torch.softmax(filtered_logits, dim=-1), num_samples=1)
            generate.append(next_token.item())
            prev = next_token.view(1, 1)
    return generate


if __name__ == '__main__':

    genre = '五言律诗'
    topic = '山川巍峨'
    prefix = '一叶知秋'

    if genre == '七言律诗':
        length = 64
    elif genre == '七言绝句':
        length = 32
    elif genre == '五言律诗':
        length = 48
    else:
        length = 24

    nsamples = 5
    tokenizer = tokenization_bert.BertTokenizer(vocab_file='model/vocab_processed.txt')
    model = GPT2LMHeadModel.from_pretrained('model')
    raw_text = '[CLS]' + genre + '[SEP]' + topic + '[SEP]' + prefix + '[SEP]'
    model.to('cpu')
    model.eval()

    context_tokens = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(raw_text))
    nn = 0
    while True:
        if nn == nsamples:
            break
        else:
            out = fast_sample_sequence(model=model, context=context_tokens, length=length, temperature=1.0, top_k=8,
                                       top_p=0, device='cpu')
            text = tokenizer.convert_ids_to_tokens(out)
            for i, item in enumerate(text[:-1]):  # 确保英文前后有空格
                if is_word(item) and is_word(text[i + 1]):
                    text[i] = item + ' '
            for i, item in enumerate(text):
                if item == '[CLS]':
                    text[i] = '\n\n'
                elif item == '[SEP]':
                    text[i] = '\n'
            text = ''.join(text).replace('##', '').strip()
            text = text.replace('\n', '')
            if '[UNK]' not in text:
                if genre == '七言律诗':
                    a, b, c, d = 16, 32, 48, 64
                elif genre == '五言律诗':
                    a, b, c, d = 12, 24, 36, 48
                elif genre == '七言绝句':
                    a, b, c, d = 8, 16, 24, 32
                else:
                    a, b, c, d = 6, 12, 18, 24
                con = text[12:]
                if con[b - 1] == '。' and con[d - 1] == '。':
                    nn += 1
                    con = con[0:a] + '\n' + con[a:b] + '\n' + con[b:c] + '\n' + con[c:d]
                    print("=" * 10 + " SAMPLE " + str(nn) + " " + "=" * 10)
                    print(con)

import itertools


def make_windowed_data(data, start, end, window_size=1):

    windowed_data = []
    for sentence, labels in data:
        ### YOUR CODE HERE (5-20 lines)
        for index, label in zip(range(len(sentence)), labels):
            windowed_word = window_word(index, sentence, start, end, window_size)
            windowed_data.append((windowed_word, label))
        ### END YOUR CODE
    return windowed_data


def window_word(index, sentence, start, end, window_size):
    windowed_word = []
    for i in range(index-window_size, index+window_size+1):
        if i < 0:
            windowed_word.append(start)
        elif i >= len(sentence):
            windowed_word.append(end)
        else:
            windowed_word.append(sentence[i])
    return list(itertools.chain.from_iterable(windowed_word))


def test_make_windowed_data():
    sentences = [[[1, 1], [2, 0], [3, 3]]]
    sentence_labels = [[1, 2, 3]]
    data = zip(sentences, sentence_labels)
    w_data = make_windowed_data(data, start=[5, 0], end=[6, 0], window_size=1)

    print w_data

    assert len(w_data) == sum(len(sentence) for sentence in sentences)

    assert w_data == [
        ([5, 0] + [1, 1] + [2, 0], 1,),
        ([1, 1] + [2, 0] + [3, 3], 2,),
        ([2, 0] + [3, 3] + [6, 0], 3,),
    ]


if __name__ == '__main__':
    test_make_windowed_data()

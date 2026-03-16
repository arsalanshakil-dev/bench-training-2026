def word_frequency (text):
    frequency = {}
    for word in text.split():
        lower_word = word.lower().strip('.,!?";()')
        if lower_word in frequency:
            frequency[lower_word] += 1
        else:
            frequency[lower_word] = 1
    return frequency

text = "This is a sample text. This text is just a sample."
print(sorted(word_frequency(text).items()))
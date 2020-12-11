class twitter:
    def __init__(self, tweet_text, retweet_count, reply_count):
        self.tweet_text = tweet_text
        self.retweet_count = retweet_count
        self.reply_count = reply_count


class output:
    def __init__(self, number_of_retweets, number_of_replies, positive_score, negative_score, net_score):
        self.number_of_retweets = number_of_retweets
        self.number_of_replies = number_of_replies
        self.positive_score = positive_score
        self.negative_score = negative_score
        self.net_score = net_score


def read_words(file):
    file = open(file, "r")
    lines = None
    is_first_semicolon_sequence = None
    is_second_semicolon_sequence = None
    ret = []
    if file.mode == "r":
        lines = file.readlines()
    file.close
    for line in lines:
        if is_second_semicolon_sequence:
            if line != "\n":
                ret.append(line.lower().strip())
        else:
            if line.find(";;;") != -1:
                if not is_first_semicolon_sequence:
                    is_first_semicolon_sequence = True
                    continue
                elif is_first_semicolon_sequence and not is_second_semicolon_sequence:
                    is_second_semicolon_sequence = True
                    continue
    return ret


def read_text():
    punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']
    file = open("files/project_twitter_data.csv", "r")
    ret = []
    if file.mode == "r":
        lines = file.readlines()
    file.close
    for line in lines:
        if line != "\n":
            splited = line.lower().strip().split(",")
            text = splited[0]
            for c in punctuation_chars:
                text = text.replace(c, " ")
            ret.append(twitter(text, splited[1], splited[2]))
    return ret


def count_words(text, words):
    ret = 0
    for w in words:
        for wt in text.split(" "):
            if w == wt:
                print('Word [{}] found in "{} text!"'.format(w, text))
                ret = ret + 1
    return ret


def sentiment_analysis(base_text, positive_words_array, negative_words_array):
    positive_score = 0
    negative_score = 0
    net_score = 0
    ret = []
    for l in base_text:
        text = l.tweet_text
        positive_score = count_words(text, positive_words_array)
        negative_score = count_words(text, negative_words_array)
        net_score = positive_score - negative_score
        if net_score > 0:
            print('[POSITIVE]: {}\n'.format(text))
        elif net_score < 0:
            print('[NEGATIVE]: {}\n'.format(text))
        else:
            print('[NEUTRAL]: {}\n'.format(text))
        ret.append(
            output(
                l.retweet_count,
                l.reply_count,
                positive_score,
                negative_score,
                net_score
            )
        )
    return ret


def generate_output(sentiment_analysis_result):
    output_file = open("files/resulting_data.csv", "w")
    output_file.write(
        "Number of Retweets,Number of Replies,Positive Score,Negative Score,Net Score\n")
    for l in sentiment_analysis_result:
        str = "{},{},{},{},{}\n".format(
            l.number_of_retweets,
            l.number_of_replies,
            l.positive_score,
            l.negative_score,
            l.net_score
        )
        output_file.write(str)
    output_file.close()


def main():
    positive_words_array = read_words("files/positive_words.txt")
    negative_words_array = read_words("files/negative_words.txt")
    base_text = read_text()
    sentiment_analysis_result = sentiment_analysis(
        base_text[1:],
        positive_words_array,
        negative_words_array)
    generate_output(sentiment_analysis_result)


main()

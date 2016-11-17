import base64
from collections import defaultdict

from utils import *

if __name__ == "__main__":
    with open("../data/8.txt") as fp:
        lines = fp.readlines()

    raw_lines = [line[:-1].decode("hex") for line in lines]
    scores = [ECB_score(line) for line in raw_lines]
    repetitions = [repeated_blocks(line, 16) for line in raw_lines]
    linenum, scores = zip(*enumerate(scores))
    # print("Candidate line for ECB: {}", i)

    best = max(enumerate(repetitions), key=lambda x: x[1])
    print("Line {} is most likely the ECB candidate with a maxrep of {}".format(best[0]+1, best[1]))

    # fig = dict(
    #     data = [
    #         go.Scatter(
    #             x = linenum,
    #             y = scores
    #         ),
    #         go.Scatter(
    #             x = linenum,
    #             y = repetitions
    #         )
    #     ],
    #     layout = dict(
    #         title = "Averaged Hamming distance between ciphertext blocks ",
    #         xaxis = dict(title = 'line number'),
    #         yaxis = dict(title = 'Metric'),
    #      )
    # )
    # py.iplot(fig, filename="ecb-detection")

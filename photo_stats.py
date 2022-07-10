#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import csv
import pprint
import argparse

AVAILABLE_MARKS = range(6,21)

def do_plot(marks, ticks=None):
    # transpose array: transforming the list of marks per picture to a list of marks per voter
    votes = list(map(list, zip(*marks)))
    counts = [[v.count(i) for v in votes] for i in AVAILABLE_MARKS]

    fig = plt.figure(figsize=(15, 10))
    box = fig.add_subplot(2, 1, 1)
    graph = fig.add_subplot(2, 1, 2)
    fig.suptitle('Statistisques des notes du concours', fontsize=16)

    box.boxplot(marks, sym='.',
        showmeans=True, meanline=True, meanprops={'color':'black', 'linestyle':'dotted'},
        medianprops={'color':'black'}
        )
    box.set_title('Dispersion des notes de chaque photo')
    if ticks:
        print('custom ticks')
        #box.set_xticks(len(ticks))
        box.set_xticklabels(ticks)
    box.tick_params(axis='both', which='major', labelsize=8)
    box.set_xlabel('Images (classées de la première à la dernière)')
    box.set_ylabel('Note')

    graph.plot(AVAILABLE_MARKS, counts, color='#CCCCCC')
    graph.plot(AVAILABLE_MARKS, [np.average(m) for m in counts], color='#666666')
    graph.set_title('Répartition des notes par votant')
    graph.tick_params(axis='both', which='major', labelsize=8)
    graph.set_xlabel('Note')
    graph.set_ylabel('Nombre de fois où la note à été donnée')

    # give the second graph more space and reduce horizontal margins
    plt.subplots_adjust(hspace=.3, left=.075, right=.95)

    return fig

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', metavar='FILE',
        help='If specifid saves the plots in FILE, otherwise show them in a new window.')
    parser.add_argument('CSVFILE', 
        help='CSV file (semicolon delimited) containing the marks: one picture per row.')
    args = parser.parse_args()

    with open(args.CSVFILE, 'r') as csvfile:
        r = csv.reader(csvfile, delimiter=';')
        marks = []
        for image in r:
            marks.append([int(x) for x in image])

        do_plot(marks, ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "12", "14", "15", "16", "17", "18", "19", "20", "20", "22", "23", "24", "24", "26", "26", "28", "28", "30", "31", "32", "32", "34", "34", "36", "37", "38", "38", "38" ])

        if args.output:
            plt.savefig(args.output)
        else:
            plt.show()
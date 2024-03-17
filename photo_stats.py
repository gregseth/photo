#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import csv
import json
import pprint
import argparse

def do_plot(marks, ticks=None, min=0, max=10):
    markspan = range(min, max+1)
    # transpose array: transforming the list of marks per picture to a list of marks per voter
    votes = list(map(list, zip(*marks)))
    counts = [[v.count(i) for v in votes] for i in markspan]

    fig = plt.figure(figsize=(16, 9))
    box = fig.add_subplot(2, 1, 1)
    graph = fig.add_subplot(2, 1, 2)
    #fig.suptitle('Statistisques des notes', fontsize=16)

    box.boxplot(marks, sym='.',
        showmeans=True, meanline=True, meanprops={'color':'black', 'linestyle':'dotted'},
        medianprops={'color':'black'}
        )
    box.set_title('Dispersion des notes de chaque photo')
    if ticks:
        box.set_xticklabels(ticks)
    box.tick_params(axis='both', which='major', labelsize=8)
    box.set_xlabel('Images (classées de la première à la dernière)')
    box.set_ylabel('Note')

    graph.plot(markspan, counts, color='#CCCCCC')
    graph.plot(markspan, [np.average(m) for m in counts], color='#666666')
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
    parser.add_argument('--csv', '-c', metavar='CSVFILE', 
        help='CSV file (semicolon delimited) containing the marks: one picture per row.')
    parser.add_argument('--json', '-j', metavar='JSONFILE', 
        help='JSON file containing the request in the format:\n{ "marks": [[]], "picture_id": [], "voter_id": [], "rank": [] }')
    args = parser.parse_args()

    if args.csv:
        with open(args.csv, 'r') as csvfile:
            r = csv.reader(csvfile, delimiter=';')
            marks = []
            for image in r:
                marks.append([int(x) for x in image])

            do_plot(marks, [str(x) for x in range(1, len(marks)+1)])

    if args.json:
        with open(args.json, 'r') as jsonfile:
            j = json.load(jsonfile)
            do_plot(j['marks'], j['rank'])


    if args.output:
        plt.savefig(args.output)
    else:
        plt.show()
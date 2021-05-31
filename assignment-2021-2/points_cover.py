import itertools
import argparse
import sys
from src.utils import parseFile, solve, brute, solveParallel

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("points_file")
    parser.add_argument('-f','--foo', action='store_true')
    parser.add_argument('-g','--goo', action='store_true')

    args = parser.parse_args()
    #print(args.points_file)
    #print(args.foo)
    #print(args.goo)

    points = parseFile(args.points_file)
    lines = []
    if args.foo:
        lines = brute(points)
        for l in lines:
            print(l)
    elif args.goo:
        lines = solveParallel(points)
        for l in lines:
            print(l)
    else :
        lines = solve(points)
        for l in lines:
            print(l)

if __name__ == "__main__":
    main()

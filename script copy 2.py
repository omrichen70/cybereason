import argparse
import os
from os.path import isfile, join, isdir
from os import listdir
from subprocess import Popen
import grpc_tools
from grpc_tools import protoc


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def getFiles(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files


def getDirs(path):
    dirs = [d for d in listdir(path) if isdir(join(path, d))]
    return dirs


def compProtos(frompath, topath):
    remainings = getDirs(frompath)
    files = getFiles(frompath)
    for i in range(len(files)):
        # add prints
        if files[i].endswith('.proto'):
            print(
                f'Currently generating file: {files[i]}, from path: {frompath}')
            process = Popen(
                f'python -m grpc_tools.protoc -I {frompath} --python_out={topath} --grpc_python_out={topath} {frompath}/{files[i]}')
    return remainings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run gRPC on protobuffs')
    parser.add_argument('-from', dest="frompath", type=dir_path,
                        required=True, help="Enter protobuffs path", metavar="FILE")
    parser.add_argument('-to', dest="topath", type=dir_path, default=".",
                        help="Enter saving path", metavar="FILE")
    args = parser.parse_args()
    remainings = compProtos(args.frompath, args.topath)
    frompath = args.frompath
    while(remainings):
        for i in range(len(remainings)):
            frompath = frompath + '/' + remainings[i]
            print("Getting into folder:" + frompath)
            compProtos(frompath, args.topath)
        remainings = compProtos(frompath, args.topath)
    print("Done generating protobuffs, results in folder: " + args.topath)

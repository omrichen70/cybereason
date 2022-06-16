import argparse
import os
from os.path import isfile, join
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


def compProtos(remainings, files):
    for i in range(len(files)):
        # add prints
        if os.path.isfile(files[i]):
            print(
                f'Currently generating file: {files[i]}, from path: {args.frompath}')
            process = Popen(
                f'python -m grpc_tools.protoc -I {args.frompath} --python_out={args.topath} --grpc_python_out={args.topath} {args.frompath}/{files[i]}'
            )
        elif os.path.isdir(files[i]):
            remainings.append(files[i])
    return remainings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run gRPC on protobuffs')
    parser.add_argument('-from', dest="frompath", type=dir_path,
                        required=True, help="Enter protobuffs path", metavar="FILE")
    parser.add_argument('-to', dest="topath", type=dir_path, default=".",
                        help="Enter saving path", metavar="FILE")
    args = parser.parse_args()
    print(args.frompath + "IS HERE")
    files = getFiles(args.frompath)
    print(files)
    remainings = compProtos([], files)
    print(remainings)
    while remainings:
        args.frompath = remainings[0]
        remainings.pop(0)
        remainings = compProtos(remainings, files)

    print("done")

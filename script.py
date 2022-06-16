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


def compProtos(frompath, topath):
    for dirpath, dirs, files in os.walk(frompath):
        for filename in files:
            if filename.endswith('.proto'):
                print(
                    f'Currently generating file: {filename}, from path: {dirpath}')
                process = Popen(
                    f'python -m grpc_tools.protoc -I {dirpath} --python_out={topath} --grpc_python_out={topath} {dirpath}/{filename}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run gRPC on protobuffs')
    parser.add_argument('-from', dest="frompath", type=dir_path,
                        required=True, help="Enter protobuffs path", metavar="FILE")
    parser.add_argument('-to', dest="topath", type=dir_path, default=".",
                        help="Enter saving path", metavar="FILE")
    args = parser.parse_args()
    compProtos(args.frompath, args.topath)
    print("Done generating protobuffs, results in folder: " + args.topath)

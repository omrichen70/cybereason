
from concurrent import futures
import _credentials
import grpc
import message_pb2
import message_pb2_grpc


class Decoder(message_pb2_grpc.DecoderServicer):

    def encodeMessage(self, request, response):
        return message_pb2.encodeResponse(message=encodeMe(request.message))

    def decodeMessage(self, request, response):
        return message_pb2.decodeResponse(message=decodeMe(request.message))


def encodeMe(s):
    ans = ""
    for x in s:
        ans += chr(ord(x)+5)
    return ans


def decodeMe(s):
    ans = ""
    for x in s:
        ans += chr(ord(x)-5)
    return ans


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_DecoderServicer_to_server(Decoder(), server)

    server_credentials = grpc.ssl_server_credentials(((
        _credentials.SERVER_CERTIFICATE_KEY,
        _credentials.SERVER_CERTIFICATE,
    ),))

    server.add_secure_port('localhost:50051', server_credentials)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

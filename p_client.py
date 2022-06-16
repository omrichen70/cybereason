import grpc
import message_pb2
import message_pb2_grpc
import _credentials
import contextlib


_SERVER_ADDR_TEMPLATE = 'localhost:%d'
_SIGNATURE_HEADER_KEY = 'x-signature'


class AuthGateway(grpc.AuthMetadataPlugin):

    def __call__(self, context, callback):
        """Implements authentication by passing metadata to a callback.

        Implementations of this method must not block.

        Args:
          context: An AuthMetadataContext providing information on the RPC that
            the plugin is being called to authenticate.
          callback: An AuthMetadataPluginCallback to be invoked either
            synchronously or asynchronously.
        """
        # Example AuthMetadataContext object:
        # AuthMetadataContext(
        #     service_url=u'https://localhost:50051/helloworld.Greeter',
        #     method_name=u'SayHello')
        signature = context.method_name[::-1]
        callback(((_SIGNATURE_HEADER_KEY, signature),), None)


@contextlib.contextmanager
def create_client_channel(addr):
    # Call credential object will be invoked for every single RPC
    call_credentials = grpc.metadata_call_credentials(AuthGateway(),
                                                      name='auth gateway')
    # Channel credential will be valid for the entire channel
    channel_credential = grpc.ssl_channel_credentials(
        _credentials.ROOT_CERTIFICATE)
    # Combining channel credentials and call credentials together
    composite_credentials = grpc.composite_channel_credentials(
        channel_credential,
        call_credentials,
    )
    channel = grpc.secure_channel(addr, composite_credentials)
    yield channel


def run(channel):
    stub = message_pb2_grpc.DecoderStub(channel)
    encodedMsg = ""
    msgQueue = []
    while True:
        print("1. Encode message")
        print("2. Decode message")
        print("3. Quit")
        val = input("Please choose your option:")
        if val == '1':
            msg = input("Please enter message:\n")
            encodedMsg = stub.encodeMessage(
                message_pb2.encodeRequest(message=msg))
            msgQueue.append(encodedMsg.message)
            print("Client recieved: " + encodedMsg.message)
        elif val == '2':
            if msgQueue:
                response = stub.decodeMessage(
                    message_pb2.decodeRequest(message=msgQueue.pop(0)))
                print("Client recieved: " + response.message)
            else:
                print("No messages to encode")

        elif val == '3':
            print("Disconnecting...")
            break
        else:
            print("Invalid input.")


def main():
    with create_client_channel('localhost:50051') as channel:
        run(channel)


if __name__ == '__main__':
    main()

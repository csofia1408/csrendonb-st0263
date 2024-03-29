# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import network_pb2 as network__pb2


class NodeServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendDownload = channel.unary_unary(
                '/NodeService/SendDownload',
                request_serializer=network__pb2.Message.SerializeToString,
                response_deserializer=network__pb2.Message.FromString,
                )
        self.SendUpload = channel.unary_unary(
                '/NodeService/SendUpload',
                request_serializer=network__pb2.Message.SerializeToString,
                response_deserializer=network__pb2.Message.FromString,
                )


class NodeServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendDownload(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendUpload(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NodeServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendDownload': grpc.unary_unary_rpc_method_handler(
                    servicer.SendDownload,
                    request_deserializer=network__pb2.Message.FromString,
                    response_serializer=network__pb2.Message.SerializeToString,
            ),
            'SendUpload': grpc.unary_unary_rpc_method_handler(
                    servicer.SendUpload,
                    request_deserializer=network__pb2.Message.FromString,
                    response_serializer=network__pb2.Message.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'NodeService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class NodeService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendDownload(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/NodeService/SendDownload',
            network__pb2.Message.SerializeToString,
            network__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendUpload(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/NodeService/SendUpload',
            network__pb2.Message.SerializeToString,
            network__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

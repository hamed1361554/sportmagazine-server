'''
Created on Oct 15, 2014

@author: Abi.Mohammadi
'''

from deltapy.packaging.package import Package

ZMQ_REQUEST_PROCESSOR = 'deltapy.request_processor.zmq'

class ZmqRequestProcessorPackage(Package):
    """
    A package to add message queuing way of managing requests using ZMQ.
    """

    __disable__ = True
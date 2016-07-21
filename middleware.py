# -*- coding:utf-8 -*-
#author:hjd
class CrossDomainMiddleware(object):
    def process_response(self, request, response):
        if response.get('Access-Control-Allow-Origin',None):
            return response
        else:
            response['Access-Control-Allow-Origin']='*'
            return response
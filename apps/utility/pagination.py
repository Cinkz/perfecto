from __future__ import unicode_literals

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class LinkHeaderLimitOffsetPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()

        if next_url is not None and previous_url is not None:
            link = '<{next_url}>; rel="next", <{previous_url}>; rel="prev"'
        elif next_url is not None:
            link = '<{next_url}>; rel="next"'
        elif previous_url is not None:
            link = '<{previous_url}>; rel="prev"'
        else:
            link = ''

        headers = {}
        link = link.format(next_url=next_url, previous_url=previous_url)
        if link:
            headers['Link'] = link
        if self.count:
            headers['Content-Range'] = self.count

        return Response(data, headers=headers)
        
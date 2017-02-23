#!/usr/bin/env python
# -*- encoding: utf-8 -*-

INFINITE_LATENCY = 501
cache_size = None


class endpoint(object):
    def __init__(self, datacenter_latencia, caches_latencia):
        self.datacenter_latencia = datacenter_latencia
        self.caches_latencia = caches_latencia


class cache(object):
    def __init__(self):
        self.videos = []


class request(object):
    def __init__(self, times, endpoint_id, video_id):
        self.times = times
        self.endpoint_id = endpoint_id
        self.video_id = video_id



>>>>>>> 7894362a8543dd5778f07f0dafd95e93966c773c

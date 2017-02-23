#!/usr/bin/env python
# -*- encoding: utf-8 -*-

INFINITE_LATENCY = 501
cache_size = 0
n_videos = 0
n_endpoints = 0
n_requests = 0
n_caches = 0

videos = []
endpoints = []
caches = []
requests = []

class Endpoint(object):
    def __init__(self, datacenter_latencia, caches_latencia):
        self.datacenter_latencia = datacenter_latencia
        self.caches_latencia = caches_latencia


class Cache(object):
    def __init__(self):
        self.videos = []



class Request(object):
    def __init__(self, times, endpoint_id, video_id):
        self.times = times
        self.endpoint_id = endpoint_id
        self.video_id = video_id


def read_file(filename):
    with open(filename, 'r') as fin:
        n_videos, n_endpoints, n_requests, n_caches, cache_size = [
            int(x) for x in fin.readline().split()]

        videos = [int(v) for v in fin.readline().split()]

        caches = [Cache() for x in range(n_caches)]

        endpoints = []
        for _ in range(n_endpoints):
            dc_latency, n_caches_endpoint = [int(x) for x in fin.readline().split()]
            endpoint_caches = [INFINITE_LATENCY for x in range(n_caches)]
            for _ in range(n_caches_endpoint):
                i, latency = [int(x) for x in fin.readline().split()]
                endpoint_caches[i] = latency
            endpoints.append(Endpoint(dc_latency, endpoint_caches))

        requests = []
        for _ in range(n_requests):
            video_id, endpoint_id, n_peticiones = [int(x) for x in fin.readline().split()]
            requests.append(Request(n_peticiones, endpoint_id, video_id))



def caches_ocupadas():
    count = 0
    for cache in caches:
        if len(cache.videos) != 0:
            count += 1
    return count

def write_output(filename):
    with open(filename, 'w') as fout:
        fout.write(str(caches_ocupadas()))
        for i in range(n_caches):
            cache_string = str(i)
            for video in cache.videos:
                cache_string += ' ' + str(video)
            fout.write(cache_string)


def main():
    read_file("me_at_the_zoo.in")
    write_output("me_at_the_zoo.out")

if __name__ == '__main__':
    main()

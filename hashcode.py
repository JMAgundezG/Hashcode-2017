#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys

INFINITE_LATENCY = 501

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

# class Video(object):
#     def __init__(self, id, size):
#         self.id = id
#         self.size = size


def read_file(filename):
    global cache_size
    global n_videos
    global n_endpoints
    global n_requests
    global n_caches

    global videos
    global endpoints
    global caches
    global requests

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
    ocupados = caches_ocupadas()
    with open(filename, 'w') as fout:
        fout.write(str(ocupados) + '\n')
        for i in range(ocupados):
            cache_string = str(i)
            for video in caches[i].videos:
                cache_string += ' ' + str(video)
            fout.write(cache_string + '\n')


def process():
    ultimo = 0
    for cache in caches:
        ocupado = cache_size
        for video in range(ultimo, n_videos):
            if videos[video] <= ocupado:
                cache.videos.append(video)
                ultimo = video
                ocupado -= videos[video]
            else:
                break


def main():
    read_file(sys.argv[1])
    process()
    write_output(sys.argv[2])

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys

r"""Se define para simplificar el almacenamiento de las latencias entre
endpoints y caches. De esta manera podemos simplemente usar una lista de
las latencias y almacenar las "no conexiones" como valor infinto. El valor
máximo de las latencias a caches es de 500, así que cualquier valor superior
se puede usar aquí.
"""
INFINITE_LATENCY = 501

class Endpoint(object):
    r"""Representa un endpoint. Almacena su latencia con el datacenter y
    con cada una de las cachés. Si no está conectado a la caché, el valor
    de la latencia es INFINITE_LATENCY.
    """
    def __init__(self, datacenter_latencia, caches_latencia):
        self.datacenter_latencia = datacenter_latencia
        self.caches_latencia = caches_latencia


class Cache(object):
    r"""Cada caché solo almacena los vídeos que contiene y los megabytes
    que han sido ocupados (que no llegarán a ser más de cache_size).
    Inicialmente, no contiene ningún vídeo y tiene 0MB ocupados.
    """
    def __init__(self):
        self.videos = []
        self.ocupado = 0

    def subir_video(self, video_id):
        self.videos.append(video_id)
        self.ocupado += videos[video_id]


class Request(object):
    r"""Almacena las veces que un vídeo en concreto ha sido pedido desde
    un endpoint.
    """
    def __init__(self, times, endpoint_id, video_id):
        self.times = times
        self.endpoint_id = endpoint_id
        self.video_id = video_id


def read_file(filename):
    r"""Lee el archivo de entrada filename"""

    r"""Tamaño máximo de todas las cachés"""
    global cache_size
    r"""Número de vídeos"""
    global n_videos
    r"""Número de endpoints"""
    global n_endpoints
    r"""Número de peticiones"""
    global n_requests
    r"""Número de cachés"""
    global n_caches

    r"""Lista en la cual la posición i contiene el
    tamaño en MB del vídeo i
    """
    global videos
    r"""Lista de endpoints"""
    global endpoints
    r"""Lista de cachés"""
    global caches
    r"""Lista de requests"""
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
    r"""Cuenta el número de cachés que han sido usadas (usado al
    escribir la salida)
    """
    count = 0
    for cache in caches:
        if len(cache.videos) != 0:
            count += 1
    return count

def write_output(filename):
    r"""Escribe al archivo de salida filename"""
    ocupados = caches_ocupadas()
    with open(filename, 'w') as fout:
        fout.write(str(ocupados) + '\n')
        for i in range(ocupados):
            cache_string = str(i)
            for video in caches[i].videos:
                cache_string += ' ' + str(video)
            fout.write(cache_string + '\n')


def process():
    r"""Algoritmo principal que coloca los vídeos en servidores.

    Se mantiene una lista de vídeos que ya han sido subidos (para
    asegurarse de que no se vuelven a subir).

    Para empezar, se ordenan las peticiones según la cantidad de tiempo
    que se ganaría al almacenar el vídeo pedido en la caché más rápida
    (multiplicando las veces que ha sido pedido por la diferencia
    entre la latencia del datacenter y la latencia de la caché más
    rápida para el endpoint que pide). Las peticiones se procesarán en ese
    orden.

    A partir de ahí, empezando por la mejor petición, y si el vídeo que se pide
    no ha sido almacenado todavía se busca el id de la caché más rápida para
    el endpoint que no esté llena, y se almacena el vídeo ahí.
    """
    videos_subidos = []
    sorted_requests = sorted(requests, key=lambda req: req.times * (endpoints[req.endpoint_id].datacenter_latencia - min(endpoints[req.endpoint_id].caches_latencia)), reverse=True)
    for request in sorted_requests:
        if request.video_id not in videos_subidos:
            mejor_hasta_ahora_l = INFINITE_LATENCY
            mejor_hasta_ahora = -1
            for i in range(len(endpoints[request.endpoint_id].caches_latencia)):
                if endpoints[request.endpoint_id].caches_latencia[i] < mejor_hasta_ahora_l \
                    and cache_size - caches[i].ocupado > videos[request.video_id]:
                    mejor_hasta_ahora_l = endpoints[request.endpoint_id].caches_latencia[i]
                    mejor_hasta_ahora = i
            if mejor_hasta_ahora != -1:
                caches[mejor_hasta_ahora].subir_video(request.video_id)
                videos_subidos.append(request.video_id)



def main():
    read_file(sys.argv[1])
    process()
    write_output(sys.argv[2])

if __name__ == '__main__':
    main()

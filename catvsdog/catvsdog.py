#!/usr/bin/env python

import sys
from collections import deque

class Edge(object):
    def __init__(self, from_vertex, to_vertex, weight):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = weight
        self.flow = 0
    
    def __hash__(self):
        return hash((self.from_vertex, self.to_vertex))
        
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.from_vertex == other.from_vertex and
                self.to_vertex == other.to_vertex)
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        return str(self.from_vertex) + '->' + str(self.to_vertex)
    
    def other(self, vertex):
        if self.from_vertex == vertex:
            return self.to_vertex
        return self.from_vertex
    
    def residual_capacity_to(self, vertex):
        if self.from_vertex == vertex:
            return self.flow
        elif self.to_vertex == vertex:
            return self.weight - self.flow
        raise ValueError('Invalid vertex')
    
    def add_residual_flow_to(self, vertex, delta):
        if self.from_vertex == vertex:
            self.flow -= delta
        elif self.to_vertex == vertex:
            self.flow += delta
        
class Graph(object):
    def __init__(self):
        self.edges = {}
    
    def add(self, edge):
        if not edge.from_vertex in self.edges:
            self.edges[edge.from_vertex] = set()
        self.edges[edge.from_vertex].add(edge)
    
    def adjacent(self, vertex):
        if not vertex in self.edges:
            return set()
        return self.edges[vertex]

class MaximumFlow(object):
    def __init__(self, graph, source, dest):
        self.max_flow = 0
        self.edge_to = {}
        self.marked = set()
        # Ford Fulkerson's algorithm
        while self._has_augmenting_path(graph, source, dest):
            bottleneck = sys.maxint
            v = dest
            while v != source:
                bottleneck = min(bottleneck, self.edge_to[v].residual_capacity_to(v))
                v = self.edge_to[v].other(v)
            v = dest
            while v != source:
                self.edge_to[v].add_residual_flow_to(v, bottleneck)
                v = self.edge_to[v].other(v)
            self.max_flow += bottleneck
        
    def _has_augmenting_path(self, graph, source, dest):
        self.edge_to = {}
        self.marked = set()
        queue = deque()
        queue.append(source)
        self.marked.add(source)
        while len(queue) != 0 and not dest in self.marked:
            vertex = queue.pop()
            for edge in graph.adjacent(vertex):
                other_vertex = edge.other(vertex)
                if edge.residual_capacity_to(other_vertex) > 0:
                    if not other_vertex in self.marked:
                        self.edge_to[other_vertex] = edge
                        self.marked.add(other_vertex)
                        queue.append(other_vertex)
        return dest in self.marked

def catvsdog():
    line = raw_input()
    n = int(line)
    for i in xrange(0, n):
        votes = []
        lines = raw_input().split()
        num_votes = int(lines[2])
        for j in xrange(0, num_votes):
            line = raw_input()
            votes.append(line)
        graph = Graph()
        for vote1 in votes:
            (u1, v1) = vote1.split()
            if u1[0] != 'C': continue
            for vote2 in votes:
                (u2, v2) = vote2.split()
                if u1 == v2 or u2 == v1:
                    graph.add(Edge(vote1, vote2, 1))
        for edges in graph.edges.values():
            for edge in edges:
                graph.add(Edge('start', edge.from_vertex, 1))
                graph.add(Edge(edge.to_vertex, 'end', 1))
        mf = MaximumFlow(graph, 'start', 'end')
        print num_votes - mf.max_flow
        
if __name__ == '__main__':
    catvsdog()
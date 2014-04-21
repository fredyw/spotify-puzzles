#!/usr/bin/env python

class Song(object):
    def __init__(self, quality, name):
        self.quality = quality
        self.name = name

    def __cmp__(self, other):
        # descending order
        if self.quality > other.quality: return -1
        elif self.quality == other.quality: return 0
        else: return 1

    def __str__(self):
        return str(self.quality) + " " + self.name

def parse_input():
    songs = []
    line = raw_input().split()
    n = int(line[0])
    m = int(line[1])
    for i in xrange(0, n):
        line = raw_input()
        t = line.split()
        freq = int(t[0])
        name = t[1]
        songs.append(Song(freq * (i+1), name))
    songs.sort()
    return (songs, int(m))

if __name__ == "__main__":
    (songs, m) = parse_input()
    for i in xrange(0, m):
        print songs[i].name

#!/usr/bin/env python

import timeit


def cprofile_main():
    from pymongo import Connection
    connection = Connection()
    connection.drop_database('timeit_test')
    connection.disconnect()

    from mongoengine import Document, DictField, connect
    connect("timeit_test")

    class Noddy(Document):
        fields = DictField()

    for i in xrange(1):
        noddy = Noddy()
        for j in range(20):
            noddy.fields["key" + str(j)] = "value " + str(j)
        noddy.save()


def main():
    """
    0.4 Performance Figures ...

    2.39654397964
    -------------------------------------------------------------
    Creating 10000 dictionaries - MongoEngine
    4.47843289375
    -------------------------------------------------------------
    Creating 10000 dictionaries - MongoEngine, safe=False
    3.6064119339
    """

    setup = """
from pymongo import Connection
connection = Connection()
connection.drop_database('timeit_test')
"""

    stmt = """
from pymongo import Connection
connection = Connection()

db = connection.timeit_test
noddy = db.noddy

for i in xrange(10000):
    example = {'fields': {}}
    for j in range(20):
        example['fields']["key"+str(j)] = "value "+str(j)

    noddy.insert(example)

myNoddys = noddy.find()
[n for n in myNoddys] # iterate
"""

    print "-" * 100
    print """Creating 10000 dictionaries - Pymongo"""
    t = timeit.Timer(stmt=stmt, setup=setup)
    #print t.timeit(1)

    setup = """
from pymongo import Connection
connection = Connection()
connection.drop_database('timeit_test')
connection.disconnect()

from mongoengine import Document, DictField, connect
connect("timeit_test")

class Noddy(Document):
    fields = DictField()
"""

    stmt = """
for i in xrange(10000):
    noddy = Noddy()
    for j in range(20):
        noddy.fields["key"+str(j)] = "value "+str(j)
    noddy.save()

myNoddys = Noddy.objects()
[n for n in myNoddys] # iterate
"""

    print "-" * 100
    print """Creating 10000 dictionaries - MongoEngine"""
    t = timeit.Timer(stmt=stmt, setup=setup)
    print t.timeit(1)

    return

    stmt = """
for i in xrange(10000):
    noddy = Noddy()
    for j in range(20):
        noddy.fields["key"+str(j)] = "value "+str(j)
    noddy.save(safe=False, validate=False)

myNoddys = Noddy.objects()
[n for n in myNoddys] # iterate
"""

    print "-" * 100
    print """Creating 10000 dictionaries - MongoEngine, safe=False, validate=False"""
    t = timeit.Timer(stmt=stmt, setup=setup)
    #print t.timeit(1)


    stmt = """
for i in xrange(10000):
    noddy = Noddy()
    for j in range(20):
        noddy.fields["key"+str(j)] = "value "+str(j)
    noddy.save(safe=False, validate=False, cascade=False)

myNoddys = Noddy.objects()
[n for n in myNoddys] # iterate
"""

    print "-" * 100
    print """Creating 10000 dictionaries - MongoEngine, safe=False, validate=False, cascade=False"""
    t = timeit.Timer(stmt=stmt, setup=setup)
    print t.timeit(1)

    stmt = """
for i in xrange(10000):
    noddy = Noddy()
    for j in range(20):
        noddy.fields["key"+str(j)] = "value "+str(j)
    noddy.save(force_insert=True, safe=False, validate=False, cascade=False)

myNoddys = Noddy.objects()
[n for n in myNoddys] # iterate
"""

    print "-" * 100
    print """Creating 10000 dictionaries - MongoEngine, force=True"""
    t = timeit.Timer(stmt=stmt, setup=setup)
    print t.timeit(1)

if __name__ == "__main__":
    main()

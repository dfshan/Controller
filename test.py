import db
    
angle=db.FindRoute(0xc0a80103, 0xc0a80102)
print angle
mb=db.FindMb(0xc0a80131)
print "%x" % mb
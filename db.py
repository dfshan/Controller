import MySQLdb

host='localhost'
user='root'
passwd='root'
db='opt_mb'
outTime=2   # out of date: 2s



def UpdateIpMb( mb, ipList ):
    '''
    update the ip_mb database
    the first argument is an IP Address(Integer) represent of the MB
    the second argument is an IP list represent the servers managed by MB
    '''
    
    conn = MySQLdb.connect( host=host, user=user, passwd=passwd, db=db )
    cursor = conn.cursor()
    # delete the old ip list managed by mb because it needs refreshing
    sql = r"delete from opt_mb.ip_mb where mb = %d" % mb
    cursor.execute(sql)
    
    sql=r"insert into opt_mb.ip_mb (server,mb) values( %s, %s) ON DUPLICATE KEY UPDATE mb=" + str(mb)
    values=[]
    # insert all the ipList
    for ip in ipList:
        values.append( (ip, mb) )
    cursor.executemany( sql, values )
    
    # delete the out of date tuples
    # cursor.execute( "delete from ip_mb where updated <= DATE_SUB( now(), INTERVAL %d SECOND )" % outTime )
    conn.commit()
    cursor.close()
    conn.close()
    
def FindMb( dst ):
    '''
    find the corresponding middle box with the destination( 1st argument)
    the destination is a number(e.g. unsigned long )
    
    if found, return the ip address on the integer format
    else, return 0
    '''
    
    conn = MySQLdb.connect( host=host, user=user, passwd=passwd, db=db )
    cursor = conn.cursor()
    count = cursor.execute( "select mb from ip_mb where server=%d" % dst )

    mbIp=0;
    if count==1:
        mbIp=cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return mbIp
        
        
def FindRoute( mb1, mb2 ):
    '''
    find the route information according to the ip address of src middle box(1st argument) and dst middle box(2nd argument)
    in our case, the route information is an angle
    
    if found, return the angle
    else return 0
    '''
    conn = MySQLdb.connect( host=host, user=user, passwd=passwd, db=db )
    cursor = conn.cursor()
    count = cursor.execute( "select angle from angle where mb1 = %d and mb2 = %d " % (mb1, mb2) )
    angle=0
    if( count == 1 ):
        angle=cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return angle
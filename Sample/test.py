import pymssql
conn=pymssql.connect(host='192.168.0.32', port=3307, database='test',user='leon',password='zaq12wsx')
cur=conn.cursor()
cur.execute('SELECT TOP 100 * FROM BAS_ATT')
for r in cur.fetchall():
    print '\t'.join(r).decode('gb2312').encode('utf-8')
conn.close()
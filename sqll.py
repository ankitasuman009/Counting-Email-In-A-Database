import sqlite3

conn = sqlite3.connect('sql3db.sqlite')
cur = conn.cursor()
cur.execute('drop table if exists Counts')
sqlstr = 'select * from Users'
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')


fname = 'mbox-short.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    dom = email.find('@')
    org = email[dom+1:len(email)]
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))


conn.commit()
sqlstr = 'select * from Counts ORDER BY count DESC LIMIT 10'
for row in cur.execute(sqlstr):
    sum += int(row[1])
    print(str(row[0]) , str(row[1]))
cur.close()

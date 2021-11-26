import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd

my_conn = mysql.connector.connect(
      host="localhost",
      user="admin",
      passwd="password",
      database="gorepodownloader",
      auth_plugin='mysql_native_password'
    )
####### end of connection ####

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
repositoryId = 1
df = pd.read_sql("SELECT c.author_date, c.commit_hash, tc.name, AVG(r.cpu_percent) AS 'cpu', AVG(r.mem_percent) AS 'mem', "
                 "AVG(r.write_count) AS 'disk_write', AVG(r.read_count) AS 'disk_read' FROM gorepodownloader.resources as r "
                 "inner join gorepodownloader.runs as run on r.run_id=run.id "
                 "inner join gorepodownloader.testcases as tc on run.test_case_id=tc.id "
                 "inner join gorepodownloader.files as f on tc.file_id=f.id "
                 "inner join gorepodownloader.commits as c on f.commit_id=c.id "
                 "inner join gorepodownloader.repositories as rep on c.repository_id=rep.id "
                 "where rep.id=" + str(repositoryId) + " "
                 "GROUP BY c.commit_hash, tc.name "
                 "ORDER BY tc.name, c.author_date;", my_conn)

df_title = pd.read_sql("SELECT name FROM gorepodownloader.repositories WHERE id=" + str(repositoryId), my_conn)
title = df_title.iloc[0, 0]

# print(df.columns)
# df['cpu_acc'] = df.groupby(["name", "author_date"])['name', 'author_date', 'cpu'].cumsum()
df['cpu_csum'] = df.groupby(['name'])['cpu'].cumsum()
df['mem_csum'] = df.groupby(['name'])['mem'].cumsum()
df['write_csum'] = df.groupby(['name'])['disk_write'].cumsum()
df['read_csum'] = df.groupby(['name'])['disk_read'].cumsum()
df.to_csv('cpu.csv')

cm = 1/2.54

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(40*cm, 20*cm))
fig.suptitle(title)
# fig, ax = plt.subplots(figsize=(40*cm, 20*cm))
for key, grp in df.groupby(['name']):
    ax1 = grp.plot(ax=ax1, kind='line', x='author_date', y='cpu_csum', label=key)
ax1.set_ylabel('%')
ax1.get_legend().remove()
# plt.legend(loc='best', prop={"size": 0.5})
plt.xticks(rotation=30)
plt.title('CPU Cumulative Sum')

# plt.savefig('cpu_csum.pdf')


for key, grp in df.groupby(['name']):
    ax2 = grp.plot(ax=ax2, kind='line', x='author_date', y='mem_csum', label=key)
# plt.legend(loc='best', prop={"size": 0.5})
ax2.set_ylabel('%')
ax2.get_legend().remove()
plt.xticks(rotation=30)
plt.title('Memory Cumulative Sum')
# plt.savefig('mem_csum.pdf')

# fig, ax = plt.subplots(figsize=(40*cm, 20*cm))
for key, grp in df.groupby(['name']):
    ax3 = grp.plot(ax=ax3, kind='line', x='author_date', y='write_csum', label=key)
# plt.legend(loc='best', prop={"size": 0.5})
ax3.set_ylabel('#')
ax3.get_legend().remove()
plt.xticks(rotation=30)
plt.title('Disk IO (Write) Cumulative Sum')
# plt.savefig('write_csum.pdf')

# fig, ax = plt.subplots(figsize=(40*cm, 20*cm))
for key, grp in df.groupby(['name']):
    ax4 = grp.plot(ax=ax4, kind='line', x='author_date', y='read_csum', label=key)
# plt.legend(loc='best', prop={"size": 0.5})
ax4.set_ylabel('#')
ax4.get_legend().remove()
plt.xticks(rotation=30)
plt.title('Disk IO (Read) Cumulative Sum')
fig.tight_layout()
plt.savefig(title + '.pdf')
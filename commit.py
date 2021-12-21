import matplotlib.pyplot as plt
import pandas as pd

def avg_by_commit(my_conn, repositoryId):
    plt.close("all")
    df = pd.read_sql(
        "SELECT c.author_date, c.commit_hash, AVG(r.cpu_percent) AS 'cpu', AVG(r.mem_percent) AS 'mem', "
        "AVG(r.write_count) AS 'disk_write', AVG(r.read_count) AS 'disk_read' FROM resources as r "
        "inner join runs as run on r.run_id=run.id "
        "inner join testcases as tc on run.test_case_id=tc.id "
        "inner join files as f on tc.file_id=f.id "
        "inner join commits as c on f.commit_id=c.id "
        "inner join repositories as rep on c.repository_id=rep.id "
        "where rep.id=" + str(repositoryId) + " "
                                              "GROUP BY c.commit_hash "
                                              "ORDER BY c.author_date;", my_conn)

    df_title = pd.read_sql("SELECT name FROM repositories WHERE id=" + str(repositoryId), my_conn)
    title = df_title.iloc[0, 0]

    df['cpu_chg'] = df['cpu'].pct_change()
    df['cpu_chg'].plot()
    plt.show()
    df['mem_chg'] = df['mem'].pct_change()
    df['mem_chg'].plot()
    plt.show()
    df['disk_write_chg'] = df['disk_write'].pct_change()
    df['disk_write_chg'].plot()
    plt.show()
    df['disk_read_chg'] = df['disk_read'].pct_change()
    df['disk_read_chg'].plot()
    plt.show()
    df.to_csv('results/avg_by_commit.csv')


def _by_commit(my_conn, repositoryId):
    plt.close("all")
    df = pd.read_sql(
        "SELECT c.author_date, c.commit_hash, AVG(r.cpu_percent) AS 'cpu', AVG(r.mem_percent) AS 'mem', "
        "AVG(r.write_count) AS 'disk_write', AVG(r.read_count) AS 'disk_read' FROM resources as r "
        "inner join runs as run on r.run_id=run.id "
        "inner join testcases as tc on run.test_case_id=tc.id "
        "inner join files as f on tc.file_id=f.id "
        "inner join commits as c on f.commit_id=c.id "
        "inner join repositories as rep on c.repository_id=rep.id "
        "where rep.id=" + str(repositoryId) + " "
                                              "GROUP BY c.commit_hash "
                                              "ORDER BY c.author_date;", my_conn)

    df_title = pd.read_sql("SELECT name FROM repositories WHERE id=" + str(repositoryId), my_conn)
    title = df_title.iloc[0, 0]

    df['cpu_chg'] = df['cpu'].pct_change()
    df['cpu_chg'].plot()
    plt.show()
    df['mem_chg'] = df['mem'].pct_change()
    df['mem_chg'].plot()
    plt.show()
    df['disk_write_chg'] = df['disk_write'].pct_change()
    df['disk_write_chg'].plot()
    plt.show()
    df['disk_read_chg'] = df['disk_read'].pct_change()
    df['disk_read_chg'].plot()
    plt.show()
    df.to_csv('results/avg_by_commit.csv')
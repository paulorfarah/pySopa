import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd

from commit import avg_by_commit
from testcase import testcases

my_conn = mysql.connector.connect(
      host="localhost",
      user="admin",
      passwd="password",
      database="gorepoownloader",
      auth_plugin='mysql_native_password'
    )
####### end of connection ####

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
repositoryId = 1

# testcases(my_conn, repositoryId)

avg_by_commit(my_conn, repositoryId)

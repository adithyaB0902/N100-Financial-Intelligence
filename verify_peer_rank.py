import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    pg.company_id,
    fr.return_on_equity_pct,
    pp.percentile_rank
FROM peer_percentiles pp
JOIN financial_ratios fr
    ON pp.company_id = fr.company_id
   AND pp.year = fr.year
JOIN peer_groups pg
    ON pp.company_id = pg.company_id
WHERE
    pg.peer_group_name = 'IT Services'
    AND pp.metric = 'return_on_equity_pct'
ORDER BY fr.return_on_equity_pct DESC;
"""

df = pd.read_sql(query, conn)

print("\nIT Services Peer Ranking\n")
print(df)

conn.close()
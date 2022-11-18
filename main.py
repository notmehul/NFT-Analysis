import sqlite3
import pandas as pd 
import networkx as nx 
from pyvis.network import Network

# connecting db
con = sqlite3.connect("nfts.sqlite")
cur = con.cursor()


#getting a list of top 5 projects
#getting volume of transfers and sorting
#divided by 1e18 to make numbers smaller from db
df1 = pd.read_sql_query(""" SELECT name, nft_address, SUM(transaction_value/1e18), AS volume
FROM transfers
INNER JOIN nfts ON transfers.nft_address = nfts.address 

GROUP BY transfers.nft_address

ORDER BY volume DESC

""", con)

conract_names_dict = dict(zip(df1.nft_address, df1.name)) #contract addresses
contracts = tuple(contract_names_dict_keys()) 

#list of all the project names and addresses
all_project_names = pd.read_sql_query(""" 
SELECT * 
FROM nfts
LIMIT 100000
""", con)

# dictionary here but that dude said he didnt need so 
# contract_names_dict_all

#top nft owners which are in the top 5 (contracts)
# the {} points to the contracts tuple which has all the top 5
#basically top 3 people who own all five of the top NFTs(actual whales lol)
top_n_owners_list = pd.read_sql_query(""" 
SELECT count(DISCTINCT nft_address) AS num_projects, owner
FROM current_owners
WHERE nft_address IN {}


GROUP BY owner
ORDER BY num_projects DESC

LIMIT 3

""".format(contracts), con)

#create tuple for the big owners
owners_tuples = tuple(top_n_owners_list['owner'])

#see what all do the big owners own
# and show them collectively
top_projects = pd.read_sql_query(""" select nft_address, count(owner) as count
from current_owners

where owner in {}

group by nft_address 
order by count desc

limit 50000""".format(owners_tuples), con)


top_projects_tuple = tuple(top_projects['nft_address'])

#getting all the nfts of top projects
all_nfts_in_top_projects = pd.read_sql_query("""
select * from current owners
where nft_address in {}
""".format(top_projects_tuple), con)


#edgy table

#shows the amount of nft projects have common owners
#example nft1 and nf2 are owned by 50 people
edge_table = pd.read_sql_query("""
select t1.nft_address as nft1, t2.nft_address  as nft2, count(*) as count
from current_owners as t1

inner join current_owners as t2
on t1.owner = t2.owner

where t1.owner in {}
and
nft1 > nft2
group by nft1, nft2

having count(*) > 50
""".format(owners_tuples), con)



















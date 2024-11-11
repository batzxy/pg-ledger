# pg-ledger
Make a ledger in POSTGRES which can be used to visualize in Grafana later on


## Steps:
1. Ensure a virtual environment is made.

2. Make a CSV file (like the one shown as example below) containing those headers and data:
```
Date,Reason,Amount,Credit,Category
2024-10-01,Phone,59.99,FALSE,Bills
2024-10-01,Salary,100,TRUE,Income
```

3. Run the `pusher.py` with changes in the script.

4. Ready for Grafana to visualize the DB data.

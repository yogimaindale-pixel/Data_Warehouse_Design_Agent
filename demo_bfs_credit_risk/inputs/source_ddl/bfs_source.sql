
CREATE TABLE borrowers (
    borrower_id VARCHAR(64) PRIMARY KEY,
    borrower_name VARCHAR(100),
    ssn VARCHAR(20),
    credit_score INT,
    risk_rating VARCHAR(10)
);

CREATE TABLE account_snapshots (
    account_id VARCHAR(64),
    borrower_id VARCHAR(64) REFERENCES borrowers(borrower_id),
    snapshot_date DATE,
    principal_balance NUMERIC(15,2),
    accrued_interest NUMERIC(15,2),
    delinquent_days INT,
    PRIMARY KEY (account_id, snapshot_date)
);

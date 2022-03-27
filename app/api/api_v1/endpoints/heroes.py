from fastapi import APIRouter
import json
import boto3

router = APIRouter()

rds_client = boto3.client('rds-data')

database_name = 'heroesteams'
db_cluster_arn= 'arn:aws:rds:us-east-1:336697874233:cluster:heroes-and-teams'
db_credentials_secrets_store_arn = 'arn:aws:secretsmanager:us-east-1:336697874233:secret:rds-db-credentials/cluster-XE7U2FG4AIEOYAKPQP52I4UPD4/itnas-GRMog0'


@router.get("/")
async def root():
    response = execute_statement('SELECT * FROM Heroes');
    return(response)

def execute_statement(sql):
    response = rds_client.execute_statement(
        secretArn= db_credentials_secrets_store_arn,
        database=database_name,
        resourceArn=db_cluster_arn,
        sql=sql
        )
    return(response)
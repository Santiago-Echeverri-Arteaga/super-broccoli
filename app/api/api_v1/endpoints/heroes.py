from fastapi import APIRouter
import json
import boto3
##
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
##
router = APIRouter()

rds_client = boto3.client('rds-data')

database_name = 'heroesteams'
db_cluster_arn= 'arn:aws:rds:us-east-1:336697874233:cluster:heroes-and-teams'
db_credentials_secrets_store_arn = 'arn:aws:secretsmanager:us-east-1:336697874233:secret:rds-db-credentials/cluster-XE7U2FG4AIEOYAKPQP52I4UPD4/itnas-GRMog0'

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str


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
    names = []
    for i in range(len(response["records"])):
        names.append(response["records"][i][0]["stringValue"])
    return(names)

@router.get("/crear")
async def create_heroe(): 
    sql = """
        INSERT INTO Heroes
        (name, secret_name, age, team, clasificacion, casa)
        VALUES(:nombre, :real, :edad, :equipo, :heroe_villano, :DC_Marvel)
        """
    param1 = {'name':'nombre', 'value':{'stringValue': 'Capitan America'}}
    param2 = {'name':'real', 'value':{'stringValue': 'Steve Rogers'}}
    param3 = {'name':'edad', 'value':{'longValue': 45}}
    param4 = {'name':'equipo', 'value':{'stringValue': 'Avengers'}}
    param5 = {'name':'heroe_villano', 'value':{'stringValue': 'Heroe'}}
    param6 = {'name':'DC_Marvel', 'value':{'stringValue': 'Marvel'}}

    param_set = [param1, param2, param3, param4, param5, param6]

    response = rds_client.execute_statement(
        secretArn= db_credentials_secrets_store_arn,
        database=database_name,
        resourceArn=db_cluster_arn,
        sql = sql,
        parameters = param_set)
    return(response)
    

@router.get("/select/{age}")
async def review_heroe(age: str): 
    # sql = f"""
    #     SELECT name FROM Heroes WHERE
    #     name <= \'{age}\'
    #     """
    # response = rds_client.execute_statement(
    #    secretArn= db_credentials_secrets_store_arn,
    #    database=database_name,
    #    resourceArn=db_cluster_arn,
    #    sql = sql)
    # return(response["records"])
    db_proxy_endpoint="heroes-and-teams.cluster-c0zdmisqyfrx.us-east-1.rds.amazonaws.com"
    sqlite_file_name = "database.db"
    port=5432
    db_name="heroesteams"
    sqlite_url = f"postgresql://itnas:S5a4n.t7i1@{db_proxy_endpoint}:{port}/{db_name}?sslmode=require"


    engine = create_engine(sqlite_url, echo=True)
    print("Los heroes son")
    with Session(engine) as session:
        statement = select(Hero).join(Team)
        results = session.exec(statement)
        for hero in results:
            print("Hero:", hero)


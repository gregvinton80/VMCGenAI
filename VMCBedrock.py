from langchain.llms.bedrock import Bedrock
from langchain_experimental.sql import SQLDatabaseChain
from langchain.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine


#DB Variables
connathena=f"athena.REGION.amazonaws.com"
portathena='443' #Update, if port is different
schemaathena='DBNAME' #from cfn params
s3stagingathena=f's3://URL'#from cfn params
wkgrpathena='primary'#Update, if workgroup is different
connection_string = f"awsathena+rest://@{connathena}:{portathena}/{schemaathena}?s3_staging_dir={s3stagingathena}/&work_group={wkgrpathena}"
engine_athena = create_engine(connection_string, echo=False)
db = SQLDatabase(engine_athena)


# setup llm
llm = Bedrock(model_id="ai21.j2-ultra-v1", model_kwargs={"maxTokens": 1024,"temperature": 0.0})

# Create db chain
QUERY = """
create a syntactically correct postgresql query to run based on the question, then look at the results of the query and return the answer with some verbage added in.

{question}
"""

# Setup the database chain
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)


def get_prompt():
    print("Type 'exit' to quit")

    while True:
        prompt = input("Ask me a Question: ")

        if prompt.lower() == 'exit':
            print('Exiting...')
            break
        else:
            try:
                question = QUERY.format(question=prompt)
                print(db_chain.run(question))
            except Exception as e:
                print(e)

get_prompt()

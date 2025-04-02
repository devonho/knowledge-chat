import os
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts.prompt import PromptTemplate

from langchain_core.tools import tool

graph = Neo4jGraph(
    url=os.environ["NEO4J_URI"],
    username=os.environ["NEO4J_USERNAME"],
    password=os.environ["NEO4J_PASSWORD"],
    enhanced_schema=True,
)

CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.
Examples: Here are a few examples of generated Cypher statements for particular questions:
# Who had previously worked for IBM?
MATCH (p:Person)-[r:WORKED_AT]->(c:Company {{companyName: 'IBM'}})
RETURN p,r,c

# Who is skilled in Linux?
MATCH (p:Person)-[r:HAS_SKILL]->(s:Skill {{skillName: 'Linux'}})
RETURN p,r,s

# Who is skilled in Linux and SQL?
MATCH (p:Person)-[r:HAS_SKILL]->(s:Skill {{skillName: 'Linux'|'SQL'}}))
RETURN p,r,s


The question is:
{question}"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)

chain = GraphCypherQAChain.from_llm(
    ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.1), 
    graph=graph, 
    verbose=True, 
    cypher_prompt=CYPHER_GENERATION_PROMPT,
    allow_dangerous_requests=True
)

@tool
def search_resume_graph_database(query):
    """search resume database for persons with particular skills or certifications or work experience at particular companies"""
    return chain.invoke({"query": query})

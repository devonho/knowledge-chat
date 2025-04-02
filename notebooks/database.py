import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

class MyGraphDB:
    def __init__(self):
        load_dotenv()
        uri = os.environ["NEO4J_URI"]
        username = os.environ["NEO4J_USERNAME"]
        password = os.environ["NEO4J_PASSWORD"]
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def add_person(self, name, email, id):
        try:
            with self.driver.session() as session:
                session.execute_write(lambda tx: tx.run("""
                    CREATE (n:Person)
                    SET n.name = $name, n.id = $id, n.email = $email
                """, name=name, id=id, email=email))
        except Exception as e:
            print(e)

    def add_company(self, company_name):
        try:
            with self.driver.session() as session:
                session.execute_write(lambda tx: tx.run("""
                    CREATE (n:Company)
                    SET n.companyName = $company_name
                """, company_name=company_name))
        except Exception as e:
            print(e)

    def add_skill(self, skill_name):
        try:
            with self.driver.session() as session:
                session.execute_write(lambda tx: tx.run("""
                    CREATE (n:Skill)
                    SET n.skillName = $skill_name
                """, skill_name=skill_name))
        except Exception as e:
            print(e)

    def add_certification(self, title):
        try:
            with self.driver.session() as session:
                session.execute_write(lambda tx: tx.run("""
                    CREATE (n:Certification)
                    SET n.title = $title
                """, title=title))
        except Exception as e:
            print(e)

    def add_WORKED_AT_rel(self, personId, companyName, roleName, startDate, endDate):
        try:
            with self.driver.session() as session:
                session.execute_write(lambda tx: tx.run("""
                    MATCH (p:Person {id: $id }),(c:Company {companyName: $companyName })
                    CREATE (p)-[:WORKED_AT {roleName: $roleName, startDate: date($startDate), endDate: date($endDate)}]->(c)
                """, id=personId, companyName=companyName, roleName=roleName, startDate=startDate, endDate=endDate))
        except Exception as e:
            print(e)

    def add_HAS_SKILL_rel(self, personId, skillName):
        try:
            with self.driver.session() as session:
                session.execute_write(lambda tx: tx.run("""
                    MATCH (p:Person {id: $id }),(s:Skill {skillName: $skillName })
                    CREATE (p)-[:HAS_SKILL]->(s)
                """, id=personId, skillName=skillName))
        except Exception as e:
            print(e)

    def add_HAS_CERTIFICATION_rel(self, personId, title, startDate):
        try:
            with self.driver.session() as session:
                session.execute_write(lambda tx: tx.run("""
                    MATCH (p:Person {id: $id }),(c:Certification {title: $title})
                    CREATE (p)-[:HAS_CERTIFICATION {startDate: date($startDate)}]->(c)
                """, id=personId, title=title, startDate=startDate))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    db = MyGraphDB()
    db.add_company("Bosch")
    db.add_company("Philips")
    db.add_person("Foobar", "foo@bar.com", "123")
    db.add_person("Farcar", "far@car.com", "456")
    db.add_skill("VSCode")
    db.add_skill("Python")
    db.add_certification("Diploma")
    db.add_certification("Degree")
    db.add_WORKED_AT_rel("123","Bosch", "Janitor", "2016-01-01", "2025-01-01")
    db.add_HAS_SKILL_rel("123","VSCode")
    db.add_HAS_CERTIFICATION_rel("123","Diploma","2025-01-01")
    db.add_WORKED_AT_rel("456","Bosch", "Manager", "2016-01-01", "2025-01-01")
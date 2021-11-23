from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import os
import uuid
import pandas as pd
from py2neo.matching import *


g = Graph(auth=('neo4j','test'))
graph = g.begin()


class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        nodes = NodeMatcher(g)
        user = nodes.match("User",username=self.username).first()
        return user

    def register(self, password):
        password=bcrypt.encrypt(password)
        if not self.find():
            user = """
            merge (a:User {username: "%s", password: "%s"})
            """%(self.username,password)
            g.run(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def add_post(self, title, tags, text, device):
        user = self.find()

        idn = uuid.uuid4()
        
        post = """
        merge (n:%s {id: "%s", title: "%s", text: "%s", timestamp: %s, date: "%s"})
        """%('Post',idn, title,text,timestamp(),date())
        
        g.run(post)
        
        if device != 'None':
            query="""
            match (a:%s {name: '%s'}),(b:%s {id: '%s'}) merge (a)-[r:%s {name:'%s'}]->(b)
            """%('device',device,'Post',idn,'insight','insight')

            g.run(query)

        rel="""
        match (a:%s {username: "%s", password: "%s"}),(b:%s {id: "%s"}) merge (a)-[r:%s]->(b)
        """%('User',user['username'],user['password'],'Post',idn,'PUBLISHED')

        g.run(rel)

        
        tags = [x.strip() for x in tags.lower().split(',')]
        for name in set(tags):
            tag = """
            merge (n:%s {name: '%s'})
            """%('Tag',name)
            g.run(tag)
            
            rel2="""
            match (a:%s {name: "%s"}),(b:%s {id: "%s"}) merge (a)-[r:%s]->(b)
            """%('Tag',name,'Post',idn,'TAGGED')

            g.run(rel2)

            

    def get_recent_posts(self):
        query = '''
        MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
        WHERE user.username = $username
        RETURN post, COLLECT(tag.name) AS tags
        ORDER BY post.timestamp DESC LIMIT 5
        '''

        return g.run(query, username=self.username)

    def get_similar_users(self):
        # Find three users who are most similar to the logged-in user
        # based on tags they've both blogged about.
        query = '''
        MATCH (you:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
              (they:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        WHERE you.username = $username AND you <> they
        WITH they, COLLECT(DISTINCT tag.name) AS tags
        ORDER BY SIZE(tags) DESC LIMIT 3
        RETURN they.username AS similar_user, tags
        '''

        return g.run(query, username=self.username)

    # def get_commonality_of_user(self, other):
    #     # Find how many of the logged-in user's posts the other user
    #     # has liked and which tags they've both blogged about.
    #     query = '''
    #     MATCH (they:User {username: {they} })
    #     MATCH (you:User {username: {you} })
    #     OPTIONAL MATCH (they)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
    #                    (you)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
    #     RETURN SIZE((they)-[:LIKED]->(:Post)<-[:PUBLISHED]-(you)) AS likes,
    #            COLLECT(DISTINCT tag.name) AS tags
    #     '''

    #     return graph.run(query, they=other.username, you=self.username).next

def get_todays_recent_posts():
    query = '''
    MATCH (user:User)-[]->(post:Post)<-[]-(tag:Tag)
    RETURN user.username AS username, post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT 10
    '''

    return g.run(query)

def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()

def date():
    return datetime.now().strftime('%Y-%m-%d')


def get_nodes_edges():

    limit= 100

    options = {"User": "username", "Post": "title", "Tag": "name"}
    
    query = """
    MATCH (n)
    WITH n, rand() AS random
    ORDER BY random
    LIMIT %s
    OPTIONAL MATCH (n)-[r]->(m)
    RETURN n AS source_node,
        id(n) AS source_id,
        r,
        m AS target_node,
        id(m) AS target_id
    """%(limit)

    data = g.run(query)

    nodes = []
    edges = []

    def get_vis_info(node, id):
        node_label = list(node.labels)
        prop_key = options.get(node_label[0])
        vis_label = node.get(prop_key, "")

        return {"id": id, "label": vis_label, "group": node_label, "title": repr(node)}

    for row in data:
        source_node = row[0]
        source_id = row[1]
        rel = row[2]
        target_node = row[3]
        target_id = row[4]

        source_info = get_vis_info(source_node, source_id)

        if source_info not in nodes:
            nodes.append(source_info)

        if rel is not None:
            target_info = get_vis_info(target_node, target_id)

            if target_info not in nodes:
                nodes.append(target_info)

            edges.append({"from": source_info["id"], "to": target_info["id"],
                        "label": str(rel).split(' ')[0].split(':')[1]})

    return nodes, edges



def get_posts():
    query='match (n:Post) return n.date as Date, n.title as `Post Title`, n.text as Content'
    d = g.run(query).to_data_frame().to_dict(orient='records')

    headers = []
    rows = []
    for m in d:
        if list(m.keys()) not in headers:    
            headers.append(list(m.keys()))
        rows.append(list(m.values()))
    if len(headers)!=0:
        headers = headers[0]
    else:
        headers = ['Date','Post Title','Content']
    

    return headers,rows



def get_devices():
    query="""
    match (a:device) return a.name as devices
    """
    devices = g.run(query).to_data_frame().squeeze().tolist()

    devices.append('None')

    return devices


def get_labels():
    labels_list=['All','device','website','provider','plan_name','DD']
    orient = ['NATURAL','REVERSE','UNDIRECTED']
    return labels_list,orient


def get_algo():
    algo_list=['PageRank']
    
    return algo_list


def run_algo(algo):
    if algo == 'PageRank':
        idn = uuid.uuid4()
        query1="""
            call gds.graph.create('%s',['device','website','provider','plan_name','DD'],{
                offered: {
                    orientation: 'UNDIRECTED'
                },
                offers: {
                        orientation: 'UNDIRECTED'
                },
                digital_demand: {
                        orientation: 'UNDIRECTED'
                }
                })
            """%(idn)

        g.run(query1)

        query2="""
        call gds.pageRank.write('%s', {writeProperty: 'pageRank'})
        """%(idn)
        g.run(query2)


def pagerank_table():
    query="""
    MATCH (t)
        where t.pageRank is not NULL
        RETURN t.name as Node, t.pageRank as PageRank
        ORDER BY t.pageRank DESC LIMIT 10
    """

    d = g.run(query).to_data_frame().to_dict(orient='records')

    headers = []
    rows = []
    for m in d:
        if list(m.keys()) not in headers:    
            headers.append(list(m.keys()))
        rows.append(list(m.values()))
    if len(headers)!=0:
        headers = headers[0]
    else:
        headers = ['Node','PageRank']
    

    return headers,rows
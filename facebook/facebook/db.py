import psycopg2

conn_str = "dbname='facebook_comments' user='postgres'" # Might want to change this

def truncate(value: str, length: int) -> str:
    if len(value) > length:
        return value[:length] + "..."
    
    return value


class db:
    def __init__(self):
        self.connection = psycopg2.connect(conn_str)
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()
    
    def rollback(self):
        self.connection.rollback()
    
    def get_highest_cn(self) -> int:
        self.cursor.execute("""SELECT highest FROM comment_number ORDER BY highest DESC LIMIT 1""")
        return self.cursor.fetchone()[0]
    
    def update_highest_cn(self, new_highest: int):
        self.cursor.execute("""INSERT INTO comment_number (highest) VALUES ({});""".format(new_highest))
        self.commit()
    
    def save_comment(self, comment_data: dict, supplier_id: int) -> int:
        user_id = self.save_user(comment_data)
        comment_id = self.save_comment_details(user_id, supplier_id, comment_data)
        self.commit()
        return comment_id

    def save_like(self, user_data: dict, supplier_id: int):
        user_id = self.save_user(user_data)
        self.save_like_details(user_id, supplier_id)
        self.commit()

    def save_user(self, comment_data: dict) -> int:
        name = truncate(comment_data["name"], 150)
        link = truncate(comment_data["link"], 900)
        uid = 0

        if "uid" in comment_data:
            uid = comment_data["uid"]

        self.cursor.execute("""
        INSERT INTO users (name, link, uid)
        VALUES(%s, %s, %s)
        ON CONFLICT (name, link) DO UPDATE SET name = %s
        RETURNING id;""", (name, link, uid, name))
        self.commit()
        return self.cursor.fetchone()[0]

    def save_comment_details(self, user_id: int, supplier_id: int, comment_data: dict) -> int:
        comment = truncate(comment_data["comment"], 5000)

        # Probably non need to store the entirety of very long comments in the database

        tagged = comment_data["tagged"]
        self.cursor.execute("""
        INSERT INTO comments (user_id, supplier_id, comment, timestamp, tagged, cid)
        VALUES (%s, %s, %s, to_timestamp(%s), %s, %s)
        ON CONFLICT (user_id, comment, timestamp) DO UPDATE SET tagged = %s RETURNING id;
        """, (user_id, supplier_id, comment, comment_data["timestamp"], tagged, comment_data["cid"], tagged))
        self.commit()
        return self.cursor.fetchone()[0]

    def save_like_details(self, user_id: int, supplier_id: int):
        self.cursor.execute("""
        INSERT INTO likes (user_id, supplier_id)
        VALUES (%s, %s)
        ON CONFLICT (user_id, supplier_id) DO NOTHING;
        """, (user_id, supplier_id))
    
    def save_supplier(self, supplier_name, page_id) -> int:
        self.cursor.execute("""
        INSERT INTO suppliers (name, page_id)
        VALUES(%s, %s)
        ON CONFLICT (name, page_id) DO UPDATE SET name = %s
        RETURNING id;""", (supplier_name, page_id, supplier_name))
        self.commit()
        return self.cursor.fetchone()[0]

    def get_suppliers(self) -> dict:
        self.cursor.execute("""SELECT id, name, page_id FROM suppliers""")
        return self.cursor.fetchall()

    def save_meta_comment(self, comment_id: int, meta_comment: dict):
        user_id = self.save_user(meta_comment)
        self.save_meta_commenter(user_id, comment_id, meta_comment)
        self.commit()

    def save_meta_commenter(self, user_id: int, comment_id: int, meta_comments):
        for comment in meta_comments["comments"]:
            self.cursor.execute("""
            INSERT INTO meta_comments (user_id, comment_id, comment, info, mcid) 
            VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
            """, (user_id, comment_id, truncate(comment["comment"], 900), truncate(str(comment["info"]), 1900), comment["id"]))
    
    def save_reactions(self, comment_id: int, reactions: dict):
        for reaction in reactions:
            user_id = self.save_user(reaction["user_details"])
            self.cursor.execute("""
            INSERT INTO reactions (user_id, comment_id, kind) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;
            """, (user_id, comment_id, reaction["kind"]))
        self.commit()

    def get_meta_comment_by_mcid(self, mcid: str) -> int:
        self.cursor.execute("""
        SELECT id FROM meta_comments WHERE mcid = %s;
        """, [mcid])
        return self.cursor.fetchone()[0]

    def save_meta_reactions(self, mcid: str, reactions: dict):

        meta_comment_id = self.get_meta_comment_by_mcid(mcid)

        for reaction in reactions:
            user_id = self.save_user(reaction["user_details"])
            self.cursor.execute("""
            INSERT INTO meta_reactions (user_id, meta_comment_id, kind) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;
            """, (user_id, meta_comment_id, reaction["kind"]))
        self.commit()
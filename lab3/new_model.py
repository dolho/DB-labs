import psycopg2
from datetime import date
import time
from hashlib import md5
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import all_tables
from sqlalchemy import exc


class DBHandler_ORM:

    def __init__(self, user, password, database):
        engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/{database}')
        Session = sessionmaker(bind=engine)
        self._session = Session()
        self.table_classes = {"user": all_tables.User, "question": all_tables.Question,
                         "answer": all_tables.Answer, "tag": all_tables.Tag}

    def add_new_instanse(self, instance: all_tables):
        self._session.add(instance)

    def delete_instance(self, instanse, id):
        res = self._session.query(instanse).filter(instanse.id == id).all()
        if res:
            self._session.query(instanse).filter(instanse.id == id).delete()
            return True
        else:
            return False

    def delete_user(self, email):
        user = self._session.query(all_tables.User).filter(all_tables.User.email == email).all()
        if user:
            self._session.query(all_tables.User).filter(all_tables.User.email == email).delete()
            return True
        else:
            return False

    def update_instance(self, instance: all_tables, id: int, new_values: dict):
        res = self._session.query(instance).filter(instance.id == id).all()
        if res:
            self._session.query(instance).filter(instance.id == id).update(new_values)
            return True
        else:
            return False

    def update_user(self, email, new_values: dict):
        user = self._session.query(all_tables.User).filter(all_tables.User.email == email).all()
        if user:
            self._session.query(all_tables.User).filter(all_tables.User.email == email).update(new_values)
            return True
        else:
            return False

    def commit_changes(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()


class DataBaseHandler:

    def __init__(self, user, password, host, database):
        try:
            self._connection = psycopg2.connect(user=user,
                                                password=password,
                                                host=host,
                                                database=database)

            self._cursor = self._connection.cursor()
            self._ORMHandler = DBHandler_ORM(user, password, database)
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            self.close_db_connection()
        except exc.SQLAlchemyError as e:
            print(e)

    def close_db_connection(self):
        """closing database connection."""
        if self._connection:
            self._cursor.close()
            self._connection.close()
            print("PostgreSQL connection is closed")

    def add_random_questions(self, user_email, quantity_of_added_questions: int = 1):
        """
            Adds given number of records to the Question table with random
            25 characters length string
        """
        try:
            # added_ids = []
            for _ in range(quantity_of_added_questions):
                self._cursor.execute(f'insert into \"Question\" (\"text\", rating, user_email, date) '
                                     f'values (substr(md5(random()::text), 0, 25), random()*100, \'{user_email}\', (select timestamp \'2014-01-10 20:00:00\' +'
                                     f'random() * (timestamp \'2020-01-20 20:00:00\' -'
                                     f'timestamp \'2014-01-10 10:00:00\')));')
                # added_ids.append(self._cursor.fetchone()[0])
            self._connection.commit()

        except (Exception, psycopg2.Error) as error:
            self._connection.rollback()
            print("Error in function add_random_questions(): ", error)

    def get_all_users_questions(self, user_email):
        try:
            self._cursor.execute(f'select * from \"Question\" where user_email=\'{user_email}\';')
            return self._cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            self._connection.rollback()
            print("Error in function get_all_users_questions(): ", error)

    def login_to_the_system(self, email, password: str) -> bool:
        """
        Returns true if pair (email, password) correct and false
        if pair doesn't exist or invalid
        """
        try:
            self._cursor.execute(f'SELECT * FROM \"Users\" '
                                 f'WHERE email=\'{str(email)}\' and password=\'{str(password)}\'')
            if self._cursor.fetchone():
                return True
            else:
                return False
        except (Exception, psycopg2.Error) as error:
            self._connection.rollback()
            print("Error in function login_to_the_system(): ", error)

    def add_random_answers(self, user_email, quantity_of_added_answers, min_id, max_id):
        """
            Adds given number of records to the Answer table with random
            25 characters length string

            It chooses random question between 10^5...2*10^5. It could work incorrectly
            if some lines would be deleted in this diapason
        """
        try:
            # added_ids = []
            for _ in range(quantity_of_added_answers):
                self._cursor.execute(f'insert into \"Answer\" (\"text\", rating, user_email, question_id) '
                                     f'values (substr(md5(random()::text), 0, 25), random()*100, \'{user_email}\', '
                                     f'random()*({min_id - max_id}) + {min_id});')
                # added_ids.append(self._cursor.fetchone()[0])
            self._connection.commit()

        except (Exception, psycopg2.Error) as error:
            self._connection.rollback()
            print("Error in function add_random_answers(): ", error)

    def add_random_tags(self, quantity_of_added_tags):
        """
                    Adds given number of records to the tags table with random
                    25 characters length string
                """
        try:
            # added_ids = []
            for _ in range(quantity_of_added_tags):
                self._cursor.execute(f'insert into \"Tag\" (\"tag\", \"references\") '
                                     f'values (substr(md5(random()::text), 0, 25), 0);')
                # added_ids.append(self._cursor.fetchone()[0])
            self._connection.commit()

        except (Exception, psycopg2.Error) as error:
            self._connection.rollback()
            print("Error in function add_random_tags(): ", error)

    def add_random_bound_question_tag(self, quantity_of_bounds, min_id_question, min_id_tag, max_id_question, max_id_tag):

        try:
            for _ in range(quantity_of_bounds):
                self._cursor.execute(f'select random()*{max_id_question - min_id_question}')
                q1 = int(self._cursor.fetchone()[0] + min_id_question)
                self._cursor.execute(f'select random()*({max_id_tag - min_id_tag})')
                t1 = int(self._cursor.fetchone()[0] + min_id_tag)
                self._cursor.execute(f' '
                                     f'insert into \"Question/Tag\" (question_id, tag_id) '
                                     f'values ({q1}, {t1});')
                self._cursor.execute(f'update \"Tag\" set "references"=("references"+1) where "id"={t1}')
            self._connection.commit()

        except (Exception, psycopg2.Error) as error:
            self._connection.rollback()
            print("Error in function add_random_tag_bounds(): ", error)

    def max_id_in_question(self):
        self._cursor.execute(f'SELECT MAX(id) FROM \"Question\" WHERE id is not null ')
        maximum = self._cursor.fetchone()[0]
        return maximum

    def min_id_in_question(self):
        self._cursor.execute(f'SELECT MIN(id) FROM \"Question\" WHERE id is not null ')
        minimum = self._cursor.fetchone()[0]
        return minimum

    def max_id_in_tag(self):
        self._cursor.execute(f'SELECT MAX(id) FROM \"Tag\" WHERE id is not null ')
        maximum = self._cursor.fetchone()[0]
        return maximum

    def min_id_in_tag(self):
        self._cursor.execute(f'SELECT MIN(id) FROM \"Tag\" WHERE id is not null ')
        minimum = self._cursor.fetchone()[0]
        return minimum

    def add_new_user(self, email, nickname, login, password, role="User"):
        try:
            user = all_tables.User(email, nickname, 0, role, login, password)
            self._ORMHandler.add_new_instanse(user)
            self._ORMHandler.commit_changes()
            return "True"
        except exc.SQLAlchemyError as error:
            self._ORMHandler.rollback()
            print(error)
            return "False"

    def update_user(self, email, nickname, login, password, role="User"):
        try:
            res = self._ORMHandler.update_user(email, {"email": email, "nickname": nickname,
                                                 "login": login, "password": password,
                                                 "role": role})
            self._ORMHandler.commit_changes()
            if res:
                return "True"
            else:
                return "False"
        except exc.SQLAlchemyError as error:
            self._ORMHandler.rollback()
            print(error)
            return "False"

    def delete_user(self, email) -> str:
        try:
            self._ORMHandler.delete_user(email)
            self._ORMHandler.commit_changes()
            return "True"
        except exc.SQLAlchemyError as error:
            self._ORMHandler.rollback()
            print(error)
            return "False"

    def add_new_question(self, user_email, question_text: str):
        try:
            question = all_tables.Question(question_text, 0, user_email)
            self._ORMHandler.add_new_instanse(question)
            self._ORMHandler.commit_changes()
            return "True"
        except exc.SQLAlchemyError as error:
            self._ORMHandler.rollback()
            print(error)
            return "False"

    def update_question(self, question_id, new_text):
        try:
            res = self._ORMHandler.update_instance(all_tables.Question, question_id,
                                             {"text": new_text})
            self._ORMHandler.commit_changes()
            if res:
                return "True"
            else:
                return "False"
        except exc.SQLAlchemyError as error:
            self._ORMHandler.rollback()
            print(error)
            return "False"

    def delete_question(self, question_id) -> bool:
        try:
            res = self._ORMHandler.delete_instance(all_tables.Question, question_id)
            self._ORMHandler.commit_changes()
            if res:
                return "True"
            else:
                return "False"
        except exc.SQLAlchemyError as error:
            self._ORMHandler.rollback()
            print(error)
            return "False"

    def add_new_answer(self, answer_text, user_email, question_id):
        try:
            answer = all_tables.Answer(answer_text, 0, user_email, question_id)
            self._ORMHandler.add_new_instanse(all_tables.Answer, answer)
            self._ORMHandler.commit_changes()
            return "True"
        except exc.SQLAlchemyError as error:
            self._ORMHandler.rollback()
            print(error)
            return "False"

    def update_answer(self, answer_id, new_answer_text):
        try:
            res = self._ORMHandler.update_instance(all_tables.Answer, answer_id,
                                             {"text": new_answer_text})
            self._ORMHandler.commit_changes()
            if res:
                return "True"
            else:
                return "False"
        except exc.SQLAlchemyError as error:
            self._ORMHandler.rollback()
            print(error)
            return "False"

    def delete_answer(self, answer_id) -> str:
        try:
            res = self._ORMHandler.delete_instance(all_tables.Answer, answer_id)
            self._ORMHandler.commit_changes()
            if res:
                return "True"
            else:
                return "False"
        except exc.SQLAlchemyError as error:
            self._ORMHandler.rollback()
            print(error)
            return "False"

    def find_question_with_popular_tag_and_highest_rating(self, quantity_of_tag_references: int) -> (int, int, float):
        """
            return (id, rating, time spent on query) of question with tag
            with  references > quantity_of_tag_references
            and highest rating among others
        """
        try:
            start = time.time()
            self._cursor.execute(f'select max(rating) as rating, question_id from '
                                 f'(select * from "Tag" as "t" join '
                                 f'(select * from "Question" as q1 join "Question/Tag" as qt on q1.id=qt.question_id) as bt '
                                 f'on "t".id =bt.tag_id and "t"."references" > {quantity_of_tag_references}) as bbt '
                                 f'group by rating, question_id '
                                 f'order by rating desc limit 1 ')
            res = self._cursor.fetchone()
            finish = time.time()
            if res:
                ans = (res[1], res[0], finish - start)
                return ans
            else:
                return ()
        except (Exception, psycopg2.Error) as error:
            self._connection.rollback()
            print("Error in function find_question_with_popular_tag_and_highest_rating(): ", error)

    def find_answers_start_same_as_question(self, start: str) -> ([(int, str, int)], float):
        """
        :param start:
        :return: (id, text, rating, time)
        """
        try:
            start_time = time.time()

            self._cursor.execute(f'select ans.id, ans.text, ans.rating from "Answer" as ans '
                                 f'join "Question" as q on ans.question_id=q.id and '
                                 f'ans.text like \'{start}%\' and q.text like \'{start}%\'')
            finish_time = time.time()
            return self._cursor.fetchall(), finish_time - start_time

        except (Exception, psycopg2.Error) as error:
            self._connection.rollback()
            print("Error in function find_answers_start_same_as_question(): ", error)

    def find_all_tags_used_during(self, start_date, end_date) -> ([(int, str)], float):
        """
        """
        try:
            start = time.time()
            self._cursor.execute(f'select ta.id, ta.tag from "Tag" as ta '
                                 f'join(select * from "Question/Tag" as qt '
                                 f'join(select * from "Question" where rating > 75 and '
                                 f'"date" between \'{start_date}\' and \'{end_date}\') as qdate '
                                 f'on qt.question_id=qdate.id) '
                                 f'as qtag on ta.id = qtag.tag_id')
            finish = time.time()
            return self._cursor.fetchall(), finish - start;
        except (Exception, psycopg2.Error) as error:
            self._connection.rollback()
            print("Error in function find_all_tags_used_during(): ", error)

    @staticmethod
    def create_user():
        user = {}
        user["email"] = input("Enter email: ")
        user["nickname"] = input("Enter nickname: ")
        user["login"] = input("Enter login: ")
        user["password"] = str(md5(input("Enter password: ").encode()).hexdigest())
        return user

    @staticmethod
    def  create_question():
        question = {}
        question["email"] = input("Enter email: ")
        question["text"] = input("Enter text of the question: ")
        return question

    @staticmethod
    def create_answer():
        answer = {}
        answer["email"] = input("Enter email: ")
        answer["text"] = input("Enter text of the answer: ")
        return answer



handler = DataBaseHandler("axel", "666524", "127.0.0.1", "postgres")
handler.add_random_questions("111@gmail.com", 200000)


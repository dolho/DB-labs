from new_model import DataBaseHandler
import view
import datetime


class Controller:

    def __init__(self):
        self.db = DataBaseHandler("axel", "666524", "127.0.0.1", "postgres")

    def post_user(self, input):
        user = DataBaseHandler.create_user()
        view.user("add", self.db.add_new_user(user["email"], user["nickname"], user["login"], user["password"]))

    def update_user(self, input):
        user = DataBaseHandler.create_user()
        view.user("update", self.db.update_user(user["email"], user["nickname"], user["login"], user["password"]))

    def delete_user(self, input):
        email = input
        view.user("delete", self.db.delete_user(email))

    def post_question(self, input):
        question = DataBaseHandler.create_question()
        view.question("add", self.db.add_new_question(question["email"], question["text"]))

    def update_question(self, input_data):
        try:
            id = int(input_data)
        except ValueError:
            print("ERROR: Id should be positive integer.")
            return
        question = input("Enter new text: ")

        view.question("update", self.db.update_question(input_data, question))

    def delete_question(self, input_data):
        try:
            id = int(input_data)
        except ValueError:
            print("ERROR: Id should be positive integer.")
            return
        view.question("delete", self.db.delete_question(id))

    def post_answer(self, input_data):
        try:
            id = int(input_data)
        except ValueError:
            print("ERROR: Id should be positive integer.")
            return
        answer = DataBaseHandler.create_answer()
        view.answer("add", self.db.add_new_answer(answer["email"], answer["text"], id))

    def update_answer(self, input_data):
        try:
            id = int(input_data)
        except ValueError:
            print("ERROR: Id should be positive integer.")
            return
        answer = input("Enter new text: ")

        view.answer("update", self.db.update_answer(id, answer))

    def delete_answer(self, input_data):
        try:
            id = int(input_data)
        except ValueError:
            print("ERROR: Id should be positive integer.")
            return
        view.answer("delete", self.db.delete_answer(id))

    def find_question_with_popular_tag(self, input_data):
        try:
            quantity_of_references = int(input_data)
        except ValueError:
            print("ERROR: number of references should be positive integer.")
            return
        view.find_question(self.db.find_question_with_popular_tag_and_highest_rating(quantity_of_references))

    def find_answer_starts_same_as_question(self, input_data):
        limit = 10
        view.find_answer(self.db.find_answers_start_same_as_question(input_data), limit)

    def find_all_tags_used_during(self, input_data):
        print("Enter start date")
        start_date = self.create_date()
        print("Enter end date")
        end_date = self.create_date()
        view.find_tag(self.db.find_all_tags_used_during(start_date, end_date))

    def create_date(self):
        while True:
            try:
                year = int(input("Enter year: "))
                month = int(input("Enter month: "))
                day = int(input("Enter day: "))
            except ValueError:
                continue
                print("You should enter positive integers. Try again")
            try:
                date = datetime.date(year, month, day)
                break
            except ValueError as e:
                print(e)
        return date

    def help(self, input):
        print("List of commands: \n"
              "Users: \n"
              "     post/user/\n"
              "     update/user/\n"
              "     delete/user/{email_of_user_to_delete}\n"
              "Questions: \n"
              "     post/question/\n"
              "     update/question/{question_id_to_update}\n"
              "     delete/question/{question_id_to_delete}\n"
              "Answers: \n"
              "     post/answer/\n"
              "     update/answer/{answer_id_to_update}\n"
              "     delete/answer/{answer_id}\n"
              "Find: \n"
              "     get/find_question/{quantity_of_references}\n"
              "     get/find_answer/{symbols_with_which_answer_and questions starts}\n"
              "     get/find_tag_between/\n"
              "Other: \n"
              "     exit - exit from program\n"
              "     get/help/ - see this info again\n")
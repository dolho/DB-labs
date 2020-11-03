from router import Router
from controller import Controller
cont = Controller()
rout = Router(cont)
rout.register_command("post/user/", cont.post_user)
rout.register_command("update/user/", cont.update_user)
rout.register_command("delete/user/", cont.delete_user)

rout.register_command("post/question/", cont.post_question)
rout.register_command("update/question/", cont.update_question)
rout.register_command("delete/question/", cont.delete_question)

rout.register_command("post/answer/", cont.post_answer)
rout.register_command("update/answer/", cont.update_answer)
rout.register_command("delete/answer/", cont.delete_answer)

rout.register_command("get/find_question/", cont.find_question_with_popular_tag)
rout.register_command("get/find_answer/", cont.find_answer_starts_same_as_question)
rout.register_command("get/find_tag_between/", cont.find_all_tags_used_during)
rout.register_command("get/help/", cont.help)


print("Type get/help/ to see list of all commands")
while True:
    command = input("Enter command: ")
    print(command)
    if command == 'exit':
        print("Finish the program")
        break
    rout.handle_command(command)
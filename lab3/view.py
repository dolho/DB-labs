

def user(action, result):
    print(f'Action {action} on user. Result: {result}')


def question(action, result):
    print(f'Action {action} on question instance. Result: {result}')


def answer(action, result):
    print(f'Action {action} on answer instance. Result: {result}')


def find_question(data: (int, int, float)):
    if data:
        print(f'Id of the question: {data[0]}. It\'s rating {data[1]}. Time spent on search: {data[2] * 1000}ms')
    else:
        print("Nothing found")

def find_answer(data: [(int, str, int, float), float], limit):
    if data[0]:
        print(f'Time spent: {data[1] * 1000}ms')
        for i in range(len(data[0])):
            print(data[0][i])
            if i == limit:
                break
    else:
        print("Nothing found")

def find_tag(data):
    limit = 10
    if data[0]:
        print(f'Time spent: {data[1] * 1000}ms')
        print("ID; TAG;")
        for i in range(len(data[0])):
            print(data[0][i])
            if i == limit:
                break
    else:
        print("Nothing found")
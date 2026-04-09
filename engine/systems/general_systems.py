def create_if(condition_func, action_func, *args, **kwargs):
    if condition_func():
        action_func(*args, **kwargs)

def test(arg):
    print(arg)

def main():
    create_if(lambda: True, test, 50)

if __name__ == '__main__':
    main()
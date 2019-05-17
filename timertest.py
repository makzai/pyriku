import threading


def hello(name):
    print("hello %s\n" % name)

    global timer
    timer = threading.Timer(2.0, hello, [name])
    timer.start()


if __name__ == "__main__":
    hello('Miffy')

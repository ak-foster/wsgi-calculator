#!/usr/bin/env python3


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    add_total = sum(args)

    return str(add_total)


def subtracting(*args):
    total = args[0]

    for num in args[1:]:
        total -= num

    return str(total)


def multiply(*args):
    product = args[0]

    for num in args[1:]:
        product *= num

    return str(product)


def divide(*args):
    quotient = args[0]

    for num in args[1:]:
        quotient /= num

    return str(quotient)

def index(*args):
    return "Use the address bar to do math.  E.g. .../subtract/10/2 will return 8"

def resolve_path(path):
    """
    Return two values: a callable and an iterable of arguments.
    """

    funcs = {
        '': index,
        'add': add,
        'subtract': subtracting,
        'multiply': multiply,
        'divide': divide,
    }

    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):

    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        i_args = [int(i) for i in args]
        body = func(*i_args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = f"<h1>Not Found for {path}</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = f"<h1>Internal Server Error for {path}</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

    # TODO: Add error handling for a user attempting to divide by zero.


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

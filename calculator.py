""" Creates a web server and provides a calculator site """

import traceback

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    total = int(args[0]) + int(args[1])

    return str(total)

def subtract(*args):
    """ Returns a STRING with the subtraction of the arguments """

    total = int(args[0]) - int(args[1])

    return str(total)

def multiply(*args):
    """ Returns a STRING with the multiplication of the arguments """

    total = int(args[0]) * int(args[1])

    return str(total)

def divide(*args):
    """ Returns a STRING with the division of the arguments """

    total = int(args[0]) / int(args[1])

    return str(total)

def index():
    """ Returns an HTML page with instructions """

    body = """
<html>
    <h1>Instructions</h1>
    Append 'add', 'subtract', 'multiply', or 'divide' and two numbers
    to the URL to get the result of the calculation.
    <h2>Examples</h2>
    <li>Add: <a href=http://localhost:8080/add/23/42>http://localhost:8080/add/23/42</a></li>
    <li>Subtract: <a href=http://localhost:8080/subtract/23/42>http://localhost:8080/subtract/23/42</a></li>
    <li>Multiply: <a href=http://localhost:8080/multiply/3/5>http://localhost:8080/multiply/3/5</a></li>
    <li>Divide: <a href=http://localhost:8080/divide/22/11>http://localhost:8080/divide/22/11</a></li>
</html>
"""

    return body

def resolve_path(path):
    """ Returns a function and arguments based on path """

    # Dictionary of possible functions for routing
    funcs = {
        '': index,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    # Split the path into operator and args
    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    # Ensure we received a valid operation
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    # Return the operation to call with numbers to action
    return func, args

def application(environ, start_response):
    """ Creates a web server and handles request and response """

    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "500 Internal Server Error"
        body = "<h1>Divide by Zero Error</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

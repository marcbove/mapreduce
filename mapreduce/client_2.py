from pyactor.context import set_context, create_host, serve_forever

if __name__ == "__main__":
    set_context()
    host = create_host('http://192.168.1.46:4323/')

    print 'host listening at port 4323'

    serve_forever()
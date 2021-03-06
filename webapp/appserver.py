import logging

import tornado
from tornado import web, httpserver, ioloop, options

from apphandler.basehandler import AppHandler


def get_web_app():
    """
    Builds the application.py class for the webserver.
    :return: tornado.web.Application
    """
    app = tornado.options.options.applications
    static_path = tornado.options.options.static_path
    return tornado.web.Application([
        (r"/api/(.*)", AppHandler,  {"path": app}),
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': static_path, "default_filename": "index.html"}),

    ],
        cookie_secret=tornado.options.options.hmac_key,
        login_url="/login/login.html",
        debug=tornado.options.options.development
    )


def configure(config_file):
    """
    Configure the tornado app's options.
    """
    logging.info("Using " + str(config_file))

    tornado.options.define("hmac_key", default=None,
                           help="HMAC Key for cookie encryption")
    tornado.options.define("port", default=8080,
                           help="Port to run the server on")
    tornado.options.define("threads", default=1,
                           help="Number of processes to start")
    tornado.options.define("version", default=1.0)
    tornado.options.define("applications",
                           default="./api",
                           help="Location of Applications")
    tornado.options.define("static_path",
                           default="./static",
                           help="Location of Applications")
    tornado.options.define("template_path",
                           default="./templates",
                           help="Template location")
    tornado.options.define("development",
                           default=True,
                           help="Development/Debug Mode")

    logging.info("Spawning" + str(
        tornado.options.options.threads) + " server(s) on port " + str(
        tornado.options.options.port))


def main():
    """
    Regular Execution.

    """
    config_file = "webapp.conf"
    configure(config_file)
    server = tornado.httpserver.HTTPServer(get_web_app())
    server.bind(tornado.options.options.port, address="127.0.0.1")
    server.start(tornado.options.options.threads)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

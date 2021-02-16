from gloover_ws.app import application

application.debug = True
if __name__ == "__main__":
    reactor_args = {}

    def run_twisted_wsgi():
        from sys import stdout
        from twisted.logger import globalLogBeginner, textFileLogObserver
        from twisted.internet import reactor
        from twisted.web.server import Site
        from twisted.web.wsgi import WSGIResource

        # start the logger
        globalLogBeginner.beginLoggingTo([textFileLogObserver(stdout)])

        resource = WSGIResource(reactor, reactor.getThreadPool(), application)
        site = Site(resource)
        reactor.listenTCP(5000, site)
        reactor.run(**reactor_args)

        if application.debug:
            # Disable twisted signal handlers in development only.
            reactor_args['installSignalHandlers'] = 0
            # Turn on auto reload.
            import werkzeug.serving
            run_twisted_wsgi = werkzeug.serving.run_with_reloader("run_twisted_wsgi")

    application.run()
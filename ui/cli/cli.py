
from ui.cli import app, options


def start():
    parser , opts  = options.register()
    app.view.banner()
    
    try:
        if opts.target:
            app.run(opts)
            
        elif opts.version:
            app.show.displayAppVersion()

        else:
            app.show.displayUsage(parser.usage)

    except SystemExit:
        pass

    except BaseException as e:
        app.show.displayError(e)
        exit(1)

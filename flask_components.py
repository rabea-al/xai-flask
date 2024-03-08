from xai_components.base import InArg, OutArg, InCompArg, Component, BaseComponent, xai_component, SubGraphExecutor, \
    dynalist
from flask import Flask, request, redirect, render_template, session, jsonify, stream_with_context, Response
from flask.views import View

import random
import string

FLASK_APP_KEY = 'flask_app'
FLASK_RES_KEY = 'flask_res'
FLASK_STREAMING_RES_KEY = 'flask_streaming_res'
FLASK_ROUTES_KEY = 'flask_routes'
FLASK_JOBS_KEY = 'flask_jobs'


def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


class Route(View):
    def __init__(self, route, ctx):
        self.route = route
        self.ctx = ctx

    def dispatch_request(self, **kwargs):
        self.ctx[FLASK_RES_KEY] = ('', 204)
        self.route.parameters.value = kwargs
        SubGraphExecutor(self.route.body if hasattr(self.route, 'body') else self.route).do(self.ctx)
        response = self.ctx[FLASK_RES_KEY]
        return response


@xai_component
class FlaskCreateApp(Component):
    """Initializes a Flask application with optional configurations for static files and secret key.

    ##### inPorts:
    - name: The name of the Flask application.
    - public_path: The filesystem path to the folder containing static files. Default is 'public'.
    - static_url_path: The URL path at which the static files are accessible. Default is an empty string.
    - secret_key: A secret key used for session management and security. Default is 'opensesame'.
    """

    name: InCompArg[str]
    public_path: InArg[str]
    static_url_path: InArg[str]
    secret_key: InArg[str]

    def execute(self, ctx):
        ctx[FLASK_APP_KEY] = Flask(
            self.name.value,
            static_folder="public" if self.public_path.value is None else self.public_path.value,
            static_url_path="" if self.static_url_path.value is None else self.static_url_path.value
        )
        ctx[FLASK_APP_KEY].secret_key = "opensesame" if self.secret_key.value is None else self.secret_key.value

        for route in ctx.setdefault(FLASK_ROUTES_KEY, []):
            methods = [route.method] if hasattr(route, 'method') else route.methods.value
            endpoint_id = '%s_%s' % (route.route.value, "_".join(methods))
            ctx[FLASK_APP_KEY].add_url_rule(
                route.route.value,
                endpoint=endpoint_id,
                methods=methods,
                view_func=Route.as_view(route.route.value, route, ctx)
            )


@xai_component
class FlaskStartServer(Component):
    """ Starts the Flask Server

    """
    debug: InArg[bool]
    host: InArg[str]
    port: InArg[int]

    def execute(self, ctx):
        app = ctx[FLASK_APP_KEY]

        if 'flask_scheduler' in ctx:
            app.config.from_object(Config())

            scheduler = ctx['flask_scheduler']
            scheduler.init_app(app)
            scheduler.start()

        # Can't run debug mode from inside jupyter.
        app.run(
            debug=False if self.debug.value is None else self.debug.value,
            host="127.0.0.1" if self.host.value is None else self.host.value,
            port=8080 if self.port.value is None else self.port.value
        )


@xai_component(type='Start', color='red')
class FlaskDefineGetRoute(Component):
    """Defines a GET route for a Flask application, linking it to a sequence of actions.

    ##### inPorts:
    - route: The URL path for the GET route.

    ##### Branch:
    - parameters: The path parameters
    """
    method = 'GET'
    parameters: OutArg[dict]
    route: InCompArg[str]

    def init(self, ctx):
        ctx.setdefault(FLASK_ROUTES_KEY, []).append(self)


@xai_component(type='Start', color='red')
class FlaskDefinePostRoute(Component):
    """Defines a POST route for a Flask application, linking it to a sequence of actions.

    ##### inPorts:
    - route: The URL path for the POST route.

    ##### Branch:
    - parameters: The path parameters
    """
    method = 'POST'
    parameters: OutArg[dict]
    route: InCompArg[str]

    def init(self, ctx):
        ctx.setdefault(FLASK_ROUTES_KEY, []).append(self)


@xai_component(type='Start', color='red')
class FlaskDefinePutRoute(Component):
    """Defines a PUT route for a Flask application, linking it to a sequence of actions.

    ##### inPorts:
    - route: The URL path for the PUT route.

    ##### Branch:
    - parameters: The path parameters
    """
    method = 'PUT'
    parameters: OutArg[dict]
    route: InCompArg[str]

    def init(self, ctx):
        ctx.setdefault(FLASK_ROUTES_KEY, []).append(self)


@xai_component(type="Start", color="red")
class FlaskDefineRoute(Component):
    """Defines a route for a Flask application, linking it to a sequence of actions.

    ##### inPorts:
    - route: The URL path for the PUT route.
    - methods: The HTTP Verbs that will trigger this route, at least one must be provided.
               Valid values are: GET, POST, PUT, DELETE, HEAD, OPTIONS

    ##### Branch:
    - parameters: The path parameters
    """
    route: InArg[str]
    methods: InArg[dynalist]
    parameters: OutArg[dict]

    def init(self, ctx):
        ctx.setdefault(FLASK_ROUTES_KEY, []).append(self)


@xai_component
class FlaskInlineDefineGetRoute(Component):
    """Defines a GET route for a Flask application, linking it to a sequence of actions.

    ##### inPorts:
    - route: The URL path for the GET route.

    ##### Branch:
    - body: The first component to be executed when the GET route is accessed.
    - parameters: The path parameters
    """

    body: BaseComponent
    parameters: OutArg[dict]
    route: InCompArg[str]

    def execute(self, ctx):
        app = ctx[FLASK_APP_KEY]
        app.add_url_rule(
            self.route.value,
            methods=['GET'],
            view_func=Route.as_view(self.route.value, self, ctx)
        )


@xai_component
class FlaskInlineDefinePostRoute(Component):
    """Defines a POST route for a Flask application, linking it to a sequence of actions.

    ##### inPorts:
    - route: The URL path for the POST route.

    ##### Branch:
    - body: The first component to be executed when the POST route is accessed.
    - parameters: The path parameters
    """

    body: BaseComponent
    parameters: OutArg[dict]
    route: InCompArg[str]

    def execute(self, ctx):
        app = ctx[FLASK_APP_KEY]
        app.add_url_rule(
            self.route.value,
            methods=['POST'],
            view_func=Route.as_view(self.route.value, self, ctx)
        )


@xai_component
class FlaskInlineDefinePutRoute(Component):
    """Defines a PUT route for a Flask application, linking it to a sequence of actions.

    ##### inPorts:
    - route: The URL path for the PUT route.

    ##### Branch:
    - body: The first component to be executed when the PUT route is accessed.
    - parameters: The path parameters
    """

    body: BaseComponent
    parameters: OutArg[dict]
    route: InCompArg[str]

    def execute(self, ctx):
        app = ctx[FLASK_APP_KEY]
        app.add_url_rule(
            self.route.value,
            methods=['PUT'],
            view_func=Route.as_view(self.route.value, self.body, ctx)
        )


@xai_component(color='red')
class FlaskRenderTemplate(Component):
    """Renders a template with optional arguments for a Flask application.

    ##### inPorts:
    - template_name: The name of the template file to render.
    - args: A dictionary of arguments to pass to the template. Default is an empty dictionary.
    """

    template_name: InCompArg[str]
    args: InArg[dict]

    def execute(self, ctx):
        arg_vars = {} if self.args.value is None else self.args.value

        ctx[FLASK_RES_KEY] = render_template(self.template_name.value, **arg_vars)


@xai_component(color='red')
class FlaskReturnStringResponse(Component):
    """Sets a string response for a Flask route in the ctx.

    ##### inPorts:
    - response: The string to be returned as the response.
    """

    response: InCompArg[str]

    def execute(self, ctx):
        ctx[FLASK_RES_KEY] = self.response.value


@xai_component(color='red')
class FlaskReturnJSONResponse(Component):
    """Sets a JSON response for a Flask route in the ctx.

    ##### inPorts:
    - response: The data to be returned as a JSON response.
    """

    response: InCompArg[any]

    def execute(self, ctx):
        ctx[FLASK_RES_KEY] = jsonify(self.response.value)


@xai_component(color='red')
class FlaskRedirect(Component):
    """Performs a redirection to a specified URL in a Flask application.

    ##### inPorts:
    - url: The target URL to redirect to.
    """

    url: InCompArg[str]

    def execute(self, ctx):
        # Sets a redirection response to the specified URL
        ctx[FLASK_RES_KEY] = redirect(self.url.value)


@xai_component(color='red')
class FlaskReturnResponse(Component):
    """Returns the given value as the Flask response.

    ##### inPorts:
    - value: Any value that Flask supports as a response.
    """
    value: InArg[any]

    def execute(self, ctx):
        ctx[FLASK_RES_KEY] = self.value.value


@xai_component(color='#8B008B')
class FlaskStreamingResponse(Component):
    """Returns a generator as the Flask response

    ##### Branch:
    - body: The first component to be used to generate the response. Must use FlaskStreamEmitter components to produce
            the overall response
    """
    body: BaseComponent

    def execute(self, ctx):
        def generator():
            comp = self.body.comp
            while comp is not None:
                comp = comp.do(ctx)
                maybe_response = ctx.get(FLASK_STREAMING_RES_KEY, None)
                if maybe_response is not None:
                    yield maybe_response
                    ctx[FLASK_STREAMING_RES_KEY] = None

        ctx[FLASK_RES_KEY] = Response(stream_with_context(generator()))


@xai_component(color='#8B008B')
class FlaskStreamEmitter(Component):
    """Adds the value to the current response and streams it out

    ##### inPorts:
    - value: A string to be added to the response. If the value ands in a new line, it will be immediately flushed
    """
    value: InArg[str]

    def execute(self, ctx):
        ctx[FLASK_STREAMING_RES_KEY] = self.value.value


@xai_component
class FlaskGetRequestJson(Component):
    """Retrieves JSON data from a request payload in a Flask application.

    ##### outPorts:
    - value: The JSON data parsed from the request payload.
    """

    value: OutArg[any]

    def execute(self, ctx):
        self.value.value = request.json


@xai_component
class FlaskGetFormValue(Component):
    """Retrieves a value from the form data sent via a POST request in a Flask application.

    ##### inPorts:
    - key: The name of the form field to retrieve the value from.

    ##### outPorts:
    - value: The value of the specified form field.
    """

    key: InCompArg[str]
    value: OutArg[str]

    def execute(self, ctx):
        self.value.value = request.form[self.key.value]


@xai_component
class FlaskSessionSet(Component):
    """Sets a key-value pair in the session storage of a Flask application.

    ##### inPorts:
    - key: The key of the session variable to set.
    - value: The value to be assigned to the session key.
    """

    key: InCompArg[str]
    value: InCompArg[any]

    def execute(self, ctx):
        session[self.key.value] = self.value.value


@xai_component
class FlaskSessionGet(Component):
    """Retrieves a value from the session storage in a Flask application based on the provided key.

    ##### inPorts:
    - key: The key of the session variable to retrieve.

    ##### outPorts:
    - value: The value associated with the provided session key.
    """

    key: InCompArg[str]
    value: OutArg[any]

    def execute(self, ctx):
        self.value.value = session[self.key.value]


@xai_component
class FlaskSessionPop(Component):
    """Removes a key-value pair from the session storage in a Flask application.

    ##### inPorts:
    - key: The key of the session variable to remove.
    """

    key: InCompArg[str]

    def execute(self, ctx):
        session.pop(self.key.value, None)


@xai_component
class FlaskSessionExists(Component):
    """Checks if a given key exists in the session storage of a Flask application.

    ##### inPorts:
    - key: The key to check in the session storage.

    ##### outPorts:
    - exists: Boolean indicating whether the key exists in the session.
    """

    key: InCompArg[str]
    exists: OutArg[bool]

    def execute(self, ctx):
        if self.key.value in session:
            self.exists.value = True
        else:
            self.exists.value = False


@xai_component
class FlaskInitScheduler(Component):
    """Initializes a scheduler for running background jobs in a Flask application.

    ##### Note:
    - This component must be executed before starting the server if background jobs are to be scheduled.
    """

    def execute(self, ctx):
        from flask_apscheduler import APScheduler

        scheduler = APScheduler()
        ctx['flask_scheduler'] = scheduler

        for task in ctx.setdefault(FLASK_JOBS_KEY, []):
            running_flag_key = 'flask_scheduler_' + task.job_id.value + '_running'
            @scheduler.task('interval', id=task.job_id.value, seconds=task.seconds.value,
                            misfire_grace_time=task.seconds.value)
            def job():
                app = ctx[FLASK_APP_KEY]
                if not ctx.setdefault(running_flag_key, False):
                    ctx[running_flag_key] = True

                    app.logger.info(f'Running interval job: {task.job_id.value}...')
                    try:
                        SubGraphExecutor(task).do(ctx)
                        app.logger.info(f'Interval job {task.job_id.value} done.')
                    except Exception as e:
                        app.logger.error(f'Interval job {task.job_id.value} failed with {e}.')
                    finally:
                        ctx[running_flag_key] = False
                else:
                    app.logger.info(f"Job {task.job_id.value} currently running.  Skipping execution.")


class Config:
    SCHEDULER_API_ENABLED = True


@xai_component(type='Start', color='red')
class FlaskCreateIntervalJob(Component):
    """Creates a scheduled interval job in a Flask application.

    ##### inPorts:
    - job_id: The identifier for the job.
    - seconds: The interval time in seconds between executions of the job.
    """
    job_id: InCompArg[str]
    seconds: InCompArg[int]

    def init(self, ctx):
        ctx.setdefault(FLASK_JOBS_KEY, []).append(self)


@xai_component
class FlaskInlineCreateIntervalJob(Component):
    """Creates a scheduled interval job in a Flask application.

    ##### inPorts:
    - job_id: The identifier for the job.
    - seconds: The interval time in seconds between executions of the job.

    ##### Branch:
    - body: The component to be executed when the job is triggered.
    """

    body: BaseComponent

    job_id: InCompArg[str]
    seconds: InCompArg[int]

    def execute(self, ctx):
        scheduler = ctx['flask_scheduler']

        try:
            scheduler.remove_job(self.job_id.value)
        except:
            pass

        running_flag_key = 'flask_scheduler_' + self.job_id.value + '_running'
        @scheduler.task('interval', id=self.job_id.value, seconds=self.seconds.value,
                        misfire_grace_time=self.seconds.value)
        def job():
            app = ctx[FLASK_APP_KEY]
            if not ctx.setdefault(running_flag_key, False):
                ctx[running_flag_key] = True

                app.logger.info(f'Running interval job: {self.job_id.value}...')
                try:
                    self.body.do(ctx)
                    app.logger.info(f'Interval job {self.job_id.value} done.')
                except Exception as e:
                    app.logger.error(f'Interval job {self.job_id.value} failed with {e}.')
                finally:
                    ctx[running_flag_key] = False
            else:
                app.logger.info(f"Job {self.job_id.value} currently running.  Skipping execution.")

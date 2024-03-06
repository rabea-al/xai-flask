from xai_components.base import InArg, OutArg, InCompArg, Component, BaseComponent, xai_component
from flask import Flask, request, redirect, render_template, session, jsonify


import random
import string

def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

@xai_component
class FlaskCreateApp(Component):
    name: InCompArg[str]
    public_path: InArg[str]
    static_url_path: InArg[str]
    secret_key: InArg[str]
    
    def execute(self, ctx):
        ctx['flask_app'] = Flask(
            self.name.value, 
            static_folder="public" if self.public_path.value is None else self.public_path.value, 
            static_url_path="" if self.static_url_path.value is None else self.static_url_path.value
        )
        ctx['flask_app'].secret_key = "opensesame" if self.secret_key.value is None else self.secret_key.value

@xai_component
class FlaskDefineGetRoute(Component):
    on_get: BaseComponent
    route: InCompArg[str]
    
    def execute(self, ctx):
        app = ctx['flask_app']
        ctx_name = random_string(8)
        self_name = random_string(8)
        fn_name = random_string(8)
        code = f"""
ctx_{ctx_name} = ctx
self_{self_name} = self
@app.get(self.route.value)
def get_route_fn_{fn_name}():
    global ctx_{ctx_name}
    global self_{self_name}
    self = self_{self_name}
    ctx = ctx_{ctx_name}
    ctx['flask_res'] = ''
    next = self.on_get
    while next:
        next = next.do(ctx)
    return ctx['flask_res']
        """
        exec(code, globals(), locals())
        
@xai_component
class FlaskDefinePostRoute(Component):
    on_post: BaseComponent
    route: InCompArg[str]
    
    def execute(self, ctx):
        app = ctx['flask_app']
        ctx_name = random_string(8)
        self_name = random_string(8)
        fn_name = random_string(8)
        code = f"""
ctx_{ctx_name} = ctx
self_{self_name} = self
@app.post(self.route.value)
def post_route_fn_{fn_name}():
    global ctx_{ctx_name}
    global self_{self_name}
    self = self_{self_name}
    ctx = ctx_{ctx_name}
    ctx['flask_res'] = ''
    next = self.on_post
    while next:
        next = next.do(ctx)
    return ctx['flask_res']
        """
        exec(code, globals(), locals())
        
@xai_component
class FlaskRenderTemplate(Component):
    template_name: InCompArg[str]
    args: InArg[dict]
    
    def execute(self, ctx):
        arg_vars = {} if self.args.value is None else self.args.value
        
        ctx['flask_res'] = render_template(self.template_name.value, **arg_vars)


@xai_component
class FlaskReturnStringResponse(Component):
    response: InCompArg[str]
    
    def execute(self, ctx):
        ctx['flask_res'] = self.response.value

@xai_component
class FlaskReturnJSONResponse(Component):
    response: InCompArg[any]
    
    def execute(self, ctx):
        ctx['flask_res'] = jsonify(self.response.value)

@xai_component
class FlaskRedirect(Component):
    url: InCompArg[str]
    
    def execute(self, ctx):
        ctx['flask_res'] = redirect(self.url.value)


@xai_component
class FlaskInitScheduler(Component):
    def execute(self, ctx):
        from flask_apscheduler import APScheduler

        ctx['flask_scheduler'] = APScheduler()

class Config:
    SCHEDULER_API_ENABLED = True

        

@xai_component
class FlaskCreateIntervalJob(Component):
    on_timeout: BaseComponent
    
    job_id: InCompArg[str]
    seconds: InCompArg[int]
    
    def execute(self, ctx):
        scheduler = ctx['flask_scheduler']
        
        try:
            scheduler.remove_job(self.job_id.value)
        except:
            pass

        ctx['flask_scheduler' + self.job_id.value + '_running'] = False
        
        @scheduler.task('interval', id=self.job_id.value, seconds=self.seconds.value, misfire_grace_time=self.seconds.value)
        def job():
            app = ctx['flask_app']
            if not ctx['flask_scheduler' + self.job_id.value + '_running']:
                ctx['flask_scheduler' + self.job_id.value + '_running'] = True

                app.logger.info(f'Running interval job: {self.job_id.value}...')
                try:
                    self.on_timeout.do(ctx)
                    app.logger.info(f'Interval job {self.job_id.value} done.')
                except Exception as e:
                    app.logger.error(f'Interval job {self.job_id.value} failed with {e}.')
                finally:
                    ctx['flask_scheduler' + self.job_id.value + '_running'] = False
            else:
                app.logger.info(f"Job {self.job_id.value} currently running.  Skipping execution.")


@xai_component
class FlaskStartServer(Component):
    debug: InArg[bool]
    host: InArg[str]
    port: InArg[int]
    
    def execute(self, ctx):
        app = ctx['flask_app']
        
        if 'flask_scheduler' in ctx:
            app.config.from_object(Config())
            
            scheduler = ctx['flask_scheduler']
            scheduler.init_app(app)
            scheduler.start()
        
        # Can't run debug mode from inside jupyter.
        app.run(
            debug=False if self.debug.value is None else self.debug.value,
            host="127.0.0.1" if self.host.value is None else self.host.value, 
            port=8888 if self.port.value is None else self.port.value
        )

@xai_component
class FlaskSessionPop(Component):
    key: InCompArg[str]
    
    def execute(self, ctx):
        session.pop(self.key.value, None)
        
@xai_component
class FlaskSessionSet(Component):
    key: InCompArg[str]
    value: InCompArg[any]
    
    def execute(self, ctx):
        session[self.key.value] = self.value.value
        
@xai_component
class FlaskSessionGet(Component):
    key: InCompArg[str]
    value: OutArg[any]
    
    def execute(self, ctx):
        self.value.value = session[self.key.value]

@xai_component
class FlaskSessionExists(Component):
    key: InCompArg[str]
    exists: OutArg[bool]
    
    def execute(self, ctx):
        if self.key.value in session:
            self.exists.value = True
        else:
            self.exists.value = False

@xai_component
class FlaskGetFormValue(Component):
    key: InCompArg[str]
    value: OutArg[str]
    
    def execute(self, ctx):
        self.value.value = request.form[self.key.value]


@xai_component
class FlaskGetRequestJson(Component):
    value: OutArg[any]
    
    def execute(self, ctx):
        self.value.value = request.json

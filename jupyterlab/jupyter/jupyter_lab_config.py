import os

c.ServerApp.ip = "*"
c.ServerApp.port = 8090
c.ServerApp.root_dir = os.getenv("WORKSPACE_HOME", "/workspace/")
c.ServerApp.open_browser = False
c.ServerApp.allow_root = True

c.ServerApp.iopub_msg_rate_limit = 100000000
c.ServerApp.iopub_data_rate_limit = 2147483647
c.ServerApp.port_retries = 0
c.ServerApp.quit_button = False
c.ServerApp.allow_remote_access = True
c.ServerApp.disable_check_xsrf = True
c.ServerApp.allow_origin = "*"
c.ServerApp.trust_xheaders = True

c.JupyterApp.answer_yes = True

# Set base url if available
# base_url = os.getenv("WORKSPACE_BASE_URL", "/")
# if base_url is not None and base_url != "/":
#     c.ServerApp.base_url = base_url
c.ServerApp.base_url = os.getenv("NB_PREFIX", "/")

c.FileContentsManager.delete_to_trash = False

# Always use inline for matplotlib
c.IPKernelApp.matplotlib = "inline"


shutdown_inactive_kernels = os.getenv("SHUTDOWN_INACTIVE_KERNELS", "false")
if shutdown_inactive_kernels and shutdown_inactive_kernels.lower().strip() != "false":
    cull_timeout = 172800  # Default is 48 hours
    try:
        # See if env variable is set as timout integer
        cull_timeout = int(shutdown_inactive_kernels)
    except ValueError:
        pass

    if cull_timeout > 0:
        print(
            "Activating automatic kernel shutdown after "
            + str(cull_timeout)
            + "s of inactivity."
        )
        # Timeout (in seconds) after which a kernel is considered idle and ready to be shutdown.
        c.MappingKernelManager.cull_idle_timeout = cull_timeout
        # Do not shutdown if kernel is busy (e.g on long-running kernel cells)
        c.MappingKernelManager.cull_busy = False
        # Do not shutdown kernels that are connected via browser, activate?
        c.MappingKernelManager.cull_connected = False


authenticate_via_jupyter = os.getenv("AUTHENTICATE_VIA_JUPYTER", "false")
if authenticate_via_jupyter and authenticate_via_jupyter.lower().strip() != "false":
    # Authentication via jupyter is activated

    # Do not allow password change since it currently needs a server restart to accept the new password
    c.ServerApp.allow_password_change = False

    if authenticate_via_jupyter.lower().strip() == "<generated>":
        # Do not do anything to let jupyter generate a token in print out on console
        pass
    # If true, do not set any token, authentication will be activate on another way (e.g. via JupyterHub)
    elif authenticate_via_jupyter.lower().strip() != "true":
        # If not true or false, set value as token
        c.ServerApp.token = authenticate_via_jupyter
else:
    # Deactivate token -> no authentication
    c.ServerApp.token = ""


# https://github.com/timkpaine/jupyterlab_iframe
try:
    if not base_url.startswith("/"):
        base_url = "/" + base_url
    # Iframe plugin currently needs absolute URLS
    c.JupyterLabIFrame.iframes = [
        base_url + "tools/ungit",
        base_url + "tools/netdata",
        base_url + "tools/vnc",
        base_url + "tools/glances",
        base_url + "tools/vscode",
    ]
except:
    pass


# https://github.com/timkpaine/jupyterlab_templates
# WORKSPACE_HOME = os.getenv("WORKSPACE_HOME", "/workspace")
# try:
#     if os.path.exists(WORKSPACE_HOME + "/templates"):
#         c.JupyterLabTemplates.template_dirs = [WORKSPACE_HOME + "/templates"]
#     c.JupyterLabTemplates.include_default = False
# except:
#     pass


# Set memory limits for resource use display: https://github.com/yuvipanda/nbresuse
try:
    mem_limit = None
    if os.path.isfile("/sys/fs/cgroup/memory/memory.limit_in_bytes"):
        with open("/sys/fs/cgroup/memory/memory.limit_in_bytes", "r") as file:
            mem_limit = file.read().replace("\n", "").strip()

    total_memory = psutil.virtual_memory().total

    if not mem_limit:
        mem_limit = total_memory
    elif int(mem_limit) > int(total_memory):
        # If mem limit from cgroup bigger than total memory -> use total memory
        mem_limit = total_memory

    # Workaround -> round memory limit, otherwise the number is quite long
    # TODO fix in nbresuse
    mem_limit = round(int(mem_limit) / (1024 * 1024)) * (1024 * 1024)
    c.ResourceUseDisplay.mem_limit = int(mem_limit)
    c.ResourceUseDisplay.mem_warning_threshold = 0.1
except:
    pass


# Change default umask for all subprocesses of the notebook server if set in
# the environment
if "NB_UMASK" in os.environ:
    os.umask(int(os.environ["NB_UMASK"], 8))


# Configuration file for lab.

# ------------------------------------------------------------------------------
# Application(SingletonConfigurable) configuration
# ------------------------------------------------------------------------------
## This is an application.

## The date format used by logging formatters for %(asctime)s
#  Default: '%Y-%m-%d %H:%M:%S'
# c.Application.log_datefmt = '%Y-%m-%d %H:%M:%S'

## The Logging format template
#  Default: '[%(name)s]%(highlevel)s %(message)s'
# c.Application.log_format = '[%(name)s]%(highlevel)s %(message)s'

## Set the log level by value or name.
#  Choices: any of [0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']
#  Default: 30
# c.Application.log_level = 30

## Instead of starting the Application, dump configuration to stdout
#  Default: False
# c.Application.show_config = False

## Instead of starting the Application, dump configuration to stdout (as JSON)
#  Default: False
# c.Application.show_config_json = False

# ------------------------------------------------------------------------------
# JupyterApp(Application) configuration
# ------------------------------------------------------------------------------
## Base class for Jupyter applications

## Answer yes to any prompts.
#  Default: False
# c.JupyterApp.answer_yes = False

## Full path of a config file.
#  Default: ''
# c.JupyterApp.config_file = ''

## Specify a config file to load.
#  Default: ''
# c.JupyterApp.config_file_name = ''

## Generate default config file.
#  Default: False
# c.JupyterApp.generate_config = False

## The date format used by logging formatters for %(asctime)s
#  See also: Application.log_datefmt
# c.JupyterApp.log_datefmt = '%Y-%m-%d %H:%M:%S'

## The Logging format template
#  See also: Application.log_format
# c.JupyterApp.log_format = '[%(name)s]%(highlevel)s %(message)s'

## Set the log level by value or name.
#  See also: Application.log_level
# c.JupyterApp.log_level = 30

## Instead of starting the Application, dump configuration to stdout
#  See also: Application.show_config
# c.JupyterApp.show_config = False

## Instead of starting the Application, dump configuration to stdout (as JSON)
#  See also: Application.show_config_json
# c.JupyterApp.show_config_json = False

# ------------------------------------------------------------------------------
# ExtensionApp(JupyterApp) configuration
# ------------------------------------------------------------------------------
## Base class for configurable Jupyter Server Extension Applications.
#
#  ExtensionApp subclasses can be initialized two ways:
#  1. Extension is listed as a jpserver_extension, and ServerApp calls
#      its load_jupyter_server_extension classmethod. This is the
#      classic way of loading a server extension.
#  2. Extension is launched directly by calling its `launch_instance`
#      class method. This method can be set as a entry_point in
#      the extensions setup.py

## Answer yes to any prompts.
#  See also: JupyterApp.answer_yes
# c.ExtensionApp.answer_yes = False

## Full path of a config file.
#  See also: JupyterApp.config_file
# c.ExtensionApp.config_file = ''

## Specify a config file to load.
#  See also: JupyterApp.config_file_name
# c.ExtensionApp.config_file_name = ''

## Generate default config file.
#  See also: JupyterApp.generate_config
# c.ExtensionApp.generate_config = False

## Handlers appended to the server.
#  Default: []
# c.ExtensionApp.handlers = []

## The date format used by logging formatters for %(asctime)s
#  See also: Application.log_datefmt
# c.ExtensionApp.log_datefmt = '%Y-%m-%d %H:%M:%S'

## The Logging format template
#  See also: Application.log_format
# c.ExtensionApp.log_format = '[%(name)s]%(highlevel)s %(message)s'

## Set the log level by value or name.
#  See also: Application.log_level
# c.ExtensionApp.log_level = 30

## Settings that will passed to the server.
#  Default: {}
# c.ExtensionApp.settings = {}

## Instead of starting the Application, dump configuration to stdout
#  See also: Application.show_config
# c.ExtensionApp.show_config = False

## Instead of starting the Application, dump configuration to stdout (as JSON)
#  See also: Application.show_config_json
# c.ExtensionApp.show_config_json = False

## paths to search for serving static files.
#
#  This allows adding javascript/css to be available from the notebook server
#  machine, or overriding individual files in the IPython
#  Default: []
# c.ExtensionApp.static_paths = []

## Url where the static assets for the extension are served.
#  Default: ''
# c.ExtensionApp.static_url_prefix = ''

## Paths to search for serving jinja templates.
#
#  Can be used to override templates from notebook.templates.
#  Default: []
# c.ExtensionApp.template_paths = []

# ------------------------------------------------------------------------------
# LabServerApp(ExtensionApp) configuration
# ------------------------------------------------------------------------------
## A Lab Server Application that runs out-of-the-box

## "A list of comma-separated URIs to get the allowed extensions list
#
#  .. versionchanged:: 2.0.0
#      `LabServerApp.whitetlist_uris` renamed to `allowed_extensions_uris`
#  Default: ''
# c.LabServerApp.allowed_extensions_uris = ''

## Answer yes to any prompts.
#  See also: JupyterApp.answer_yes
# c.LabServerApp.answer_yes = False

## Deprecated, use `LabServerApp.blocked_extensions_uris`
#  Default: ''
# c.LabServerApp.blacklist_uris = ''

## A list of comma-separated URIs to get the blocked extensions list
#
#  .. versionchanged:: 2.0.0
#      `LabServerApp.blacklist_uris` renamed to `blocked_extensions_uris`
#  Default: ''
# c.LabServerApp.blocked_extensions_uris = ''

## Full path of a config file.
#  See also: JupyterApp.config_file
# c.LabServerApp.config_file = ''

## Specify a config file to load.
#  See also: JupyterApp.config_file_name
# c.LabServerApp.config_file_name = ''

## Generate default config file.
#  See also: JupyterApp.generate_config
# c.LabServerApp.generate_config = False

## Handlers appended to the server.
#  See also: ExtensionApp.handlers
# c.LabServerApp.handlers = []

## Options to pass to the jinja2 environment for this
#  Default: {}
# c.LabServerApp.jinja2_options = {}

## The interval delay in seconds to refresh the lists
#  Default: 3600
# c.LabServerApp.listings_refresh_seconds = 3600

## The optional kwargs to use for the listings HTTP requests             as
#  described on https://2.python-requests.org/en/v2.7.0/api/#requests.request
#  Default: {}
# c.LabServerApp.listings_request_options = {}

## The date format used by logging formatters for %(asctime)s
#  See also: Application.log_datefmt
# c.LabServerApp.log_datefmt = '%Y-%m-%d %H:%M:%S'

## The Logging format template
#  See also: Application.log_format
# c.LabServerApp.log_format = '[%(name)s]%(highlevel)s %(message)s'

## Set the log level by value or name.
#  See also: Application.log_level
# c.LabServerApp.log_level = 30

## Settings that will passed to the server.
#  See also: ExtensionApp.settings
# c.LabServerApp.settings = {}

## Instead of starting the Application, dump configuration to stdout
#  See also: Application.show_config
# c.LabServerApp.show_config = False

## Instead of starting the Application, dump configuration to stdout (as JSON)
#  See also: Application.show_config_json
# c.LabServerApp.show_config_json = False

## paths to search for serving static files.
#  See also: ExtensionApp.static_paths
# c.LabServerApp.static_paths = []

## Url where the static assets for the extension are served.
#  See also: ExtensionApp.static_url_prefix
# c.LabServerApp.static_url_prefix = ''

## Paths to search for serving jinja templates.
#  See also: ExtensionApp.template_paths
# c.LabServerApp.template_paths = []

## A list of comma-separated URIs to get the whitelist
#  Default: ''
# c.LabServerApp.whitelist_uris = ''

# ------------------------------------------------------------------------------
# LabApp(LabServerApp) configuration
# ------------------------------------------------------------------------------
##
#  See also: LabServerApp.allowed_extensions_uris
# c.LabApp.allowed_extensions_uris = ''

## Answer yes to any prompts.
#  See also: JupyterApp.answer_yes
# c.LabApp.answer_yes = False

## The app directory to launch JupyterLab from.
#  Default: None
# c.LabApp.app_dir = None

## Deprecated, use `LabServerApp.blocked_extensions_uris`
#  See also: LabServerApp.blacklist_uris
# c.LabApp.blacklist_uris = ''

##
#  See also: LabServerApp.blocked_extensions_uris
# c.LabApp.blocked_extensions_uris = ''

## Full path of a config file.
#  See also: JupyterApp.config_file
# c.LabApp.config_file = ''

## Specify a config file to load.
#  See also: JupyterApp.config_file_name
# c.LabApp.config_file_name = ''

## Whether to start the app in core mode. In this mode, JupyterLab will run using
#  the JavaScript assets that are within the installed JupyterLab Python package.
#  In core mode, third party extensions are disabled. The `--dev-mode` flag is an
#  alias to this to be used when the Python package itself is installed in
#  development mode (`pip install -e .`).
#  Default: False
# c.LabApp.core_mode = False

## The default URL to redirect to from `/`
#  Default: '/lab'
# c.LabApp.default_url = '/lab'

## Whether to start the app in dev mode. Uses the unpublished local JavaScript
#  packages in the `dev_mode` folder.  In this case JupyterLab will show a red
#  stripe at the top of the page.  It can only be used if JupyterLab is installed
#  as `pip install -e .`.
#  Default: False
# c.LabApp.dev_mode = False

## Whether to expose the global app instance to browser via window.jupyterlab
#  Default: False
# c.LabApp.expose_app_in_browser = False

## Generate default config file.
#  See also: JupyterApp.generate_config
# c.LabApp.generate_config = False

## Handlers appended to the server.
#  See also: ExtensionApp.handlers
# c.LabApp.handlers = []

## Options to pass to the jinja2 environment for this
#  Default: {}
# c.LabApp.jinja2_options = {}

## The interval delay in seconds to refresh the lists
#  See also: LabServerApp.listings_refresh_seconds
# c.LabApp.listings_refresh_seconds = 3600

## The optional kwargs to use for the listings HTTP requests             as
#  described on https://2.python-requests.org/en/v2.7.0/api/#requests.request
#  See also: LabServerApp.listings_request_options
# c.LabApp.listings_request_options = {}

## The date format used by logging formatters for %(asctime)s
#  See also: Application.log_datefmt
# c.LabApp.log_datefmt = '%Y-%m-%d %H:%M:%S'

## The Logging format template
#  See also: Application.log_format
# c.LabApp.log_format = '[%(name)s]%(highlevel)s %(message)s'

## Set the log level by value or name.
#  See also: Application.log_level
# c.LabApp.log_level = 30

## The override url for static lab assets, typically a CDN.
#  Default: ''
# c.LabApp.override_static_url = ''

## The override url for static lab theme assets, typically a CDN.
#  Default: ''
# c.LabApp.override_theme_url = ''

## Settings that will passed to the server.
#  See also: ExtensionApp.settings
# c.LabApp.settings = {}

## Instead of starting the Application, dump configuration to stdout
#  See also: Application.show_config
# c.LabApp.show_config = False

## Instead of starting the Application, dump configuration to stdout (as JSON)
#  See also: Application.show_config_json
# c.LabApp.show_config_json = False

## paths to search for serving static files.
#  See also: ExtensionApp.static_paths
# c.LabApp.static_paths = []

## Url where the static assets for the extension are served.
#  See also: ExtensionApp.static_url_prefix
# c.LabApp.static_url_prefix = ''

## Paths to search for serving jinja templates.
#  See also: ExtensionApp.template_paths
# c.LabApp.template_paths = []

## The directory for user settings.
#  Default: 'C:\\Users\\inaba\\.jupyter\\lab\\user-settings'
# c.LabApp.user_settings_dir = 'C:\\Users\\inaba\\.jupyter\\lab\\user-settings'

## Whether to serve the app in watch mode
#  Default: False
# c.LabApp.watch = False

## A list of comma-separated URIs to get the whitelist
#  See also: LabServerApp.whitelist_uris
# c.LabApp.whitelist_uris = ''

## The directory for workspaces
#  Default: 'C:\\Users\\inaba\\.jupyter\\lab\\workspaces'
# c.LabApp.workspaces_dir = 'C:\\Users\\inaba\\.jupyter\\lab\\workspaces'

# ------------------------------------------------------------------------------
# ServerApp(JupyterApp) configuration
# ------------------------------------------------------------------------------
## ����Access-Control-Allow-Credentials:true��ͷ
#  Default: False
# c.ServerApp.allow_credentials = False

## Set the Access-Control-Allow-Origin header
#
#  Use '*' to allow any origin to access your server.
#
#  Takes precedence over allow_origin_pat.
#  Default: ''
# c.ServerApp.allow_origin = ''

## Use a regular expression for the Access-Control-Allow-Origin header
#
#  Requests from an origin matching the expression will get replies with:
#
#      Access-Control-Allow-Origin: origin
#
#  where `origin` is the origin of the request.
#
#  Ignored if allow_origin is set.
#  Default: ''
# c.ServerApp.allow_origin_pat = ''

## Allow password to be changed at login for the Jupyter server.
#
#  While loggin in with a token, the Jupyter server UI will give the opportunity
#  to the user to enter a new password at the same time that will replace the
#  token login mechanism.
#
#  This can be set to false to prevent changing password from the UI/API.
#  Default: True
# c.ServerApp.allow_password_change = True

## Allow requests where the Host header doesn't point to a local server
#
#  By default, requests get a 403 forbidden response if the 'Host' header shows
#  that the browser thinks it's on a non-local domain. Setting this option to
#  True disables this check.
#
#  This protects against 'DNS rebinding' attacks, where a remote web server
#  serves you a page and then changes its DNS to send later requests to a local
#  IP, bypassing same-origin checks.
#
#  Local IP addresses (such as 127.0.0.1 and ::1) are allowed as local, along
#  with hostnames configured in local_hostnames.
#  Default: False
# c.ServerApp.allow_remote_access = False

## Whether to allow the user to run the server as root.
#  Default: False
# c.ServerApp.allow_root = False

## Answer yes to any prompts.
#  See also: JupyterApp.answer_yes
# c.ServerApp.answer_yes = False

## The base URL for the Jupyter server.
#
#  Leading and trailing slashes can be omitted, and will automatically be added.
#  Default: '/'
# c.ServerApp.base_url = '/'

## Specify what command to use to invoke a web browser when starting the server.
#  If not specified, the default browser will be determined by the `webbrowser`
#  standard library module, which allows setting of the BROWSER environment
#  variable to override it.
#  Default: ''
# c.ServerApp.browser = ''

## SSL/TLS ��֤�ļ�����ȫ·��.
#  Default: ''
# c.ServerApp.certfile = ''

## ����ssl/tls�ͻ���������֤��֤��䷢֤�������·��.
#  Default: ''
# c.ServerApp.client_ca = ''

## Full path of a config file.
#  See also: JupyterApp.config_file
# c.ServerApp.config_file = ''

## Specify a config file to load.
#  See also: JupyterApp.config_file_name
# c.ServerApp.config_file_name = ''

## The config manager class to use
#  Default: 'jupyter_server.services.config.manager.ConfigManager'
# c.ServerApp.config_manager_class = 'jupyter_server.services.config.manager.ConfigManager'

## The content manager class to use.
#  Default: 'jupyter_server.services.contents.largefilemanager.LargeFileManager'
# c.ServerApp.contents_manager_class = 'jupyter_server.services.contents.largefilemanager.LargeFileManager'

## Extra keyword arguments to pass to `set_secure_cookie`. See tornado's
#  set_secure_cookie docs for details.
#  Default: {}
# c.ServerApp.cookie_options = {}

## The random bytes used to secure cookies. By default this is a new random
#  number every time you start the server. Set it to a value in a config file to
#  enable logins to persist across server sessions.
#
#  Note: Cookie secrets should be kept private, do not share config files with
#  cookie_secret stored in plaintext (you can read the value from a file).
#  Default: b''
# c.ServerApp.cookie_secret = b''

## ���cookie��Կ���ļ���������.
#  Default: ''
# c.ServerApp.cookie_secret_file = ''

## Override URL shown to users.
#
#  Replace actual URL, including protocol, address, port and base URL, with the
#  given value when displaying URL to the users. Do not change the actual
#  connection URL. If authentication token is enabled, the token is added to the
#  custom URL automatically.
#
#  This option is intended to be used when the URL to display to the user cannot
#  be determined reliably by the Jupyter server (proxified or containerized
#  setups for example).
#  Default: ''
# c.ServerApp.custom_display_url = ''

## �� `/` �ض��򵽵�Ĭ��URL
#  Default: '/'
# c.ServerApp.default_url = '/'

## Disable cross-site-request-forgery protection
#
#  Jupyter notebook 4.3.1 introduces protection from cross-site request
#  forgeries, requiring API requests to either:
#
#  - originate from pages served by this server (validated with XSRF cookie and
#  token), or - authenticate with a token
#
#  Some anonymous compute resources still desire the ability to run code,
#  completely without authentication. These services can disable all
#  authentication and security checks, with the full knowledge of what that
#  implies.
#  Default: False
# c.ServerApp.disable_check_xsrf = False

## handlers that should be loaded at higher priority than the default services
#  Default: []
# c.ServerApp.extra_services = []

## Extra paths to search for serving static files.
#
#  This allows adding javascript/css to be available from the Jupyter server
#  machine, or overriding individual files in the IPython
#  Default: []
# c.ServerApp.extra_static_paths = []

## Extra paths to search for serving jinja templates.
#
#  Can be used to override templates from jupyter_server.templates.
#  Default: []
# c.ServerApp.extra_template_paths = []

#  Default: ''
# c.ServerApp.file_to_run = ''

## Generate default config file.
#  See also: JupyterApp.generate_config
# c.ServerApp.generate_config = False

## Extra keyword arguments to pass to `get_secure_cookie`. See tornado's
#  get_secure_cookie docs for details.
#  Default: {}
# c.ServerApp.get_secure_cookie_kwargs = {}

## (bytes/sec) Maximum rate at which stream output can be sent on iopub before
#  they are limited.
#  Default: 1000000
# c.ServerApp.iopub_data_rate_limit = 1000000

## (msgs/sec) Maximum rate at which messages can be sent on iopub before they are
#  limited.
#  Default: 1000
# c.ServerApp.iopub_msg_rate_limit = 1000

## The IP address the Jupyter server will listen on.
#  Default: 'localhost'
# c.ServerApp.ip = 'localhost'

## Supply extra arguments that will be passed to Jinja environment.
#  Default: {}
# c.ServerApp.jinja_environment_options = {}

## Extra variables to supply to jinja templates when rendering.
#  Default: {}
# c.ServerApp.jinja_template_vars = {}

## ��Pythonģ����Ϊ�ʼǱ���������չ���ء�����ʹ����Ŀֵ�����úͽ�����չ�ļ��ء���Щ��չ������ĸ˳����ء�
#  Default: {}
# c.ServerApp.jpserver_extensions = {}

## The kernel manager class to use.
#  Default: 'jupyter_server.services.kernels.kernelmanager.MappingKernelManager'
# c.ServerApp.kernel_manager_class = 'jupyter_server.services.kernels.kernelmanager.MappingKernelManager'

## The kernel spec manager class to use. Should be a subclass of
#  `jupyter_client.kernelspec.KernelSpecManager`.
#
#  The Api of KernelSpecManager is provisional and might change without warning
#  between this version of Jupyter and the next stable one.
#  Default: 'jupyter_client.kernelspec.KernelSpecManager'
# c.ServerApp.kernel_spec_manager_class = 'jupyter_client.kernelspec.KernelSpecManager'

## SSL/TLS ˽Կ�ļ�����ȫ·��.
#  Default: ''
# c.ServerApp.keyfile = ''

## Hostnames to allow as local when allow_remote_access is False.
#
#  Local IP addresses (such as 127.0.0.1 and ::1) are automatically accepted as
#  local as well.
#  Default: ['localhost']
# c.ServerApp.local_hostnames = ['localhost']

## The date format used by logging formatters for %(asctime)s
#  See also: Application.log_datefmt
# c.ServerApp.log_datefmt = '%Y-%m-%d %H:%M:%S'

## The Logging format template
#  See also: Application.log_format
# c.ServerApp.log_format = '[%(name)s]%(highlevel)s %(message)s'

## Set the log level by value or name.
#  See also: Application.log_level
# c.ServerApp.log_level = 30

## The login handler class to use.
#  Default: 'jupyter_server.auth.login.LoginHandler'
# c.ServerApp.login_handler_class = 'jupyter_server.auth.login.LoginHandler'

## The logout handler class to use.
#  Default: 'jupyter_server.auth.logout.LogoutHandler'
# c.ServerApp.logout_handler_class = 'jupyter_server.auth.logout.LogoutHandler'

## Sets the maximum allowed size of the client request body, specified in the
#  Content-Length request header field. If the size in a request exceeds the
#  configured value, a malformed HTTP message is returned to the client.
#
#  Note: max_body_size is applied even in streaming mode.
#  Default: 536870912
# c.ServerApp.max_body_size = 536870912

## Gets or sets the maximum amount of memory, in bytes, that is allocated for use
#  by the buffer manager.
#  Default: 536870912
# c.ServerApp.max_buffer_size = 536870912

## DEPRECATED, use root_dir.
#  Default: ''
# c.ServerApp.notebook_dir = ''

## Whether to open in a browser after starting. The specific browser used is
#  platform dependent and determined by the python standard library `webbrowser`
#  module, unless it is overridden using the --browser (ServerApp.browser)
#  configuration option.
#  Default: False
# c.ServerApp.open_browser = False

## Hashed password to use for web authentication.
#
#  To generate, type in a python/IPython shell:
#
#    from jupyter_server.auth import passwd; passwd()
#
#  The string should be of the form type:salt:hashed-password.
#  Default: ''
# c.ServerApp.password = ''

## Forces users to use a password for the Jupyter server. This is useful in a
#  multi user environment, for instance when everybody in the LAN can access each
#  other's machine through ssh.
#
#  In such a case, serving on localhost is not secure since any user can connect
#  to the Jupyter server via ssh.
#  Default: False
# c.ServerApp.password_required = False

## The port the Jupyter server will listen on.
#  Default: 8888
# c.ServerApp.port = 8888

## ���ָ���Ķ˿ڲ����ã���Ҫ���������˿ڵ�����.
#  Default: 50
# c.ServerApp.port_retries = 50

## DISABLED: use %pylab or %matplotlib in the notebook to enable matplotlib.
#  Default: 'disabled'
# c.ServerApp.pylab = 'disabled'

## If True, display a button in the dashboard to quit (shutdown the Jupyter
#  server).
#  Default: True
# c.ServerApp.quit_button = True

## (sec) Time window used to check the message and data rate limits.
#  Default: 3
# c.ServerApp.rate_limit_window = 3

## �������е��쳣���������ط�������չ��?
#  Default: False
# c.ServerApp.reraise_server_extension_failures = False

## ���ڱʼǱ����ں˵�Ŀ¼��
#  Default: ''
# c.ServerApp.root_dir = ''

## The session manager class to use.
#  Default: 'jupyter_server.services.sessions.sessionmanager.SessionManager'
# c.ServerApp.session_manager_class = 'jupyter_server.services.sessions.sessionmanager.SessionManager'

## Instead of starting the Application, dump configuration to stdout
#  See also: Application.show_config
# c.ServerApp.show_config = False

## Instead of starting the Application, dump configuration to stdout (as JSON)
#  See also: Application.show_config_json
# c.ServerApp.show_config_json = False

## Shut down the server after N seconds with no kernels or terminals running and
#  no activity. This can be used together with culling idle kernels
#  (MappingKernelManager.cull_idle_timeout) to shutdown the Jupyter server when
#  it's not in use. This is not precisely timed: it may shut down up to a minute
#  later. 0 (the default) disables this automatic shutdown.
#  Default: 0
# c.ServerApp.shutdown_no_activity_timeout = 0

## Supply SSL options for the tornado HTTPServer. See the tornado docs for
#  details.
#  Default: {}
# c.ServerApp.ssl_options = {}

## Supply overrides for terminado. Currently only supports "shell_command".
#  Default: {}
# c.ServerApp.terminado_settings = {}

## Set to False to disable terminals.
#
#  This does *not* make the server more secure by itself. Anything the user can
#  in a terminal, they can also do in a notebook.
#
#  Terminals may also be automatically disabled if the terminado package is not
#  available.
#  Default: True
# c.ServerApp.terminals_enabled = True

## Token used for authenticating first-time connections to the server.
#
#  When no password is enabled, the default is to generate a new, random token.
#
#  Setting to an empty string disables authentication altogether, which is NOT
#  RECOMMENDED.
#  Default: '<generated>'
# c.ServerApp.token = '<generated>'

## Supply overrides for the tornado.web.Application that the Jupyter server uses.
#  Default: {}
# c.ServerApp.tornado_settings = {}

## Whether to trust or not X-Scheme/X-Forwarded-Proto and X-Real-Ip/X-Forwarded-
#  For headerssent by the upstream reverse proxy. Necessary if the proxy handles
#  SSL
#  Default: False
# c.ServerApp.trust_xheaders = False

## Specify where to open the server on startup. This is the `new` argument passed
#  to the standard library method `webbrowser.open`. The behaviour is not
#  guaranteed, but depends on browser support. Valid values are:
#
#   - 2 opens a new tab,
#   - 1 opens a new window,
#   - 0 opens in an existing window.
#
#  See the `webbrowser.open` documentation for details.
#  Default: 2
# c.ServerApp.webbrowser_open_new = 2

## Set the tornado compression options for websocket connections.
#
#  This value will be returned from
#  :meth:`WebSocketHandler.get_compression_options`. None (default) will disable
#  compression. A dict (even an empty one) will enable compression.
#
#  See the tornado docs for WebSocketHandler.get_compression_options for details.
#  Default: None
# c.ServerApp.websocket_compression_options = None

## The base URL for websockets, if it differs from the HTTP server (hint: it
#  almost certainly doesn't).
#
#  Should be in the form of an HTTP origin: ws[s]://hostname[:port]
#  Default: ''
# c.ServerApp.websocket_url = ''

#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import bokeh

from bokeh.embed import server_document

_isAfterBokeh1210 = False

try:
    from bokeh.embed import notebook_div
except ImportError:
    from bokeh.embed.notebook import notebook_content
    _isAfterBokeh1210 = True


import logging
logger = logging.getLogger(__name__)
import uuid




def _show_zeppelin_doc_with_state(obj, state, notebook_handle):
    if notebook_handle:
        raise ValueError("Zeppelin doesn't support notebook_handle.")
    if _isAfterBokeh1210:
        (script, div, cell_doc) = notebook_content(obj)
        print("%html " + div)
        print('%html ' + '<script type="text/javascript">' + script + "</script>")
    else:
        print("%html " + notebook_div(obj))

    return None

def _origin_url(url):
    if url.startswith("http"):
        url = url.split("//")[1]
    return url

def _show_zeppelin_app_with_state(app, state, notebook_url):
    logging.basicConfig()
    from tornado.ioloop import IOLoop
    from bokeh.server.server import Server
    loop = IOLoop.current()
    server = Server({"/": app}, io_loop=loop, port=0,  allow_websocket_origin=[notebook_url])

    server_id = uuid.uuid4().hex
    if _isAfterBokeh1210:
        from bokeh.io.state import curstate
        curstate().uuid_to_server[server_id] = server
    else:
        bokeh.io._state.uuid_to_server[server_id] = server

    server.start()
    url = 'http://%s:%d%s' % (notebook_url.split(':')[0], server.port, "/")
    script = server_document(url)

    div_html = "<div class='bokeh_class' id='{divid}'>{script}</div>"
    print('%html ' + div_html.format(script=script, divid=server_id))


_notebook_loaded = None

FINALIZE_JS = """
document.getElementById("%s").textContent = "BokehJS is loading...";
"""

def _load_notebook_html(resources=None, verbose=False, hide_banner=False,
                        load_timeout=5000):
    global _notebook_loaded

    from bokeh import __version__
    from bokeh.core.templates import AUTOLOAD_NB_JS, NOTEBOOK_LOAD
    from bokeh.util.serialization import make_id
    from bokeh.util.compiler import bundle_all_models
    from bokeh.resources import CDN

    if resources is None:
        resources = CDN

    if resources.mode == 'inline':
        js_info = 'inline'
        css_info = 'inline'
    else:
        js_info = resources.js_files[0] if len(resources.js_files) == 1 else resources.js_files
        css_info = resources.css_files[0] if len(resources.css_files) == 1 else resources.css_files

    warnings = ["Warning: " + msg['text'] for msg in resources.messages if msg['type'] == 'warn']

    if _notebook_loaded and verbose:
        warnings.append('Warning: BokehJS previously loaded')

    _notebook_loaded = resources

    element_id = make_id()

    html = NOTEBOOK_LOAD.render(
        element_id    = element_id,
        verbose       = verbose,
        js_info       = js_info,
        css_info      = css_info,
        bokeh_version = __version__,
        warnings      = warnings,
        hide_banner   = hide_banner,
    )

    custom_models_js = bundle_all_models() or ""

    js = AUTOLOAD_NB_JS.render(
        elementid = '' if hide_banner else element_id,
        js_urls  = resources.js_files,
        css_urls = resources.css_files,
        js_raw   = resources.js_raw + [custom_models_js] + ([] if hide_banner else [FINALIZE_JS % element_id]),
        css_raw  = resources.css_raw_str,
        force    = True,
        timeout  = load_timeout
    )

    return html, js

def load_notebook(resources=None, verbose=False, hide_banner=False, load_timeout=5000):
    ''' Prepare the Zeppelin notebook for displaying Bokeh plots.

    Args:
        resources (Resource, optional) :
            how and where to load BokehJS from (default: CDN)

        verbose (bool, optional) :
            whether to report detailed settings (default: False)

        hide_banner (bool, optional):
            whether to hide the Bokeh banner (default: False)

        load_timeout (int, optional) :
            Timeout in milliseconds when plots assume load timed out (default: 5000)

    .. warning::
        Clearing the output cell containing the published BokehJS
        resources HTML code may cause Bokeh CSS styling to be removed.

    Returns:
        None

    '''
    lab_html, lab_js = _load_notebook_html(resources, verbose, hide_banner, load_timeout)
    print('\n%html ' + lab_html)
    print('\n%html ' + '<script type="text/javascript">' + lab_js + "</script>")



import sys, os, textwrap
import tree_sitter_javascript as javascript
from tree_sitter import Parser, Language
from bs4 import BeautifulSoup
from contextlib import contextmanager
from core.scanner.endpoint import EndPoint
from core.jsanalyzer.anlysis import *
   

class EndpointsMiner:

    class Resolver:
        def __init__(self):
            self._variables = {}
            self._aliases = {}
            self._functions = {}

        def insert(self, name, value):
            self._variables[ name ] = value

        def get(self, name):
            return self._variables[ name ] if name in self._variables else None
        
        def unwrap(self, obj):
            while callable( obj ):
                obj = obj()

            if isinstance( obj, list ):
                for idx in range( len(obj) ):
                    obj[ idx ] = self.unwrap( obj[idx] )

            elif isinstance( obj, dict ):
                for k, o in obj.items():
                    obj[ k ] = self.unwrap( o )

            return obj

        def resolve(self, node, src, local_vars=None, depth=0, visited=None):
            """
            Resolves a node in the global context or with optional local_vars
            """

            if node is None or depth > 3:
                return None

            if visited is None:
                visited = set()

            node_id = id( node )
            if node_id in visited:
                return None
            visited.add( node_id )

            if local_vars is None:
                local_vars = {}

            t = node.type

            # LITERALS
            if t == "string":
                return EndpointsMiner.get_text( node, src ).strip( '"\'' )
            if t == "number":
                return EndpointsMiner.get_text( node, src )

            if t == "identifier":
                name = EndpointsMiner.get_text(node, src  )

                # check local scope first
                if name in local_vars:
                    value = local_vars[ name ]
                else:
                    # resolve aliases recursively
                    name = self._resolve_alias( name )
                    value = self._variables.get( name, name )

                # fully resolve chained identifiers
                while isinstance( value, str ) and value in self._variables:
                    value = self._variables[ value ]

                value = self.unwrap( value )

                return value

            # string concat
            if t == "binary_expression":
                left = self.resolve( node.child_by_field_name("left"), src, local_vars, depth+1, visited )
                right = self.resolve( node.child_by_field_name("right"), src, local_vars, depth+1, visited )
                return f"{left}{right}"

            if t == "template_string":
                result = ""
                for child in node.children:
                    if child.type == "string_fragment":
                        result += EndpointsMiner.get_text( child, src )
                    elif child.type == "template_substitution":
                        expr = child.named_children[ 0 ]
                        result += str( self.resolve(expr, src, local_vars, depth+1, visited) )
                    else:
                        result += str( self.resolve(child, src, local_vars, depth+1, visited) )
                return result.strip( "`" )

            if t == "object":
                obj = {}
                for child in node.children:
                    if child.type == "pair":
                        k = child.child_by_field_name( "key" )
                        v = child.child_by_field_name( "value" )
                        key = EndpointsMiner.get_text( k, src ).strip( '"\'' )
                        # use scope-aware resolution
                        # obj[ key ] = self.resolve( v, src, local_vars, depth+1 )
                        obj[ key ] = lambda src=src, lv=local_vars, node=v: self.resolve( node, src, lv, depth+1, visited )
                return obj

            if t == "array":
                return [ self.resolve(c, src, local_vars, depth+1, visited) for c in node.named_children ]

            # FUNCTION CALL
            if t == "call_expression":
                func_node = node.child_by_field_name( "function" )
                args_node = node.child_by_field_name( "arguments" )
                if func_node:
                    fname = EndpointsMiner.get_text( func_node, src ).strip()
                    if fname in self._functions:
                        return self._resolve_function( fname, args_node, src, local_vars )
                    # fallback for unknown calls: resolve args
                    # resolved_args = [ self.resolve(a, src, local_vars, depth+1, visited) for a in args_node.named_children ] if args_node else []
                    # return f"{fname}({', '.join(map(str, resolved_args))})"
                    return None

            # Member expressions like -> obj.prop
            if t == "member_expression":
                parts = []
                current = node
                while current and current.type == "member_expression":
                    prop = current.child_by_field_name( "property" )
                    parts.insert( 0, EndpointsMiner.get_text(prop, src) )
                    current = current.child_by_field_name( "object" )
                if current:
                    # resolve root object with scope awareness
                    root_val = self.resolve( current, src, local_vars, depth+1 )
                    while isinstance( root_val, str ) and root_val in self._variables:
                        root_val = self._variables[ root_val ]
                    parts.insert( 0, root_val )
                return self._resolve_chain( parts )
            
            if t == "this": # Crazy thing but it works: I don't know WHY THE FUCK "this" doesn't treated as identifier
                return local_vars.get( t, self._variables.get(t, t) )

            # FALLBACK: raw text
            return EndpointsMiner.get_text( node, src )

        # This method responsible for handles sh1ts like, x=10, y=x, where y is the same f*cking x
        def _resolve_alias(self, name):
            visited = set()
            while name in self._aliases:
                if name in visited:
                    break
                visited.add(name)
                name = self._aliases[name]
            return name

        # Member chain resolution like -> obj.a.b.c
        def _resolve_chain(self, parts):
            if not parts:
                return None
            
            value = self.unwrap( parts[0] )

            for p in parts[1:]:
                value = self.unwrap( value )
                if isinstance(value, dict):
                    value = value.get( p )
                    # child = value.get( p )
                    # if child is None:
                    #     return f"{value}.{p}"
                    # # lazy evaluation
                    # if callable(child):
                    #     child = child()
                    #     value[p] = child  # cache resolved value
                    # value = child
                else:
                    # return f"{value}.{p}"
                    return None
                
            # # Final resolution if still not resolved
            # if callable( value ):
            #     value = value()

            return self.unwrap( value )

        def _resolve_function(self, fname, args_node, src, outer_scope=None):
            if fname not in self._functions:
                return None
    
            fn = self._functions[ fname ]
            local_vars = ( outer_scope or {} ).copy()

            if "this" not in local_vars:
                local_vars[ "this" ] = {}

            # map args to parameters
            if args_node:
                for i, arg in enumerate( args_node.named_children ):
                    if i < len( fn["params"] ):
                        local_vars[ fn["params"][i] ] = self._resolve_with_scope( arg, src, outer_scope or {} )

            # find return statement
            def find_return(node):
                if node.type == "return_statement":
                    val = node.child_by_field_name( "value" )
                    if val:
                        return self._resolve_with_scope( val, src, local_vars )
                for c in node.children:
                    r = find_return( c )
                    if r is not None:
                        return r
                return None

            return find_return( fn["body"] )

        # Scope-aware node resolution
        def _resolve_with_scope(self, node, src, local_vars):
            if node is None:
                return None

            # backup global vars
            original_vars = self._variables.copy()

            try:
                # inject local scope into global scope temporarily
                if local_vars:
                    self._variables.update( local_vars )

                return self.resolve( node, src, local_vars )

            finally:
                self._variables = original_vars


    def __init__(self, config: Config, crawler_result):
        self._endpoints = {}
        self._crawler_result = crawler_result
        self._config = config

        JS_LANGUAGE = Language( javascript.language() )
        self._parser = Parser( JS_LANGUAGE )
        self._parser.logger = None

    def collect_functions(self, node, src, resolver):

        if node.type == "function_declaration":
            name_node = node.child_by_field_name( "name" )
            params_node = node.child_by_field_name( "parameters" )
            body_node = node.child_by_field_name( "body" )

            if name_node and body_node:
                name = EndpointsMiner.get_text( name_node, src )
                params = []

                if params_node:
                    for p in params_node.named_children:
                        params.append( EndpointsMiner.get_text(p, src) )

                resolver._functions[ name ] = {
                    "params": params,
                    "body": body_node
                }

        for c in node.children:
            self.collect_functions( c, src, resolver )

    def collect_variables(self, root, src, resolver):
        def visit(node):
            if node.type == "variable_declarator":
                name = node.child_by_field_name( "name" )
                value = node.child_by_field_name( "value" )

                if name and value:
                    var_name = EndpointsMiner.get_text( name, src )
                    resolver.insert( var_name, resolver.resolve(value, src) )

            elif node.type == "assignment_expression":
                left = node.child_by_field_name( "left" )
                right = node.child_by_field_name( "right" )

                # obj.prop = value
                if left.type == "member_expression":
                    parts = []

                    current = left
                    while current and current.type == "member_expression":
                        prop = current.child_by_field_name( "property" )
                        parts.insert( 0, EndpointsMiner.get_text(prop, src) )
                        current = current.child_by_field_name( "object" )

                    if current:
                        root_name = EndpointsMiner.get_text( current, src )

                        # ensure root is a dict
                        existing = resolver.get( root_name )

                        if not isinstance( existing, dict ):
                            resolver.insert( root_name, {} )
                            
                        obj = resolver.get( root_name )

                        # build nested safely
                        for p in parts[ :-1 ]:
                            child = obj.get( p )
                            if callable( child ):
                                child = resolver.unwrap( child )
                                obj[ p ] = child
                            if not isinstance( child, dict ):
                                obj[ p ] = {}
                            obj = obj[ p ]

                        # assign final value
                        obj[ parts[-1] ] = (
                            lambda right=right, src=src, resolver=resolver:
                                resolver.resolve( right, src )
                        )

                # variable = value
                elif left.type == "identifier":
                    name = EndpointsMiner.get_text( left, src )
                    # alias case: let a = b;
                    if right.type == "identifier":
                        target = EndpointsMiner.get_text( right, src )
                        resolver._aliases[ name ] = target
                    else:
                        resolver.insert( name, value )

            for c in node.children:
                visit( c )

        visit( root )

    def extract_requests(self, root, src, resolver):
        results = []
        xhr_map = {}  # track xhr instances

        def visit(node):
            if node.type == "call_expression":
                func = node.child_by_field_name( "function" )
                args = node.child_by_field_name( "arguments" )

                if not func:
                    return

                func_name = EndpointsMiner.get_text( func, src )

                if func_name == "fetch":
                    url = None
                    method = "GET"
                    headers = {}
                    params = []

                    if args and args.named_child_count >= 1:
                        url = resolver.unwrap( resolver.resolve(args.named_children[0], src) )

                    if args and args.named_child_count >= 2:
                        opts = resolver.unwrap( resolver.resolve(args.named_children[1], src) )

                        if isinstance( opts, dict ):
                            method = opts.get( "method", method ).upper()
                            headers = opts.get( "headers", {} )
                            params = self.dict_to_params( opts.get("body", {}) )
                        
                    results.append({
                        "method": "fetch",
                        "url": url,
                        "m_type": method,
                        "headers": headers,
                        "params": params
                    })

                elif "axios" in func_name:
                    method = func_name.split( '.' )[ -1 ].upper()
                    url = None
                    headers = {}
                    params = []
                    data = {}

                    if args and args.named_child_count >= 1:
                        url = resolver.unwrap( resolver.resolve(args.named_children[0], src) )

                    if args and args.named_child_count >= 2:
                        cfg = resolver.unwrap( resolver.resolve(args.named_children[1], src) )

                        if isinstance( cfg, dict) :
                            headers = cfg.get( "headers", {} )
                            data = cfg.get( "data", {} )
                            params = self.dict_to_params( cfg.get("params", {}) )

                    results.append({
                        "method": "axios",
                        "m_type": method,
                        "url": url,
                        "headers": headers,
                        "params": params,
                        "body": data
                    })

                # XHR HANDLING (STATEFUL)
                # xhr.open(method, url)
                elif ".open" in func_name:
                    obj = func_name.split( "." )[ 0 ]

                    if args and len(args.named_children) >= 2:
                        method = resolver.resolve( args.named_children[0], src ).upper()
                        url = resolver.resolve( args.named_children[1], src )

                        xhr_map.setdefault( obj, {} )
                        xhr_map[ obj ][ "method" ] = method
                        xhr_map[ obj ][ "url" ] = url
                        xhr_map[ obj ].setdefault( "headers", {} )

                # xhr.setRequestHeader(k, v)
                elif ".setRequestHeader" in func_name:
                    obj = func_name.split( "." )[ 0 ]

                    if args and len(args.named_children) >= 2:
                        key = resolver.resolve( args.named_children[0], src )
                        val = resolver.resolve( args.named_children[1], src )

                        xhr_map.setdefault( obj, {} )
                        xhr_map[ obj ].setdefault( "headers", {} )
                        xhr_map[ obj ][ "headers" ][ key ] = val

                # xhr.send(body)
                elif ".send" in func_name:
                    obj = func_name.split( "." )[ 0 ]

                    body = None
                    if args and args.named_child_count >= 1:
                        body = resolver.unwrap( resolver.resolve(args.named_children[0], src) )

                    if obj in xhr_map:
                        if not isinstance( body, dict ):
                            body = {}

                        params = self.dict_to_params( body )

                        # finalize request
                        results.append({
                            "method": "xhr",
                            "url": xhr_map[obj].get("url"),
                            "m_type": xhr_map[obj].get("method"),
                            "headers": xhr_map[obj].get("headers", {}),
                            "params": params
                        })

            for c in node.children:
                visit( c )

        visit( root )
        return results

    def validate(self, results):
        valid_results = []

        for result in results:
            url = result.get( 'url' )
            m_type = result.get( 'm_type', 'GET' ).upper()

            # Skip if URL is None or empty
            if not url or not isinstance( url, str ) or not url.strip():
                continue

            url = url.strip()

            # Validate URL with regex (LINK_EXTRACTOR should match normal URLs)
            if not re.match( LINK_EXTRACTOR, f"\"{url}\"", re.VERBOSE ):    
                continue  # skip invalid URLs

            # Allow relative URLs starting with /
            if url.startswith( "/" ):
                url = urllib.parse.urljoin( self._config.GetTarget(), url )

            # Ensure method is GET or POST
            if m_type not in ( "GET", "POST" ):
                m_type = "GET"

            result[ 'url' ] = url
            result[ 'm_type' ] = m_type

            valid_results.append( result )

        return valid_results
    
    def scan_js_url(self, js_file_url):
        try:
            code = Get( js_file_url, headers=self._config.GetHeaders(), proxy=self._config.GetProxy() ).Send( timeout=10 ).content
            return self.scan_js( code )
        except:
            return []
        
    def scan_js(self, code):
        
        try:
        
            # Large JS file cause constructing too large AST/CST
            # which ultimately results in the process being killed by the operating system.
            if EndpointsMiner.is_large_js( code ):
                return []
                    
            with EndpointsMiner.suppress_tree_sitter_warnings():
                tree = self._parser.parse( code )

            resolver = EndpointsMiner.Resolver()
            self.collect_functions( tree.root_node, code, resolver )
            self.collect_variables( tree.root_node, code, resolver )
            results = self.extract_requests( tree.root_node, code, resolver )
            return self.validate( results )
        
        except:
            return []
    
    def scan_html(self, endpoint):
        all_results = []
        
        try:
            r = EndPoint.Load( endpoint ).GetRequester( self._config.GetHeaders(), self._config.GetProxy() )
            html = r.Send( timeout=10 ).content
            if b"<html" in html:
                js_blocks = self.extract_js_from_html( html )

                for js in js_blocks:
                    results = self.scan_js( js.encode("utf-8") )
                    all_results.extend( results )

            return all_results
        except:
            return all_results
    
    def extract_js_from_html(self, html_content):
        soup = BeautifulSoup( html_content, "html.parser" )
        scripts = []

        # <script> blocks
        for script in soup.find_all( "script" ):
            if script.string:
                scripts.append( textwrap.dedent(script.string) )

        # inline event handlers
        for tag in soup.find_all():
            for attr, val in tag.attrs.items():
                if attr.startswith( "on" ):  # onclick, onload, etc.
                    scripts.append( val )

        return scripts
    
    def Start(self):
        features = []

        with ThreadPoolExecutor( max_workers=self._config.GetThreads() ) as executor:
            features.extend( [executor.submit(self.scan_js_url, js) for js in self._crawler_result.GetJsFiles()] )
            features.extend( [executor.submit(self.scan_html, e) for e in self._crawler_result.GetEndPoints()] )

        return [ result for feature in features for result in feature.result() ]
    
    def dict_to_params(self, d):
        params = []

        if isinstance( d, dict ):
            for k, v in d.items():
                params.append({
                    "name": k,
                    "value": v,
                    "p_type": ""
                })

        return params

    @classmethod
    def get_text(cls, node, src):
        return src[ node.start_byte:node.end_byte ].decode( "utf-8", errors="ignore" ) if node else ""

    @classmethod
    @contextmanager
    def suppress_tree_sitter_warnings(cls):
        stderr_fd = sys.stderr.fileno()
        saved_stderr_fd = os.dup( stderr_fd )

        try:
            with open( os.devnull, 'w' ) as devnull:
                os.dup2( devnull.fileno(), stderr_fd )
            yield
        finally:
            os.dup2( saved_stderr_fd, stderr_fd )
            os.close( saved_stderr_fd )

    @classmethod
    def is_large_js(cls, code, max_size_kb=512, max_lines=5000):
        if code is None:
            return False

        if isinstance( code, str ):
            raw_bytes = code.encode( "utf-8", errors="ignore" )
            text = code
        else:
            raw_bytes = code
            text = code.decode( "utf-8", errors="ignore" )

        size_kb = len( raw_bytes ) / 1024
        if size_kb > max_size_kb:
            return True

        if text.count( "\n" ) > max_lines:
            return True

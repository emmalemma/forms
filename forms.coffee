path = require 'path'
@App = 
	paradigm_version: "0.2.0"
	
	port: 			8007
	app_dir:		dir= 			'/Users/adrian/Projects/forms'
	private_dir: 	path.join dir, 	'private'
	public_dir: 	path.join dir, 	'public'
	client_cs_dir: 	path.join dir, 	'private/cs/'
	client_js_dir: 	path.join dir, 	'public/js/'
	server_code: 	path.join dir, 	"server.coffee"
	
	db:
		adapter: 	'couchdb'
		host: 		'cushman.cloudant.com'
		port: 		80
		api_key: 	'parenignodscuryouldrerve' #api key with admin access
		secret:		'xxSpEupF4O8DfL4r1y5tvBVT'
		views: 		path.join dir, 	"views.coffee"
		
	client_lib:		'jquery'
	
	middlewares:
		functions:
			match:		/^\/\$\/(.+)/
			prefix:		'\$'
			client:		yes
			
		sessions:
			client: 	no

		paperboy:
			mimetypes:
				svg: 'image/svg+xml'
		
		
		
		
@Watcher =
	dir:		dir
	verbose: 	no
	process: 	"paradigm"
	args: 		["forms"]
	timeout:	300					#seems like a good balance between cpu and response
	ignore: 	[
					'.git'
					'.DS_Store'
					/.+\/public\/.+/ #fun little loop here
					/^\./			#anything that starts in . probably not necessary
					/\.tmp$/		#same for .tmps
					/\.swp$/		#good joke vim	
			]
	

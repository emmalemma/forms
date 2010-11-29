path = require 'path'
@App = 
	paradigm_version: "0.2.0"
	
	port: 			8007
	app_dir:		dir= 			'/home/ec2-user/app/forms'
	private_dir: 	path.join dir, 	'private'
	public_dir: 	path.join dir, 	'public'
	client_cs_dir: 	path.join dir, 	'private/cs/'
	client_js_dir: 	path.join dir, 	'public/js/'
	server_code: 	path.join dir, 	"server.coffee"
	
	db:
		adapter: 	'couchdb'
		host: 		'cushman.cloudant.com'
		port: 		80
		name: 		''
		views: 		path.join dir, 	"views.coffee"
		
	middlewares:
		functions:
			match:		/^\/\$\/(.+)/
			prefix:		'\$'
			client:		yes
			
		sessions:
			client: 	yes

		paperboy:  	true
		
		
@Watcher =
	dir:		dir
	verbose: 	no
	process: 	"paradigm"
	args: 		["forms"]
	timeout:	300					#seems like a good balance between cpu and response
	ignore: 	[
					'.git'
					/.+\/public\/.+/ #fun little loop here
					/^\..+/			#anything that starts in . probably not necessary
					/\.tmp$/		#same for .tmps
					/\.swp$/		#good joke vim	
			]
	


from project import app


if __name__ == '__main__':
	app.run()
    #app.run(host='0.0.0.0', ssl_context=('tmp/cert.crt', 'tmp/key.key'), port=5000)
   	#app.run(host='0.0.0.0', debug=True, port=1025, ssl_context=('tmp/cert.crt','tmp/key.key'))


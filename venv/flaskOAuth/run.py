
from project import app


if __name__ == '__main__':
	#app.run(host='0.0.0.0', port=8080)
    app.run('0.0.0.0', debug=True, port=8080, ssl_context=('tmp/cert.crt', 'tmp/key.key'))



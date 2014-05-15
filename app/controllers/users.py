from bottle import get

@get('/users')
@get('/users/<page:int>')
def index(page=0):
	pass

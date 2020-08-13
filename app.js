require('dotenv').config()

const http = require('http')
const express = require('express')
const path = require('path')
var debug = require('debug')('server:server');

require('./models/db')

const app = express()

var port = process.env.PORT || '3000'
app.set('port', port);

const authRouter = require('./routes/auth')
const userRouter = require('./routes/user')

app.use(express.json())
app.use(express.urlencoded({ extended: false }))
app.use(express.static(path.join(__dirname, 'public/_site')))

app.get('/', (req, res) => {
    console.log('ye')
    return res.sendFile('index.html')
})

app.use('/', authRouter)
app.use('/user', userRouter)


// catch 404 and forward to error handler
app.use(function(req, res, next) {
    next(createError(404))
})

// error handler
app.use(function(err, req, res, next) {
    // set locals, only providing error in development
    res.locals.message = err.message
    res.locals.error = req.app.get('env') === 'development' ? err : {}

    // render the error page
    return res.status(err.status || 500).json(err.status)
})

// http server creation

server = http.createServer(app)

server.listen(port)
server.on('error', onError)
server.on('listening', onListening)

function onError(error) {
    if (error.syscall !== 'listen') {
        throw error
    }

    var bind = typeof port === 'string'
        ? 'Pipe ' + port
        : 'Port ' + port

    // handle specific listen errors with friendly messages
    switch (error.code) {
        case 'EACCES':
        console.error(bind + ' requires elevated privileges')
        process.exit(1)
        break;
        case 'EADDRINUSE':
        console.error(bind + ' is already in use')
        process.exit(1)
        break
        default:
        throw error
    }
}

/**
 * Event listener for HTTP server "listening" event.
 */

function onListening() {
    var addr = server.address()
    var bind = typeof addr === 'string'
        ? 'pipe ' + addr
        : 'port ' + addr.port
    debug('Listening on ' + bind)
}
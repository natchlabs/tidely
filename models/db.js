const mongoose = require('mongoose')
mongoose.set('useCreateIndex', true)

const dbURI = (process.env.JEST_WORKER_ID == undefined ? process.env.DB_URI : process.env.LOCAL_DB_URI)
mongoose.connect(dbURI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
})

mongoose.connection.on('connected', () => {
    console.log(`Mongoose connected to ${dbURI}`)
})
mongoose.connection.on('error', err => {
    console.log(`Mongoose connection error: ${err}`)
})
// mongoose.connection.on('disconnected', () => {
//     console.log(`Mongoose disconnected`)
// })

// function to close the mongoose connection
function gracefulShutdown(msg, callback) {
    mongoose.connection.close(() => {
        console.log(`Mongoose disconnected through ${msg}`)
        callback()
    })
}

// nodemon shutdown signal
process.once('SIGUSR2', () => {
    gracefulShutdown('nodemon restart', () => {
        process.kill(process.pid, 'SIGUSR2')
    })
})
// general application shutdown signal
process.on('SIGINT', () => {
    gracefulShutdown('app termination', () => {
        process.exit(0)
    })
})
// heroku shutdown signal
process.on('SIGTERM', () => {
    gracefulShutdown('Heroku app shutdown', () => {
        process.exit(0)
    })
})

require('./user')
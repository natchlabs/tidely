const bcrypt = require('bcrypt')
const jwt = require('jsonwebtoken')

const validate = require('./validate')
const User = require('mongoose').model('User')

async function register(req, res) {
    console.log(JSON.stringify(req.body))
    const val = validate.isUser(req.body)
    if(!val.success) return res.status(400).json(val.error.details[0].message)

    const emailInUse = await User.findOne({ email: req.body.email })
    if(emailInUse) return res.status(400).json('Email already exists.')

    const salt = await bcrypt.genSalt(10) // most likely too low for production
    const hashedPassword = await bcrypt.hash(req.body.password, salt)

    const user = new User({
        email: req.body.email,
        password: hashedPassword
    })
    try {
        await user.save()
        const token = jwt.sign({ _id: user._id }, process.env.TOKEN_SECRET)
        return res.header('auth-token', token).send()
    }
    catch (err) {
        return res.status(400).json(err)
    }
}

async function login(req, res) {
    const { error } = validate.isUser(req.body)
    if(error) return res.status(400).json(error.details[0].message)

    const user = await User.findOne({ email: req.body.email })
    if(!user) return res.status(400).json({ message: 'Email or password incorrect.' })

    const isValidPassword = await bcrypt.compare(req.body.password, user.password)
    if(!isValidPassword) return res.status(400).json({ message: 'Email or password incorrect.' })

    const token = jwt.sign({ _id: user._id }, process.env.TOKEN_SECRET)
    return res.header('auth-token', token).send()
}

async function authorise(req, res, next) {
    const token = req.header('auth-token')
    if(!token) return res.status(401).json('Access denied; no token provided.')

    try {
        const authorised = jwt.verify(token, process.env.TOKEN_SECRET)
        req.payload = authorised
        next()
    }
    catch (err) {
        return res.status(400).json({ message: 'Access denied; invalid token.' })
    }
}

module.exports = {
    register,
    login,
    authorise
}
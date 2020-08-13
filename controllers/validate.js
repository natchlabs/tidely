const Joi = require('@hapi/joi')
Joi.objectId = require('joi-objectid')(Joi)

function isValid(schema) {
    return function(source) {
        const { error } = schema.validate(source)
        if(error) {
            return { success: false, error }
        }
        return { success: true, error: null }
    }
}

const userSchema = Joi.object({
    email: Joi.string().email().required(),
    password: Joi.string()
})
const idSchema = Joi.object({
    _id: Joi.objectId().required()
})

module.exports = {
    isUser: isValid(userSchema),
    isId: isValid(idSchema)
}
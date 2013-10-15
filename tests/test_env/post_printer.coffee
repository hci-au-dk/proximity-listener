express = require 'express'

app = express()
app.use express.bodyParser()

app.post '/', (req, res) ->
    console.log req.body
    res.send 'Thanks'
  
app.listen(3000)
 
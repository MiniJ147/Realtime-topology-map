const express = require('express');
const app = express();

const fs = require('fs')
const stream = require('stream')

const port = process.argv[2] || 8080;

let inputRoute = "";
let outputRoute = "";

function loadFile(filePath) {
    const r = fs.createReadStream(filePath); 
    const ps = new stream.PassThrough() 
    stream.pipeline(
    r,
    ps,
    (err) => {
        if (err) {
            return err; 
        }
    })

    return ps;
}

app.get("/",(req,res)=>{
    res.send({
        "reloadConfig": "/reload",
        "inputRoute": "/input",
        "outputRoute": "/output",
    })
})
app.get("/input",(req,res)=>{
    try{
        ps = loadFile(inputRoute);
        ps.pipe(res)
    }catch(e){
        return res.status(400).send(e); 
    }
})

app.get("/output",(req,res)=>{
    try{
        ps = loadFile(outputRoute);
        ps.pipe(res)
    }catch(e){
        return res.status(400).send(e); 
    }
})

app.get("/reload",(req,res)=>{
    config = require('./config.json');
    inputRoute = config.inputFileDir;
    outputRoute = config.outFileDir;

    res.send({
        "newInputRoute": inputRoute,
        "newOutputRoute": outputRoute
    })
})

app.listen(port,()=>{
    config = require('./config.json');
    inputRoute = config.depthFileDir;
    outputRoute = config.outFileDir;

    console.log("running on port: ",port);
})
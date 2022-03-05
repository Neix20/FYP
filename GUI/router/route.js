const express = require('express');
const fs = require('fs');
const path = require('path');
const multer = require('multer');
const upload = multer({ dest: "Dataset/" });
const { spawn } = require('child_process');
const router = express.Router();

router.get('/', (req, res) => {
    res.sendFile(`${__dirname}/public/index.html`);
});

router.post('/uploadCSV', upload.single('ePaymentDataset'), (req, res) => {
    // Rename File
    fs.rename(`${req.file.path}`, `Dataset\\${req.file.originalname}`, _ => {});

    let python = spawn('python', ['gen_corr_img.py', req.file.originalname]);
    // collect data from script
    python.stdout.on('data', _ => {
        console.log("Running")
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', () => {});

    return res.status(200).json({ msg: "Success!" });
});

module.exports = router;
const express = require('express');
const fs = require('fs');
const path = require('path');
const multer = require('multer');
const upload = multer({ dest: "Dataset/" });
const spawnSync = require('child_process').spawnSync;
const router = express.Router();

router.get('/', (req, res) => {
    res.sendFile(`${__dirname}/public/index.html`);
});

router.post('/uploadCSV', upload.single('ePaymentDataset'), (req, res) => {

    var fileName = req.file.originalname,
        feat_col_arr = [];
    // Rename File
    fs.rename(`${req.file.path}`, `Dataset\\${fileName}`, _ => {});

    let python = spawnSync('python', ['Python-Executables\\script.py', fileName]);

    // collect data from script
    feat_col_arr = python.stdout.toString().split("->");

    return res.status(200).json({ msg: `Successfully added ${fileName}!`, feature_columns: feat_col_arr });
});

module.exports = router;
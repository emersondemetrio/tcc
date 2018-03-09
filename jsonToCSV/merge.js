// https://github.com/bahmutov/csv-pair

const fs = require('fs');
const process = require('process');
const resolve = require('path').resolve
const jsonexport = require('jsonexport');
const csvPair = require("csv-pair");

const folderPath = "./output";

// npm run merge

console.log("Reading: ", folderPath);
const outputFile = resolve("./", "merge.csv");

fs.readdir(folderPath, (err, files) => {
	const csvFiles = files.filter(file => file !== ".gitkeep").map(file => resolve(folderPath, file));
	csvPair(csvFiles, outputFile);
});

// http://kauegimenes.github.io/jsonexport/

const fs = require('fs');
const process = require('process');
const resolve = require('path').resolve
var jsonexport = require('jsonexport');

const folderPath = process.argv[2];

// npm start /home/emerson/projects/tcc/input # for example

console.log("Reading: ", folderPath);

const parseJsonFile = (inputPath, outputPath) => {
	const input = fs.createReadStream(inputPath, { encoding: 'utf8' });
	const output = fs.createWriteStream(outputPath, { encoding: 'utf8' });

	input.pipe(jsonexport()).pipe(output);
}

fs.readdir(folderPath, (err, files) => {

	files.forEach(file => {

		const inputPath = resolve(folderPath, file);
		const outputPath = resolve("./", "output", file.replace(".json", ".csv"));
		console.log(`From ${inputPath} to ${outputPath}`);

		parseJsonFile(inputPath, outputPath);
	});
});

const process = require('process');
const fs = require('fs');
const resolve = require('path').resolve
const Json2csvTransform = require('json2csv').Transform;

const folderPath = process.argv[2];

console.log("Reading: ", folderPath);

const parseJsonFile = (inputPath, outputPath) => {

	const fields = ['field1', 'field2', 'field3'];
	const opts = {
		fields
	};

	const transformOpts = {
		highWaterMark: 16384,
		encoding: 'utf-8'
	};

	const input = fs.createReadStream(inputPath, { encoding: 'utf8' });
	const output = fs.createWriteStream(outputPath, { encoding: 'utf8' });
	const json2csv = new Json2csvTransform({}, transformOpts);

	const processor = input.pipe(json2csv).pipe(output);

	// You can also listen for events on the conversion and see how the header or the lines are coming out.
	json2csv
		.on('header', header => console.log(header))
		.on('line', line => console.log(line))
		.on('error', err => console.log(err));
}

fs.readdir(folderPath, (err, files) => {
	files.forEach(file => {
		const inputPath = resolve(folderPath, file);
		const outputPath = resolve("./", "output", file.replace(".json", ".csv"));
		parseJsonFile(inputPath, outputPath);
	});
});

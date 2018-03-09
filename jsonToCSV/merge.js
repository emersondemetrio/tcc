// https://github.com/bahmutov/csv-pair

const fs = require('fs');
const process = require('process');
const resolve = require('path').resolve;

// npm run merge

const folderPath = "./output";
const outputFile = resolve("./", "merged.csv");

const read = (file, callback) => {
	fs.readFile(file, 'utf8', function (err, data) {
		if (err) {
			console.log(err);
		}
		callback(data);
	});
}

const write = (content) => {
	fs.appendFile(outputFile, content, (err) => {
		if (err) {
			console.log("Error", err);
		} else {
			console.log("Done.");
		}
	});
}

fs.readdir(folderPath, (err, files) => {
	const csvFiles = files
		.filter(file => file !== ".gitkeep")
		.map(file => resolve(folderPath, file));
	let times = 0;

	csvFiles.forEach((path) => {
		read(path, (data) => {
			if (times === 0) {
				write(data.split("\n")[0]);
			}
			write(data.split("\n")[1]);
			times++;
		});
	});
});

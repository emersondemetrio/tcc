// TODO

// using db.mir.id
// update music add field mfcc
// read results and update mfcc
// ...

const fs = require('graceful-fs');
const process = require('process');
const resolvePath = require('path').resolve
const mysql = require('mysql');

// npm start /home/emerson/projects/tcc/input # for example

const connection = mysql.createConnection({
	host: 'localhost',
	user: 'root',
	password: '123',
	database: 'mir'
});

connection.connect();

const DIR_PATH = process.argv[2];
const MAX = process.argv[3] ? parseInt(process.argv[3]) : 20000;
const ERROR_LOG = resolvePath(__dirname, 'error.log');

const readDirPromise = (path) => new Promise((resolve, reject) => {
	fs.readdir(path, (err, files) => {
		if (err) {
			reject(err);
		} else {
			const absFiles = [];
			let count = 0;

			files.forEach(file => {
				(count < MAX) && absFiles.push({
					id: file.replace('.json', ''),
					path: resolvePath(path, file)
				});
				count++;
			});

			resolve(absFiles);
		}
	});
});

const readFilePromise = (pathModel) => new Promise((resolve, reject) => {
	fs.readFile(pathModel.path, 'utf8', (err, data) => {
		if (err) {
			reject(err);
		} else {
			resolve({
				id: pathModel.id,
				data: JSON.parse(data)
			});
		}
	});
});

const updateMir = (id, parsedFile, index) => {
	const mfcc = parsedFile.lowlevel.mfcc.mean.join(';');
	// for MUSIC
	// const UPDATE_QUERY = `UPDATE music SET mfcc = '${mfcc}' WHERE id = '${id}';`;
	// for MUSIC_TEST
	const UPDATE_QUERY = `UPDATE music_test SET mfcc = '${mfcc}' WHERE id = '${id}';`;

	connection.query(UPDATE_QUERY, (error, results, fields) => {
		if (error) {
			console.log(error);
		} else {
			console.log(`Results [index: ${index}] =`, results.affectedRows);
		}
	});
}

readDirPromise(DIR_PATH).then((absFiles) => {
	const files = absFiles.map(absfilePath => readFilePromise(absfilePath));

	Promise
		.all(files)
		.then(parsedFiles => {

			parsedFiles.forEach((parsed, index) => {
				updateMir(parsed.id, parsed.data, index);
			});

			connection.end();
		}).catch((err) => {
			console.log("ERR", err);
		});
}).catch((err) => {
	console.log("ERR", err);
});

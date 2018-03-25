const fs = require('fs');
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
const MAX = process.argv[3] ? parseInt(process.argv[3]) : 1000;
const ERROR_LOG = resolvePath(__dirname, 'error.log');

const _s = (string) => {
	return connection
		.escape(string)
		.replace(/'/g, "")
		.replace(/-/g, " ")
		.replace(/\\/g, "")
		.replace(/\//g, " ")
		.trim();
}

const _g = (string) => {
	const rawGenre = (string.split(',')[0]).toLocaleLowerCase();

	if (rawGenre === 'rock n roll' || rawGenre === 'rock & roll') {
		return 'rock and roll';
	}

	if (rawGenre === 'thrash metal') {
		return 'trash metal';
	}

	if (rawGenre === 'rock/pop') {
		return 'rock pop';
	}

	if (rawGenre === 'pop/rock') {
		return 'pop rock';
	}

	if (rawGenre === 'folk/rock') {
		return 'folk rock';
	}

	if (rawGenre === 'ethereal wave') {
		return 'ethereal';
	}

	if (rawGenre === 'hard rock. heavy metal') {
		return 'hard rock';
	}

	if (rawGenre.indexOf('progressive') > -1) {
		return 'progressive';
	}

	if (rawGenre === 'dance & dj' || rawGenre === 'dance punk') {
		return 'dance';
	}

	if (rawGenre === 'acoustic rock') {
		return 'acoustic';
	}

	if (rawGenre === 'alt. rock') {
		return 'alternative rock';
	}

	if (rawGenre === 'electronic music') {
		return 'electronic';
	}

	if (rawGenre === 'proto punk') {
		return 'protopunk';
	}

	if (rawGenre === 'electronica') {
		return 'electronic';
	}

	if (rawGenre === 'garage rock revival') {
		return 'garage rock';
	}

	if (rawGenre === 'general rock') {
		return 'rock';
	}

	if (rawGenre === 'hark rock') {
		return 'hard rock';
	}

	if (rawGenre === 'avant garde jazz' || rawGenre === 'avante garde folk'
		|| rawGenre === 'avantgarde rock'
	) {
		return 'avantgarde';
	}

	if (rawGenre === 'country rock') {
		return 'country'
	}

	return rawGenre;
}

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

const insertMusic = (id, parsedFile, index) => {
	const INSERT_QUERY = `INSERT INTO music (
		id,
		name,
		album,
		artist,
		genre,
		average_loudness,
		bpm,
		beats_loudness_mean,
		danceability,
		chords_changes_rate,
		chords_number_rate,
		extra
	) VALUES (
		'${id}',
		'${_s(parsedFile.metadata.tags.title ? parsedFile.metadata.tags.title[0] : 'unknown')}',
		'${_s(parsedFile.metadata.tags.album ? parsedFile.metadata.tags.album[0] : 'unknown')}',
		'${_s(parsedFile.metadata.tags.artist ? parsedFile.metadata.tags.artist[0] : 'unknown')}',
		'${_g(_s(parsedFile.metadata.tags.genre ? parsedFile.metadata.tags.genre[0] : 'unknown'))}',
		'${parsedFile.lowlevel.average_loudness}',
		'${parsedFile.rhythm.bpm}',
		'${parsedFile.rhythm.beats_loudness.mean}',
		'${parsedFile.rhythm.danceability}',
		'${parsedFile.tonal.chords_changes_rate}',
		'${parsedFile.tonal.chords_number_rate}',
		'${parsedFile.tonal.key_strength}'
	);`;

	connection.query(INSERT_QUERY, (error, results, fields) => {
		if (error) {
			console.log(error.message);

			if (error.code !== 'ER_DUP_ENTRY') {
				console.log(INSERT_QUERY, error.code);

				const errorLog = `code: ${error.code}
				msg: ${error.message}
				query: ${INSERT_QUERY}`;

				fs.appendFile(ERROR_LOG, errorLog, (err) => {
					if (err) throw err;
				});
			}
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
				insertMusic(parsed.id, parsed.data, index);
			});

			connection.end();
		}).catch((err) => {
			console.log("ERR", err);
		});
}).catch((err) => {
	console.log("ERR", err);
});

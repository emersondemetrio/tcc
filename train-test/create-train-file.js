const fs = require('fs');
const process = require('process');
const resolvePath = require('path').resolve
const mysql = require('mysql');

const connection = mysql.createConnection({
	host: 'localhost',
	user: 'root',
	password: '123',
	database: 'mir'
});

connection.connect();

const MAX = process.argv[2] ? parseInt(process.argv[2]) : 1000;
const OUTPUT_FILE = resolvePath("./results", `train_${MAX}.csv`);
const HEADERS = [
	"average_loudness",
	"bpm",
	"beats_loudness_mean",
	"danceability",
	"chords_changes_rate",
	"chords_number_rate",
	...[...Array(13).keys()].map(n => `mfcc_${n + 1}`),
	"genre"
];

const HEADER = `${HEADERS.map(he => `"${he}"`).join(";")}\n`;

const appendGenreSetToTrain = (super_genre) => {
	const QUERY = `
		SELECT
			average_loudness,
			bpm_int AS bpm,
			beats_loudness_mean,
			(SELECT REPLACE(danceability_d, ',', '.')) AS danceability,
			chords_changes_rate,
			chords_number_rate,
			mfcc,
			super_genre AS genre
		FROM
			music
		WHERE
			super_genre = '${super_genre}'
		LIMIT ${MAX};
	`;

	connection.query(QUERY, (error, results, fields) => {
		if (error) {
			console.log(error.message);
		}

		let out = '';
		results.forEach((result) => {
			const parsedMFCC = result.mfcc.split(";");
			const resultList = [
				result.average_loudness,
				result.bpm,
				result.beats_loudness_mean,
				result.danceability,
				result.chords_changes_rate,
				result.chords_number_rate,
				...parsedMFCC,
				result.genre,
			];

			out += `${resultList.map(el => `"${el}"`).join(";")}\n`
		});

		fs.appendFileSync(OUTPUT_FILE, out);
		console.log(super_genre);
	});
}

const init = (id, parsedFile, index) => {

	const QUERY = `SELECT DISTINCT super_genre from music;`;

	connection.query(QUERY, (error, results, fields) => {
		if (error) {
			console.log(error.message);
		}

		results.forEach((result) => {
			appendGenreSetToTrain(result.super_genre);
		});
	});
}

fs.writeFile(OUTPUT_FILE, '', () => {
	fs.appendFileSync(OUTPUT_FILE, HEADER);
	init();
});

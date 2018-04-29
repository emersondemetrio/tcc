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

const PERCENT_LIMIT = process.argv[2] ? parseInt(process.argv[2]) : 30;
const OUTPUT_FILE = resolvePath("./results", `test_${PERCENT_LIMIT}.sql`);

const createTestSetPerGenre = (limit, super_genre) => {
	const QUERY = `SELECT * FROM music WHERE super_genre = '${super_genre}' LIMIT ${limit};`;

	connection.query(QUERY, (error, results, fields) => {
		if (error) {
			console.log(error.message);
		}

		let out = '';

		results.forEach((result) => {
			out += `INSERT INTO music_test SELECT * from music WHERE id = '${result.id}';\n`;
			out += `DELETE FROM music WHERE id = '${result.id}';\n`;
		});

		fs.appendFileSync(OUTPUT_FILE, out);
	});
}

const percent = (max) => {
	return parseInt(PERCENT_LIMIT * (max / 100));
}

const init = (id, parsedFile, index) => {

	const QUERY = `SELECT count(id) AS max, super_genre FROM music GROUP BY 2 ORDER BY 1 desc;`;

	connection.query(QUERY, (error, results, fields) => {
		if (error) {
			console.log(error.message);
		}

		results.forEach((result) => {
			createTestSetPerGenre(percent(result.max), result.super_genre);
		});
	});
}

fs.writeFile(OUTPUT_FILE, '', () => {
	fs.appendFileSync(OUTPUT_FILE, 'TRUNCATE TABLE music_test;\n');
	init();
});

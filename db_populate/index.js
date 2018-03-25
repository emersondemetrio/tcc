const mysql = require('mysql');

const connection = mysql.createConnection({
	host: 'localhost',
	user: 'root',
	password: '123',
	database: 'mir'
});

connection.connect();

connection.query('SELECT * FROM music', (error, results, fields) => {
	if (error) throw error;
	console.log('The solution is: ', results);
});

connection.end();

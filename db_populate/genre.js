module.exports = (artist) => {
	switch (artist.toLowerCase()) {
		case 'dredg':
			return 'progressive';

		case 'alex turner':
			return 'alternative rock';

		case 'duran duran':
			return 'new wave';

		case 'raul seixas':
			return 'rock';

		case 'Ramin Djawadi':
			return 'soundtrack';

		default:
			return 'unknown';
	}
}

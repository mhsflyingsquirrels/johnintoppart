#pragma once

#define err( r, ... ) \
do { \
	fprintf( stderr, "Error on line %d of file \"%s\":\n", __LINE__, __FILE__ ); \
	fprintf( stderr, __VA_ARGS__ ); \
	exit( r ); \
} while ( 0 )

#define warn( ... ) \
do { \
	fprintf( stderr, "Warning on line %d of file \"%s\":\n", __LINE__, __FILE__ ); \
	fprintf( stderr, __VA_ARGS__ ); \
} while ( 0 )


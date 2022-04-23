# Axione
Test Axione


# Install
First pull image `git clone git@github.com:llPekoll/Axione.git`  
Then on a machine with docker `docker-compose up --build`  


# Usage
The first endpoint `http//localhost:5000/init` will feed the database, this might take a while :/  
Second endpoint `http//localhost:5000/townfinder` will found the best town for you if you feed it with the good parameters ex: 
`
{
	"departement":11,
	"surface":50,
	"loyer_max":800
}
`
node('covid19-be') {

    checkout scm

    stage ('Build & Deploy')
        {
           sh '/usr/local/bin/docker-compose down -v'
           sh '/usr/local/bin/docker-compose up -d --build'
        }
}
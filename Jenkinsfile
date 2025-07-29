pipeline {
    agent any

    environment {
        // Database Configuration
        DB_PORT = '3306'
        DB_NAME = 'hospital_db'
        SQL_FILE = 'hospital_db_backup.sql'

        // Docker Configuration
        IMAGE_NAME = 'hospital_app_image'
        CONTAINER_NAME = 'hospital_app_container'
        APP_PORT = '5000'
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo '🔄 Cloning repository...'
                git branch: 'main', url: 'https://github.com/charannk007/Hospital_Management.git'
            }
        }

       stage('Deploy SQL to AWS RDS') {
    steps {
        echo '🟡 Deploying hospital_db_backup.sql to AWS RDS...'
        sh '''
            mysql -h database-1.czccaimeyk2a.ap-south-1.rds.amazonaws.com \
                  -P 3306 \
                  -u admin \
                  -p'admin1234' \
                  hospital_db < hospital_db_backup.sql
        '''
    }
}


        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh "docker build -t $IMAGE_NAME ."
            }
        }

        stage('Run Docker Container') {
            steps {
                echo '🚀 Running Docker container...'
                sh '''
                    docker rm -f $CONTAINER_NAME || true
                    docker run -d --name $CONTAINER_NAME -p 5000:5000 $IMAGE_NAME
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
            echo '🏥 App is running in Docker on port 5000'
        }
        failure {
            echo '❌ Pipeline failed - Check the logs for details'
        }
    }
}

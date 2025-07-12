pipeline {
    agent any

    environment {
        DB_PORT = '3306'
        DB_NAME = 'hospital_db'
        SQL_FILE = 'hospital_db_backup.sql'

        // DockerHub
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        IMAGE_NAME = 'nkcharan/hspmgmt'
        CONTAINER_NAME = 'hospital_app'
    }

    stages {

        stage('Clone Repository') {
            steps {
                echo '🔄 Cloning repository...'
                git branch: 'main', url: 'https://github.com/charannk007/Hospital_Management.git'
            }
        }
        stage('SonarQube Code Analysis') {
            steps {
                withSonarQubeEnv('MySonar') {
                    withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
                        sh """
                            sonar-scanner \
                            -Dsonar.login=$SONAR_TOKEN
                        """
                    }
                }
            }
        }

        stage('Deploy SQL to AWS RDS') {
            steps {
                withCredentials([
                    usernamePassword(credentialsId: 'mysql-rds-creds', usernameVariable: 'MYSQL_USER', passwordVariable: 'MYSQL_PASS'),
                    string(credentialsId: 'rds-endpoint', variable: 'DB_HOST')
                ]) {
                    sh '''
                        echo "🟡 Deploying hospital_db_backup.sql to AWS RDS..."
                        mysql -h $DB_HOST -P $DB_PORT -u $MYSQL_USER -p"$MYSQL_PASS" $DB_NAME < $SQL_FILE
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh "docker build -t $IMAGE_NAME:v1 ."
            }
        }

        stage('Login to Docker Hub') {
            steps {
                echo '🔐 Logging in to Docker Hub...'
                sh """
                    echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo '📤 Pushing image to Docker Hub...'
                sh "docker push $IMAGE_NAME:v1"
            }
        }

        stage('Run Docker Container') {
            steps {
                echo '🚀 Running Docker container on port 5000...'
                sh '''
                    docker stop $CONTAINER_NAME || true
                    docker rm $CONTAINER_NAME || true
                    docker run -d --name $CONTAINER_NAME -p 5000:5000 $IMAGE_NAME:v1
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed — App running on port 5000 and DB restored to AWS RDS.'
        }
        failure {
            echo '❌ Pipeline failed — Check the logs for details.'
        }
    }
}





// pipeline {
//     agent any

//     environment {
//         DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials') // Jenkins credentials ID
//         IMAGE_NAME = 'nkcharan/hspmgmt'
//     }

//     stages {

//         stage('Clone Repository') {
//             steps {
//                 echo 'Cloning repository...'
//                 git branch: 'main', url: 'https://github.com/charannk007/Hospital_Management.git'
//             }
//         }

//         stage('Build Docker Image') {
//             steps {
//                 script {
//                     echo 'Building Docker image...'
//                     sh "docker build -t $IMAGE_NAME:v1 ."
//                 }
//             }
//         }

//         stage('Login to Docker Hub') {
//             steps {
//                 script {
//                     echo 'Logging in to Docker Hub...'
//                     sh """
//                         echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
//                     """
//                 }
//             }
//         }

//         stage('Push to Docker Hub') {
//             steps {
//                 script {
//                     echo 'Pushing image to Docker Hub...'
//                     sh """
//                         docker push $IMAGE_NAME:v1
//                     """
//                 }
//             }
//         }

//     }

//     post {
        
//         success {
//             echo 'Pipeline completed successfully!'
//         }
//         failure {
//             echo 'Pipeline failed.'
//         }
//     }
// }

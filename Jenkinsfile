pipeline {
    agent any
    
    environment {
        // Database Configuration
        DB_PORT = '3306'
        DB_NAME = 'hospital_db'
        SQL_FILE = 'hospital_db_backup.sql'

        // DockerHub Configuration
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        IMAGE_NAME = 'nkcharan/hspmgmt'
        CONTAINER_NAME = 'hospital_app'
        
        // AWS EKS Configuration
        AWS_REGION = 'ap-south-1'
        EKS_CLUSTER_NAME = 'hospital-management'
        NODE_GROUP_NAME = 'worker-nodes'
        NODE_TYPE = 't3.medium'
        DESIRED_NODES = '2'
        MIN_NODES = '1'
        MAX_NODES = '4'
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
        
        stage('Create EKS Cluster') {
            steps {
                withAWS(credentials: 'aws-credentials-id', region: "${AWS_REGION}") {
                    script {
                        echo '🚀 Creating EKS cluster...'
                        sh '''
                            eksctl create cluster \
                              --name ${EKS_CLUSTER_NAME} \
                              --region ${AWS_REGION} \
                              --nodegroup-name ${NODE_GROUP_NAME} \
                              --node-type ${NODE_TYPE} \
                              --nodes ${DESIRED_NODES} \
                              --nodes-min ${MIN_NODES} \
                              --nodes-max ${MAX_NODES} \
                              --with-oidc \
                              --managed
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to EKS Cluster') {
            steps {
                withAWS(credentials: 'aws-credentials-id', region: "${AWS_REGION}") {
                    script {
                        echo '🚀 Deploying application to EKS...'
                        sh '''
                            echo "Configuring kubectl for EKS cluster..."
                            aws eks update-kubeconfig --name ${EKS_CLUSTER_NAME} --region ${AWS_REGION}
                            echo "Deploying application..."
                            kubectl apply -f deployment.yml
                            kubectl apply -f service.yml    
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
            echo '🏥 Hospital Management System deployed to EKS cluster'
        }
        failure {
            echo '❌ Pipeline failed - Check the logs for details'
        }
    }
}












// pipeline {
//     agent any
//     environment {
//         DB_PORT = '3306'
//         DB_NAME = 'hospital_db'
//         SQL_FILE = 'hospital_db_backup.sql'

//         // DockerHub
//         DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
//         IMAGE_NAME = 'nkcharan/hspmgmt'
//         CONTAINER_NAME = 'hospital_app'
//     }

//     stages {

//         stage('Clone Repository') {
//             steps {
//                 echo '🔄 Cloning repository...'
//                 git branch: 'main', url: 'https://github.com/charannk007/Hospital_Management.git'
//             }
//         }
//         stage('Deploy SQL to AWS RDS') {
//             steps {
//                 withCredentials([
//                     usernamePassword(credentialsId: 'mysql-rds-creds', usernameVariable: 'MYSQL_USER', passwordVariable: 'MYSQL_PASS'),
//                     string(credentialsId: 'rds-endpoint', variable: 'DB_HOST')
//                 ]) {
//                     sh '''
//                         echo "🟡 Deploying hospital_db_backup.sql to AWS RDS..."
//                         mysql -h $DB_HOST -P $DB_PORT -u $MYSQL_USER -p"$MYSQL_PASS" $DB_NAME < $SQL_FILE
//                     '''
//                 }
//             }
//         }

//         stage('Build Docker Image') {
//             steps {
//                 echo '🐳 Building Docker image...'
//                 sh "docker build -t $IMAGE_NAME:v1 ."
//             }
//         }

//         stage('Login to Docker Hub') {
//             steps {
//                 echo '🔐 Logging in to Docker Hub...'
//                 sh """
//                     echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
//                 """
//             }
//         }

//         stage('Push to Docker Hub') {
//             steps {
//                 echo '📤 Pushing image to Docker Hub...'
//                 sh "docker push $IMAGE_NAME:v1"
//             }
//         }

//       post {
//         success {
//             echo '✅ Pipeline completed — App running on port 5000 and DB restored to AWS RDS.'
//         }
//         failure {
//             echo '❌ Pipeline failed — Check the logs for details.'
//         }
//     }
// }





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

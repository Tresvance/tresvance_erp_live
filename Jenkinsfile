pipeline {
    agent any

    environment {
        // Define any environment variables here if needed
        COMPOSE_PROJECT_NAME = 'tresvance_erp_live'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the SCM configured in the Jenkins job
                checkout scm
            }
        }

        stage('Build & Test') {
            steps {
                script {
                    // Validate docker-compose configuration
                    echo 'Validating Docker Compose file...'
                    if (isUnix()) {
                        sh 'docker compose config'
                    } else {
                        bat 'docker compose config'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying to live environment...'
                    if (isUnix()) {
                        // For Linux servers
                        sh 'docker compose up -d --build'
                    } else {
                        // For Windows servers
                        bat 'docker compose up -d --build'
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Deployment Failed. Please check the logs.'
        }
    }
}

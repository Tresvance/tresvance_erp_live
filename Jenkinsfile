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

        stage('Deploy to Live Server') {
            steps {
                script {
                    echo 'Deploying to live environment via SSH...'
                    // We use sshagent to securely use your Jenkins SSH credentials
                    // 'live-server-key' is the ID of the credential you will create in Jenkins
                    sshagent(credentials: ['live-server-key']) {
                        // Change YOUR_SERVER_IP to your actual Ubuntu server IP address
                        if (isUnix()) {
                            sh 'ssh -o StrictHostKeyChecking=no root@YOUR_SERVER_IP "cd /odoo/tresvance_erp_live && git pull origin main && docker-compose up -d --build"'
                        } else {
                            bat 'ssh -o StrictHostKeyChecking=no root@YOUR_SERVER_IP "cd /odoo/tresvance_erp_live && git pull origin main && docker-compose up -d --build"'
                        }
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

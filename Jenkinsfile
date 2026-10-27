pipeline {
    agent any

    parameters {
        choice(
            name: 'APP_VERSION',
            choices: ['v1', 'v2', 'v3'],
            description: 'Application version branch to build, test, and publish'
        )
        string(
            name: 'DOCKERHUB_USERNAME',
            defaultValue: 'thiru247',
            description: 'Docker Hub Username / Repository namespace'
        )
    }

    environment {
        IMAGE_NAME = "${params.DOCKERHUB_USERNAME}/notification-system"
        TAG = "${params.APP_VERSION}"
        DOCKER_CREDS = credentials('dockerhub-credentials') // Jenkins Credentials ID
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out branch: ${params.APP_VERSION}"
                checkout scmGit(
                    branches: [[name: "*/${params.APP_VERSION}"]],
                    userRemoteConfigs: scm.userRemoteConfigs
                )
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Setting up Python virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Automated Tests') {
            steps {
                echo 'Running automated tests with pytest...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image ${IMAGE_NAME}:${TAG}..."
                sh """
                    docker build -t ${IMAGE_NAME}:${TAG} .
                """
            }
        }

        stage('Tag Image') {
            steps {
                echo "Tagging Docker image with version: ${TAG}..."
                sh """
                    docker tag ${IMAGE_NAME}:${TAG} ${IMAGE_NAME}:${TAG}
                    docker images | grep ${IMAGE_NAME}
                """
            }
        }

        stage('Authenticate to Docker Hub') {
            steps {
                echo 'Authenticating securely to Docker Hub via Jenkins Credentials...'
                sh """
                    echo \$DOCKER_CREDS_PSW | docker login -u \$DOCKER_CREDS_USR --password-stdin
                """
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                echo "Publishing ${IMAGE_NAME}:${TAG} to Docker Hub..."
                sh """
                    docker push ${IMAGE_NAME}:${TAG}
                """
            }
        }
    }

    post {
        always {
            echo "Pipeline run completed for Notification Management System [${params.APP_VERSION}]."
            sh 'docker logout || true'
        }
        success {
            echo "SUCCESS: ${IMAGE_NAME}:${TAG} built, tested, and pushed successfully!"
        }
        failure {
            echo "FAILURE: Build or test failed for ${IMAGE_NAME}:${TAG}."
        }
    }
}

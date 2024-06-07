pipeline {
    agent any

    environment {
        IMAGE_NAME = 'iris-scheduler'
        IMAGE_TAG = '0.1.0'
        DOCKERFILE = 'Dockerfile.scheduler'
        CONTEXT_DIR = '.'
        FULL_IMAGE_NAME = "${IMAGE_NAME}:${IMAGE_TAG}"
        NETWORK_NAME = 'iris-network'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Check if the image exists
                    def img = sh(script: "docker images -q ${FULL_IMAGE_NAME}", returnStdout: true).trim()
                    if (img) {
                        echo "Image exists, deleting image"
                        // Delete the existing image
                        sh "docker rmi ${FULL_IMAGE_NAME}"
                    }
                    // Build the image
                    echo "Building new image"
                    sh "docker build -t ${FULL_IMAGE_NAME} -f ${DOCKERFILE} ${CONTEXT_DIR}"
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                // Run the container with the image and mount the models and data directories
                sh "docker run --rm --network ${NETWORK_NAME} -v \$(pwd)/models:/app/models -v \$(pwd)/data:/app/data ${FULL_IMAGE_NAME}"
            }
        }

        stage('Cleanup Docker Image') {
            steps {
                script {
                    // Use 'docker rmi' to remove the image
                    sh "docker rmi ${FULL_IMAGE_NAME}"
                }
            }
        }
    }
}

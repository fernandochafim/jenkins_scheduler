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
        stage('Check Image Exists') {
            steps {
                script {
                    def img = sh(script: "docker images -q ${FULL_IMAGE_NAME}", returnStdout: true).trim()
                    if (img == "") {
                        echo "Image does not exist"
                        sh "docker build -t ${FULL_IMAGE_NAME} -f ${DOCKERFILE} ${CONTEXT_DIR}"
                    } else {
                        echo "Image exists, skipping build"
                    }
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                sh "docker run --rm --network ${NETWORK_NAME} -v \$(pwd)/models:/app/models -v \$(pwd)/data:/app/data ${FULL_IMAGE_NAME}"
            }
        }
    }
}

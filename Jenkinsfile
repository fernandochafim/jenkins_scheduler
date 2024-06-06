pipeline {
    agent any

    environment {
        IMAGE_NAME = 'iris-scheduler'
    }

    stages {
        stage('Check Image Exists') {
            steps {
                script {
                    def img = sh(script: "docker images -q ${IMAGE_NAME}", returnStdout: true).trim()
                    if (img == "") {
                        echo "Image does not exist"
                        sh "docker build -t ${IMAGE_NAME} ."
                    } else {
                        echo "Image exists, skipping build"
                    }
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                sh "docker run --rm ${IMAGE_NAME}"
            }
        }
    }
}

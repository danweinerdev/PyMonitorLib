pipeline {
    agent {
        dockerfile {
            customWorkspace "workspace/${env.JOB_NAME}/${env.BUILD_NUMBER}"
            dir 'deploy'
            filename 'Builder.Dockerfile'
            label 'linux && docker'
            additionalBuildArgs '--network host'
            args '--network host'
        }
    }

    triggers {
        pollSCM('H/5 * * * * ')
    }

    stages {
        stage('Validate parameters') {
            steps {
                script {
                    sh "/bin/true"
                }
            }
        }
        stage('Run Tests') {
            steps {
                sh "/bin/true"
            }
        }
    }
}

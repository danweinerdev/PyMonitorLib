pipeline {
    agent {
        dockerfile {
            customWorkspace "workspace/${env.JOB_NAME}/${env.BUILD_NUMBER}"
            filename 'deploy/Builder.Dockerfile'
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
        stage('Build Package') {
            steps {
                script {
                    sh "python3 setup.py sdist bdist_wheel"
                }
            }
        }
        stage('Publish Package') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'PyPi_PyMonitorLib_API_Token',
                        usernameVariable: 'PYPI_USERNAME',
                        passwordVariable: 'PYPI_PASSWORD')])
                {
                    sh '''
                        set +x
                        python3 -m twine upload --non-interactive \
                            --username $PYPI_USERNAME \
                            --password $PYPI_PASSWORD \
                            dist/*
                    '''
                }
            }
        }
    }
}

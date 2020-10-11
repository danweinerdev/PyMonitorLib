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

    stages {
        stage('Validate parameters') {
            steps {
                script {
                    sh "/bin/true"
                }
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
                        credentialsId: 'PyPI_API_Token',
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

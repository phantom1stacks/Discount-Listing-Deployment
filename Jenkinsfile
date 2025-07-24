pipeline {
    agent any
    environment {
        VENV = "${WORKSPACE}/venv"
    }
    stages {
        stage('Clone') {
            steps { checkout scm }
        }
        stage('Build') {
            steps {
                sh 'python -m venv $VENV && . $VENV/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh '. $VENV/bin/activate && pytest -q'
            }
            post { always { junit 'pytest.xml' } }
        }
        stage('SonarQube') {
            when { branch 'main' }
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '. $VENV/bin/activate && sonar-scanner'
                }
            }
        }
        stage('Deploy') {
            steps {
                sh '. $VENV/bin/activate && FLASK_ENV=production flask run --host=0.0.0.0 &'
            }
        }
    }
    post {
        success { echo '✅ Deployed successfully.' }
        failure { echo '❌ Build failed.' }
    }
}

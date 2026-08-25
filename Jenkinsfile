pipeline {
    agent any

    parameters {
        choice(
            name: 'DEPLOY_MODE',
            choices: ['delta', 'all'],
            description: 'delta = Only deploy new/modified JSON jobs in this commit; all = Deploy all jobs in repository'
        )
        choice(
            name: 'TARGET_ENV',
            choices: ['DEV', 'UAT', 'PROD'],
            description: 'Target Control-M Environment'
        )
        booleanParam(
            name: 'DRY_RUN',
            defaultValue: false,
            description: 'If checked, validates (builds) without deploying to Control-M'
        )
    }

    environment {
        CTM_ENV = "${params.TARGET_ENV}"
        PYTHONUNBUFFERED = "1"
    }

    stages {
        stage('Checkout & Setup') {
            steps {
                echo "=========================================================="
                echo " Starting Control-M Jobs-as-Code CI/CD Pipeline"
                echo " Environment: ${params.TARGET_ENV} | Mode: ${params.DEPLOY_MODE}"
                echo "=========================================================="
            }
        }

        stage('Validate & Build (Jobs-as-Code)') {
            steps {
                script {
                    echo "--> Dynamically discovering and validating Control-M Job definitions..."
                    if (isUnix()) {
                        sh "python3 engine/ctm_pipeline_engine.py --mode ${params.DEPLOY_MODE} --action build"
                    } else {
                        bat "python engine/ctm_pipeline_engine.py --mode %DEPLOY_MODE% --action build"
                    }
                }
            }
        }

        stage('Deploy to Control-M') {
            when {
                expression { return params.DRY_RUN == false }
            }
            steps {
                script {
                    echo "--> Deploying verified definitions to Control-M ${params.TARGET_ENV}..."
                    if (isUnix()) {
                        sh "python3 engine/ctm_pipeline_engine.py --mode ${params.DEPLOY_MODE} --action deploy"
                    } else {
                        bat "python engine/ctm_pipeline_engine.py --mode %DEPLOY_MODE% --action deploy"
                    }
                }
            }
        }
    }

    post {
        always {
            echo "--> Archiving Deployment Reports & Logs..."
            archiveArtifacts artifacts: 'ctm-deploy-reports/**', allowEmptyArchive: true
        }
        success {
            echo "=========================================================="
            echo " SUCCESS: Control-M Jobs-as-Code pipeline completed cleanly!"
            echo "=========================================================="
        }
        failure {
            echo "=========================================================="
            echo " FAILED: One or more jobs failed validation or deployment."
            echo "=========================================================="
        }
    }
}

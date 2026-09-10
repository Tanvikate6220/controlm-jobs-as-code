pipeline {
    agent any

    parameters {
        choice(
            name: 'DEPLOY_MODE',
            choices: ['delta', 'all'],
            description: 'delta = Only deploy new/modified JSON jobs in this commit; all = Full repo sync'
        )
        choice(
            name: 'TARGET_ENV',
            choices: ['DEV', 'UAT', 'PROD'],
            description: 'Target Control-M Environment'
        )
        booleanParam(
            name: 'AUTO_ORDER',
            defaultValue: true,
            description: 'Automatically order/trigger the job in Control-M active monitoring after deployment'
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
        PATH = "C:\\Users\\Tanvi.kate\\AppData\\Roaming\\npm;C:\\Program Files\\nodejs;C:\\Program Files\\Git\\cmd;C:\\Users\\Tanvi.kate\\AppData\\Local\\Programs\\Python\\Python312;${env.PATH}"
    }

    stages {
        stage('Checkout & Setup') {
            steps {
                echo "Starting Control-M Jobs-as-Code Pipeline for Environment: ${params.TARGET_ENV} | Mode: ${params.DEPLOY_MODE} | Auto-Order: ${params.AUTO_ORDER}"
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

        stage('Deploy & Auto-Order in Control-M') {
            when {
                expression { return params.DRY_RUN == false }
            }
            steps {
                script {
                    def orderFlag = params.AUTO_ORDER ? "--auto-order" : "--no-auto-order"
                    echo "--> Deploying and auto-scheduling definitions to Control-M ${params.TARGET_ENV}..."
                    if (isUnix()) {
                        sh "python3 engine/ctm_pipeline_engine.py --mode ${params.DEPLOY_MODE} --action deploy ${orderFlag}"
                    } else {
                        bat "python engine/ctm_pipeline_engine.py --mode %DEPLOY_MODE% --action deploy ${orderFlag}"
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
            echo "SUCCESS: Control-M Jobs-as-Code pipeline completed cleanly with automatic deployment and scheduling!"
        }
        failure {
            echo "FAILED: One or more jobs failed validation, deployment, or ordering."
        }
    }
}

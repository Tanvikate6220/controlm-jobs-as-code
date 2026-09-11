pipeline {
    agent any

    parameters {
        choice(
            name: 'ACTION',
            choices: ['reconcile_two_way', 'build_and_deploy', 'reverse_sync_gui_to_git', 'build_only'],
            description: 'reconcile_two_way = Full automated bidirectional sync with conflict & loop protection; build_and_deploy = Forward Git->Control-M; reverse_sync_gui_to_git = Control-M GUI->GitHub'
        )
        choice(
            name: 'DEPLOY_MODE',
            choices: ['delta', 'all'],
            description: 'delta = Only process git changed/deleted jobs in this commit; all = Full scan'
        )
        choice(
            name: 'TARGET_ENV',
            choices: ['DEV', 'UAT', 'PROD'],
            description: 'Target Control-M Environment'
        )
    }

    environment {
        CTM_ENV = "${params.TARGET_ENV}"
        PYTHONUNBUFFERED = "1"
        PATH = "C:\\Users\\Tanvi.kate\\AppData\\Roaming\\npm;C:\\Program Files\\nodejs;C:\\Program Files\\Git\\cmd;C:\\Users\\Tanvi.kate\\AppData\\Local\\Programs\\Python\\Python312;${env.PATH}"
    }

    stages {
        stage('Pipeline Initialization') {
            steps {
                echo "================================================================="
                echo "Control-M Jobs-as-Code Two-Way Reconciliation Engine"
                echo "Action: ${params.ACTION} | Environment: ${params.TARGET_ENV} | Mode: ${params.DEPLOY_MODE}"
                echo "================================================================="
            }
        }

        stage('Two-Way Bidirectional Reconciliation') {
            when {
                expression { return params.ACTION == 'reconcile_two_way' }
            }
            steps {
                script {
                    echo "--> Running SHA-256 Hash-Based Bidirectional Reconciliation..."
                    if (isUnix()) {
                        sh "python3 engine/ctm_reconciliation_engine.py"
                    } else {
                        bat "python engine/ctm_reconciliation_engine.py"
                    }
                }
            }
        }

        stage('Reverse Sync (Control-M GUI -> GitHub)') {
            when {
                expression { return params.ACTION == 'reverse_sync_gui_to_git' }
            }
            steps {
                script {
                    echo "--> Pulling latest definitions from Control-M GUI and synchronizing GitHub..."
                    if (isUnix()) {
                        sh "python3 engine/ctm_pipeline_engine.py --action reverse-sync"
                    } else {
                        bat "python engine/ctm_pipeline_engine.py --action reverse-sync"
                    }
                }
            }
        }

        stage('Validate & Build (Jobs-as-Code)') {
            when {
                expression { return params.ACTION in ['build_and_deploy', 'build_only'] }
            }
            steps {
                script {
                    echo "--> Dynamically validating Control-M Job JSON definitions..."
                    if (isUnix()) {
                        sh "python3 engine/ctm_pipeline_engine.py --mode ${params.DEPLOY_MODE} --action build"
                    } else {
                        bat "python engine/ctm_pipeline_engine.py --mode %DEPLOY_MODE% --action build"
                    }
                }
            }
        }

        stage('Configure in Control-M (Planning Domain & Deletions)') {
            when {
                expression { return params.ACTION == 'build_and_deploy' }
            }
            steps {
                script {
                    echo "--> Configuring definitions and applying deletions in Control-M Planning (${params.TARGET_ENV})..."
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
            echo "SUCCESS: Control-M Jobs-as-Code automation completed cleanly!"
        }
        failure {
            echo "FAILED: Pipeline encountered an error during execution."
        }
    }
}



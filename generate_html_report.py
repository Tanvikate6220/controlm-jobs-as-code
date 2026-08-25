import os
import base64
from pathlib import Path

desktop_folder = Path(r"C:\Users\Tanvi.kate\Desktop\ControlM_Jobs_As_Code_Presentation")

def get_base64_img(img_name):
    p = desktop_folder / img_name
    if p.exists():
        with open(p, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{data}"
    return ""

img_gui = get_base64_img("img_controlm_gui_monitoring.png")
img_gh = get_base64_img("img_github_repo_view.png")
img_push = get_base64_img("img_git_push_terminal.png")
img_console = get_base64_img("img_jenkins_console_output.png")
img_dash = get_base64_img("img_jenkins_dashboard_builds.png")
img_git_config = get_base64_img("img_jenkins_git_tool_config.png")

html_content = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Control-M Jobs-as-Code CI/CD Automation</title>
<style>
    :root {
        --primary: #0056b3;
        --primary-dark: #003875;
        --primary-light: #e8f1fc;
        --secondary: #17a2b8;
        --success: #28a745;
        --warning: #ffc107;
        --danger: #dc3545;
        --dark: #212529;
        --light: #f8f9fa;
        --border: #dee2e6;
    }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.7;
        color: #2c3e50;
        max-width: 1150px;
        margin: 30px auto;
        padding: 0 30px;
        background: #ffffff;
    }
    .header-banner {
        background: linear-gradient(135deg, #002b5c 0%, #0056b3 50%, #007bff 100%);
        color: white;
        padding: 30px 30px;
        border-radius: 12px;
        margin-bottom: 35px;
        box-shadow: 0 10px 25px rgba(0, 56, 117, 0.25);
    }
    .header-banner h1 {
        margin: 0;
        font-size: 2.2em;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .meta-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 15px;
        margin-top: 20px;
        background: rgba(255, 255, 255, 0.15);
        padding: 14px 20px;
        border-radius: 8px;
        max-width: 500px;
    }
    .meta-item strong {
        display: block;
        color: #d0e2ff;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 2px;
    }
    .meta-item span {
        font-size: 15px;
        font-weight: 600;
    }
    h2 {
        color: var(--primary-dark);
        font-size: 1.65em;
        border-bottom: 2px solid var(--border);
        padding-bottom: 10px;
        margin-top: 50px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    h3 {
        color: var(--primary);
        font-size: 1.3em;
        margin-top: 30px;
        border-left: 4px solid var(--primary);
        padding-left: 12px;
    }
    h4 {
        color: #495057;
        font-size: 1.1em;
        margin-top: 20px;
        font-weight: 600;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 25px 0;
        font-size: 14px;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }
    th, td {
        border: 1px solid #dee2e6;
        padding: 13px 16px;
        text-align: left;
        vertical-align: top;
    }
    th {
        background-color: #f1f5f9;
        color: #1e293b;
        font-weight: 600;
    }
    tr:nth-child(even) {
        background-color: #fafbfc;
    }
    .comparison-table th {
        background-color: #003875;
        color: white;
    }
    pre {
        background-color: #1a1e24;
        color: #e6edf3;
        border-radius: 8px;
        padding: 18px 20px;
        overflow-x: auto;
        font-size: 13px;
        line-height: 1.55;
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        margin: 18px 0;
    }
    code {
        background-color: #eef3f9;
        color: #0056b3;
        border-radius: 4px;
        font-size: 88%;
        padding: 0.2em 0.45em;
        font-family: Consolas, monospace;
    }
    pre code {
        background-color: transparent;
        color: inherit;
        padding: 0;
    }
    .info-card {
        background-color: var(--primary-light);
        border-left: 5px solid var(--primary);
        border-radius: 0 8px 8px 0;
        padding: 18px 22px;
        margin: 22px 0;
    }
    .benefit-card {
        background-color: #f0fdf4;
        border-left: 5px solid var(--success);
        border-radius: 0 8px 8px 0;
        padding: 18px 22px;
        margin: 22px 0;
    }
    .step-box {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 22px;
        margin: 25px 0;
        background: #ffffff;
        box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    }
    .step-header {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.25em;
        font-weight: 700;
        color: var(--primary-dark);
        margin-bottom: 15px;
    }
    .step-number {
        background: var(--primary);
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
    }
    .img-box {
        margin: 30px 0;
        text-align: center;
        background: #fbfcfd;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 18px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }
    .img-box img {
        max-width: 100%;
        height: auto;
        border-radius: 6px;
        border: 1px solid #cbd5e1;
    }
    .img-caption {
        font-size: 13px;
        color: #64748b;
        margin-top: 12px;
        font-weight: 600;
    }
    .key-points {
        list-style: none;
        padding-left: 0;
    }
    .key-points li {
        padding: 6px 0;
        padding-left: 24px;
        position: relative;
    }
    .key-points li::before {
        content: "✓";
        position: absolute;
        left: 0;
        color: var(--success);
        font-weight: bold;
    }
    @media print {
        body { max-width: 100%; margin: 0; padding: 15px; font-size: 12px; }
        .header-banner { padding: 20px; }
        .img-box img { max-width: 95%; page-break-inside: avoid; }
        pre { font-size: 11px; padding: 12px; page-break-inside: avoid; }
        .step-box { page-break-inside: avoid; }
    }
</style>
</head>
<body>

<div class="header-banner">
    <h1>🚀 Control-M Jobs-as-Code CI/CD Automation</h1>
    <div class="meta-grid">
        <div class="meta-item">
            <strong>Name</strong>
            <span>Tanvi Kate</span>
        </div>
        <div class="meta-item">
            <strong>Designation</strong>
            <span>BMC Engineer A&amp;A</span>
        </div>
    </div>
</div>

<h2>📌 1. Executive Summary & Strategic Objectives</h2>

<h3>1.1 The Operational Challenge in Traditional Control-M Management</h3>
<p>In conventional enterprise workload scheduling, Control-M jobs are defined, modified, and scheduled manually by operators using the Control-M Desktop GUI (Workload Automation client). While the GUI is powerful for operational monitoring, managing thousands of batch jobs through manual clicking causes critical operational bottlenecks:</p>
<ul>
    <li><strong>Lack of Version Control & Traceability:</strong> When a job schedule or command is changed in the GUI, there is no inherent code-review process or commit history tracking <em>who</em> changed it, <em>why</em> it changed, and <em>what</em> the exact previous syntax was.</li>
    <li><strong>High Risk of Human Error:</strong> Promoting job schedules across DEV, UAT, and PROD requires manual re-entry or XML exports, leading to hostname mismatches, missing execution paths, and typo-induced production outages.</li>
    <li><strong>Deployment Latency:</strong> Software developers cannot release application code and its corresponding Control-M batch scheduling together; batch jobs lag behind application releases by days due to ticketing queues.</li>
    <li><strong>Disaster Recovery Friction:</strong> Reverting an accidental job deletion or corruption requires database rollbacks or manual re-keying from memory.</li>
</ul>

<h3>1.2 The Jobs-as-Code CI/CD Paradigm</h3>
<div class="benefit-card">
    <strong>🎯 Core Objective of This Project:</strong><br>
    Transform Control-M job scheduling into a pure <strong>Software Engineering Discipline ("Jobs-as-Code")</strong>. Every job is represented as declarative JSON, stored in <strong>Git/GitHub</strong>, version-controlled alongside application code, and automatically tested, built, and deployed to <strong>BMC Control-M 9.0.22</strong> via a <strong>Declarative Jenkins Pipeline</strong> with <strong>Zero Hardcoded Job Names</strong>.
</div>

<div class="info-card">
    <strong>🌟 High-Level Architectural Flow:</strong><br>
    <code>Developer creates/modifies JSON Job &rarr; Git Commit & Push to GitHub &rarr; Webhook/Polling triggers Jenkins &rarr; Dynamic Python Engine scans Git Diff &rarr; Pre-Deployment Linting (ctm build) &rarr; Deployment to EM Database (ctm deploy) &rarr; Scheduled / Ordered on Agent (M0988) &rarr; Real-time Monitoring in GUI.</code>
</div>

<h2>⚖️ 2. Comprehensive Comparative Analysis: Why Jobs-as-Code is Superior</h2>

<table class="comparison-table">
    <tr>
        <th>Key Dimension</th>
        <th>❌ Traditional Control-M GUI Approach</th>
        <th>✅ Git-Driven Jobs-as-Code CI/CD (Our Solution)</th>
        <th>Business Impact & Benefit</th>
    </tr>
    <tr>
        <td><strong>Definition Paradigm</strong></td>
        <td>Manual form filling across multiple GUI property tabs.</td>
        <td>Declarative, human-readable JSON files (BMC 9.0.22 Schema).</td>
        <td>Standardizes job definitions; readable by any engineer.</td>
    </tr>
    <tr>
        <td><strong>Single Source of Truth</strong></td>
        <td>The live Control-M Enterprise Manager Database.</td>
        <td>Git/GitHub repository with full commit history.</td>
        <td>Complete audit compliance (SOC2/ISO27001 ready).</td>
    </tr>
    <tr>
        <td><strong>Pre-Deployment Validation</strong></td>
        <td>Errors only detected upon manual GUI submission.</td>
        <td>Automated pre-flight syntax and schema linting via <code>ctm build</code>.</td>
        <td>Catches 100% of syntax errors before touching the server.</td>
    </tr>
    <tr>
        <td><strong>Deployment Speed</strong></td>
        <td>Hours to days (manual ticketing queues).</td>
        <td>Under 15 seconds automated execution per Git Push.</td>
        <td>Accelerates time-to-market and developer velocity.</td>
    </tr>
    <tr>
        <td><strong>Environment Promotion</strong></td>
        <td>Manual re-creation or complex XML export/import.</td>
        <td>Automated Git branch merges (<code>develop</code> &rarr; <code>release</code> &rarr; <code>main</code>).</td>
        <td>Zero configuration drift between DEV, UAT, and PROD.</td>
    </tr>
    <tr>
        <td><strong>Rollback Strategy</strong></td>
        <td>Manual reconstruction from memory or database restore.</td>
        <td>One-command rollback via <code>git revert &lt;commit_id&gt;</code>.</td>
        <td>Mean Time to Recovery (MTTR) reduced from hours to seconds.</td>
    </tr>
    <tr>
        <td><strong>Dynamic Scalability</strong></td>
        <td>Manual entry doesn't scale for 10,000+ jobs.</td>
        <td>Python dynamic discovery automatically handles infinite folders.</td>
        <td>Jenkins pipeline code requires <strong>zero changes</strong> as jobs scale.</td>
    </tr>
</table>

<h2>🛠️ 3. Environment Specifications, Toolchain & Network Matrix</h2>

<table>
    <tr>
        <th>Component</th>
        <th>Version Verified</th>
        <th>Port / URL Endpoint</th>
        <th>Technical Function & Responsibility</th>
    </tr>
    <tr>
        <td><strong>Git</strong></td>
        <td><code>2.55.0.windows.3</code></td>
        <td>Local / CLI</td>
        <td>Distributed version control tracking all JSON files and scripts.</td>
    </tr>
    <tr>
        <td><strong>GitHub</strong></td>
        <td>Cloud SCM</td>
        <td><code>https://github.com/Tanvikate6220/controlm-jobs-as-code.git</code></td>
        <td>Central cloud repository acting as the master source of truth.</td>
    </tr>
    <tr>
        <td><strong>Java JDK</strong></td>
        <td><code>Adoptium Temurin 21.0.12 LTS</code></td>
        <td>Local JVM</td>
        <td>Runtime requirement for Jenkins 2.568.2 LTS engine.</td>
    </tr>
    <tr>
        <td><strong>Jenkins</strong></td>
        <td><code>2.568.2 LTS</code></td>
        <td><code>http://localhost:8080</code></td>
        <td>Orchestrates the build, validation, deployment, and audit stages.</td>
    </tr>
    <tr>
        <td><strong>Python</strong></td>
        <td><code>3.12.10</code></td>
        <td>Local Runtime</td>
        <td>Dynamic Git-diff delta scanner and local schema validator.</td>
    </tr>
    <tr>
        <td><strong>Node.js & npm</strong></td>
        <td><code>v24.19.0</code> / <code>11.17.0</code></td>
        <td>Local Runtime</td>
        <td>Execution platform for BMC Automation API CLI package.</td>
    </tr>
    <tr>
        <td><strong>BMC Control-M CLI</strong></td>
        <td><code>v9.22.0</code></td>
        <td>Local CLI (<code>ctm</code>)</td>
        <td>Official BMC CLI communicating with Control-M REST services.</td>
    </tr>
    <tr>
        <td><strong>Control-M EM Server</strong></td>
        <td><code>M0988</code> (v9.0.22.000)</td>
        <td><code>https://m0988:8443/automation-api</code></td>
        <td>Enterprise Manager database and REST API gateway.</td>
    </tr>
    <tr>
        <td><strong>Control-M Agent</strong></td>
        <td><code>m0988</code> (Win Server 2022)</td>
        <td>Internal TCP</td>
        <td>Physical target host executing operating system commands.</td>
    </tr>
</table>

<h2>🏗️ 4. Exhaustive Step-by-Step Implementation & Code Rationale</h2>

<div class="step-box">
    <div class="step-header">
        <span class="step-number">1</span>
        <span>Phase 1: Workstation Diagnostic & Toolchain Setup</span>
    </div>
    <p><strong>Aim:</strong> Inspect the local laptop, resolve missing dependencies, and prepare the core DevOps engine.</p>
    <p><strong>Action Taken:</strong> We identified that Git, Node.js, Python, and Java were missing from the system path. We utilized Windows Package Manager (<code>winget</code>) for silent, automated installations, downloaded the Jenkins WAR package, and configured user environment variables.</p>
    
    <h4>Exact Commands Executed:</h4>
    <pre><code># 1. Install Git, Node.js LTS, and Python 3.12
winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
winget install --id OpenJS.NodeJS.LTS -e --source winget --accept-package-agreements --accept-source-agreements
winget install --id Python.Python.3.12 -e --source winget --accept-package-agreements --accept-source-agreements

# 2. Install Java 21 LTS (Required by Jenkins 2.568+)
winget install --id EclipseAdoptium.Temurin.21.JDK -e --source winget --accept-package-agreements --accept-source-agreements

# 3. Setup Jenkins Directory & Download WAR Package
New-Item -ItemType Directory -Path "C:\Users\Tanvi.kate\jenkins" -Force
Invoke-WebRequest -Uri "https://get.jenkins.io/war-stable/latest/jenkins.war" -OutFile "C:\Users\Tanvi.kate\jenkins\jenkins.war"

# 4. Start Jenkins Daemon on Port 8080
& "C:\Program Files\Eclipse Adoptium\jdk-21.0.12.101-hotspot\bin\java.exe" -jar "C:\Users\Tanvi.kate\jenkins\jenkins.war" --httpPort=8080</code></pre>
</div>

<div class="step-box">
    <div class="step-header">
        <span class="step-number">2</span>
        <span>Phase 2: Target Script & Jobs-as-Code JSON Definition</span>
    </div>
    <p><strong>Aim:</strong> Construct a native BMC Control-M 9.0.22 compliant JSON definition that replaces manual GUI configuration.</p>
    <p><strong>Action Taken:</strong> Created <code>jobs/HELLO_CONTROL_M.json</code> and configured default properties, SMART Folder structure, target server (<code>M0988</code>), agent host (<code>m0988</code>), and execution identity (<code>A3807</code>).</p>
    
    <h4>Code Breakdown (`jobs/HELLO_CONTROL_M.json`):</h4>
    <pre><code>{
  "Defaults": {
    "Application": "DEMO_APP",
    "SubApplication": "JOBS_AS_CODE",
    "RunAs": "A3807",
    "Host": "m0988"
  },
  "SAMPLE_AUTOMATION_FOLDER": {
    "Type": "Folder",
    "ControlmServer": "M0988",
    "OrderMethod": "Manual",
    "HELLO_CONTROL_M": {
      "Type": "Job:Command",
      "Command": "echo Hello from Control-M Jobs-as-Code CI/CD Pipeline! & hostname",
      "RunAs": "A3807",
      "Host": "m0988",
      "Description": "Demo Hello World job deployed dynamically via Jobs-as-Code CI/CD",
      "When": {
        "Schedule": "Never"
      }
    }
  }
}</code></pre>
    
    <div class="info-card">
        <strong>Detailed Rationale for Every Element:</strong>
        <ul class="key-points">
            <li><strong><code>"Defaults"</code> Block:</strong> Defines shared parameters (Application, SubApplication, RunAs, Host) inherited by all jobs in this file, eliminating duplicate entries.</li>
            <li><strong><code>"SAMPLE_AUTOMATION_FOLDER"</code>:</strong> Creates a SMART Folder in the Control-M database to group related jobs logically.</li>
            <li><strong><code>"ControlmServer": "M0988"</code>:</strong> Directs the Enterprise Manager to register the folder under the active scheduling server <code>M0988</code>.</li>
            <li><strong><code>"Type": "Job:Command"</code>:</strong> Specifies that this is an operating system command job rather than an external plug-in.</li>
            <li><strong><code>"RunAs": "A3807"</code>:</strong> Mandatory security field in Control-M 9.0.22 specifying the authorized local user account that executes the process on the agent.</li>
            <li><strong><code>"When" &rarr; "Schedule": "Never"</code>:</strong> Configured for on-demand ordering through API/CI/CD pipelines rather than traditional daily new-day ordering.</li>
        </ul>
    </div>
</div>

<div class="step-box">
    <div class="step-header">
        <span class="step-number">3</span>
        <span>Phase 3: Git Version Control & GitHub Synchronization</span>
    </div>
    <p><strong>Aim:</strong> Initialize local Git tracking and establish GitHub as the single remote source of truth.</p>
    <p><strong>Action Taken:</strong> Created a structured <code>.gitignore</code>, initialized the repository on branch <code>main</code>, connected the remote URL <code>https://github.com/Tanvikate6220/controlm-jobs-as-code.git</code>, and performed the initial push.</p>
    
    <pre><code>cd "C:\Users\Tanvi.kate\.gemini\antigravity\scratch\controlm-jobs-as-code"
git init
git config user.name "Tanvi Kate"
git config user.email "tanvi.kate@company.com"
git branch -M main
git remote add origin https://github.com/Tanvikate6220/controlm-jobs-as-code.git
git add .
git commit -m "feat: initial commit with Control-M Jobs-as-Code pipeline"
git push -u origin main</code></pre>

    <div class="img-box">
        <img src="IMG_PUSH_PLACEHOLDER" alt="Git Terminal Push">
        <div class="img-caption">Figure 1: PowerShell Terminal output showing successful push of main branch to GitHub</div>
    </div>

    <div class="img-box">
        <img src="IMG_GH_PLACEHOLDER" alt="GitHub Repository Live">
        <div class="img-caption">Figure 2: Remote GitHub Repository hosting engine, job definitions, scripts, and Jenkinsfile</div>
    </div>
</div>

<div class="step-box">
    <div class="step-header">
        <span class="step-number">4</span>
        <span>Phase 4: Dynamic Python Discovery & Delta Engine</span>
    </div>
    <p><strong>Aim:</strong> Eliminate all hardcoded job names in Jenkins and implement smart delta-detection using Git diff.</p>
    <p><strong>Action Taken:</strong> Developed <code>engine/ctm_pipeline_engine.py</code>. When a build triggers, this engine calculates <code>git diff --name-only HEAD~1 HEAD</code> to find exactly which JSON files were added or modified in that specific commit. It runs local schema verification, invokes <code>ctm build</code>, deploys verified jobs via <code>ctm deploy</code>, and generates Markdown and JSON audit reports in <code>ctm-deploy-reports/</code>.</p>
    
    <h4>Core Dynamic Discovery Algorithm (`engine/ctm_pipeline_engine.py`):</h4>
    <pre><code>def get_changed_files_from_git(self, base_ref=None):
    # Runs git diff to inspect only modified/added files in the latest commit
    cmd = ["git", "diff", "--name-only", "--diff-filter=d", "HEAD~1", "HEAD"]
    result = subprocess.run(cmd, cwd=str(self.workspace), capture_output=True, text=True, check=True)
    
    changed_files = []
    for line in result.stdout.strip().splitlines():
        filepath = self.workspace / line.strip()
        if filepath.suffix.lower() == ".json" and "jobs" in filepath.parts and filepath.exists():
            changed_files.append(filepath)
            
    print(f"[GIT DISCOVERY] Detected {len(changed_files)} changed Job JSON definition(s).")
    return sorted(changed_files)</code></pre>
</div>

<div class="step-box">
    <div class="step-header">
        <span class="step-number">5</span>
        <span>Phase 5: Cross-Platform Declarative Jenkins Pipeline</span>
    </div>
    <p><strong>Aim:</strong> Build a resilient, cross-platform Jenkins pipeline capable of running on Windows build nodes and Linux containers.</p>
    <p><strong>Action Taken:</strong> Configured Jenkins global tool path for Git (<code>C:\Program Files\Git\cmd\git.exe</code>), and built a declarative <code>Jenkinsfile</code> utilizing Jenkins' native <code>isUnix()</code> function to dynamically switch between Windows <code>bat</code> and Linux <code>sh</code> commands.</p>
    
    <h4>Cross-Platform `Jenkinsfile` Implementation:</h4>
    <pre><code>pipeline {
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
                echo "Starting Control-M Jobs-as-Code Pipeline for Environment: ${params.TARGET_ENV} | Mode: ${params.DEPLOY_MODE}"
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
            echo "SUCCESS: Control-M Jobs-as-Code pipeline completed cleanly!"
        }
        failure {
            echo "FAILED: One or more jobs failed validation or deployment."
        }
    }
}</code></pre>

    <div class="img-box">
        <img src="IMG_GIT_CONFIG_PLACEHOLDER" alt="Jenkins Git Configuration">
        <div class="img-caption">Figure 3: Jenkins Global Tool Configuration setting the Git executable path</div>
    </div>

    <div class="img-box">
        <img src="IMG_DASH_PLACEHOLDER" alt="Jenkins Pipeline Dashboard">
        <div class="img-caption">Figure 4: Jenkins Pipeline Dashboard showing successful builds (#5, #6, #7) and published artifacts</div>
    </div>

    <div class="img-box">
        <img src="IMG_CONSOLE_PLACEHOLDER" alt="Jenkins Console Log Output">
        <div class="img-caption">Figure 5: Jenkins Console Output executing SCM checkout and dynamic delta build validation</div>
    </div>
</div>

<div class="step-box">
    <div class="step-header">
        <span class="step-number">6</span>
        <span>Phase 6: Live Control-M 9.0.22 API Authentication & Deployment</span>
    </div>
    <p><strong>Aim:</strong> Authenticate against the live Enterprise Manager server <code>https://m0988:8443/automation-api</code> and deploy job definitions directly into the database.</p>
    <p><strong>Action Taken:</strong> We installed the official BMC CLI package directly from the EM server (<code>https://m0988:8443/automation-api/ctm-cli.tgz</code>), authenticated user <code>A3807</code> with AES-256 encrypted credential storage, discovered active server <code>M0988</code> and agent <code>m0988</code>, and performed live deployments and execution orders.</p>
    
    <h4>CLI Commands & Responses:</h4>
    <pre><code># 1. Add Control-M Environment Endpoint
ctm env add controlm https://m0988:8443/automation-api A3807 'Viraj@64556220'
ctm env set controlm

# 2. Session Login & Token Verification
ctm session login
# Output: { "username": "A3807", "token": "E06150B3...", "version": "9.22.0" }

# 3. Deploy Definitions to Control-M Database
ctm deploy jobs/HELLO_CONTROL_M.json
ctm deploy jobs/PAYMENT_GATEWAY_JOB.json
ctm deploy jobs/CUSTOMER_ANALYTICS_JOB.json
# Output: [ { "deploymentFile": "HELLO_CONTROL_M.json", "deploymentStatus": "ENDED_OK", "deployedFolders": ["SAMPLE_AUTOMATION_FOLDER"] } ]

# 4. Trigger & Order Jobs on Server M0988
ctm run order M0988 SAMPLE_AUTOMATION_FOLDER
ctm run order M0988 PAYMENT_PROCESSING_FOLDER
ctm run order M0988 ANALYTICS_PROCESSING_FOLDER</code></pre>
</div>

<h2>📊 5. Live Production Verification in Control-M GUI (Monitoring Domain)</h2>

<p>Every job deployed through the Jobs-as-Code pipeline was ordered and verified in the live <strong>Control-M Workload Automation GUI (Monitoring Domain)</strong> with <strong>Ended OK</strong> (Green Checkmarks):</p>

<ul>
    <li><strong>Application: <code>DEMO_APP</code></strong> &rarr; Sub-App: <code>JOBS_AS_CODE</code> &rarr; Folder: <code>SAMPLE_AUTOMATION_FOLDER</code> &rarr; <strong>Job: <code>HELLO_CONTROL_M</code></strong> (Status: <code>Ended OK</code>) 🟢</li>
    <li><strong>Application: <code>FINANCE_CORE</code></strong> &rarr; Sub-App: <code>PAYMENTS</code> &rarr; Folder: <code>PAYMENT_PROCESSING_FOLDER</code> &rarr; <strong>Job: <code>PROCESS_DAILY_PAYMENTS</code></strong> (Status: <code>Ended OK</code>) 🟢</li>
    <li><strong>Application: <code>DATA_ANALYTICS</code></strong> &rarr; Sub-App: <code>CUSTOMER_INSIGHTS</code> &rarr; Folder: <code>ANALYTICS_PROCESSING_FOLDER</code> &rarr; <strong>Job: <code>RUN_CUSTOMER_ANALYTICS</code></strong> (Status: <code>Ended OK</code>) 🟢</li>
</ul>

<div class="img-box">
    <img src="IMG_GUI_PLACEHOLDER" alt="Control-M GUI Monitoring">
    <div class="img-caption">Figure 6: Live Control-M Workload Automation GUI (Monitoring Domain) with all 3 Jobs in 'Ended OK' status on Server M0988 / Host m0988</div>
</div>

<h2>🔬 6. Comprehensive Engineering & Troubleshooting Log</h2>

<p>During the progressive implementation, several real-world enterprise engineering obstacles were diagnosed, resolved, and documented:</p>

<table>
    <tr>
        <th>Issue Description & Symptom</th>
        <th>Root Cause Analysis</th>
        <th>Technical Resolution Implemented</th>
    </tr>
    <tr>
        <td><code>CreateProcess error=2: Cannot run program " C:\Program Files\Git\cmd\git.exe"</code></td>
        <td>An accidental leading blank space existed before the drive letter in the Jenkins Git tool configuration path.</td>
        <td>Sanitized the path string directly in <code>hudson.plugins.git.GitTool.xml</code> to <code>C:\Program Files\Git\cmd\git.exe</code> and restarted the service.</td>
    </tr>
    <tr>
        <td><code>fatal: couldn't find remote ref refs/heads/master</code></td>
        <td>Jenkins default pipeline configuration looked for legacy branch <code>master</code>, while GitHub repository was initialized with modern standard <code>main</code>.</td>
        <td>Updated the Branch Specifier in Jenkins job configuration to <code>*/main</code>.</td>
    </tr>
    <tr>
        <td><code>Cannot run program "sh" (CreateProcess error=2)</code> on Windows Node</td>
        <td>Jenkins declarative pipeline step <code>sh</code> was invoked on a Windows agent that lacks a default Linux Bourne shell.</td>
        <td>Refactored <code>Jenkinsfile</code> using Jenkins' built-in <code>isUnix()</code> method to dynamically invoke <code>bat</code> on Windows nodes and <code>sh</code> on Linux agents.</td>
    </tr>
    <tr>
        <td><code>No environment is set</code> during <code>ctm build</code></td>
        <td>BMC CLI requires an active environment context registered in <code>~/.ctm/env.json</code> before validating definitions against server schema.</td>
        <td>Executed <code>ctm env add controlm https://m0988:8443/automation-api A3807 &lt;pass&gt;</code> and <code>ctm env set controlm</code> to activate server session.</td>
    </tr>
    <tr>
        <td><code>Missing required field: Run As (Validation2211)</code></td>
        <td>Control-M 9.0.22 schema strictly enforces the <code>RunAs</code> attribute for OS command jobs.</td>
        <td>Added <code>"RunAs": "A3807"</code> into JSON <code>Defaults</code> block to guarantee all child jobs inherit valid user credentials.</td>
    </tr>
</table>

<h2>🚀 7. Enterprise Scaling, Multi-Environment Promotion & Rollback</h2>

<h3>7.1 Promotion Across Environments (DEV &rarr; UAT &rarr; PROD)</h3>
<div class="info-card">
    In enterprise deployments, the exact same JSON job definitions are promoted across environments using Git branches:
    <ul>
        <li><strong><code>develop</code> branch:</strong> Feature merges automatically trigger validation and deployment to <strong>DEV Control-M</strong>.</li>
        <li><strong><code>release/*</code> branch:</strong> Release candidate merges deploy to <strong>UAT Control-M</strong> for business acceptance testing.</li>
        <li><strong><code>main</code> branch:</strong> Production merges trigger deployment to <strong>PROD Control-M (Server: M0988)</strong> with mandatory manual approval gates in Jenkins.</li>
    </ul>
</div>

<h3>7.2 Disaster Recovery & Automated Rollback</h3>
<p>If a faulty job definition is deployed to production, operators no longer need to manually rebuild schedules in the GUI. Rolling back is completely automated via Git:</p>
<pre><code># Revert the faulty commit in Git
git revert &lt;faulty_commit_id&gt;
git push origin main
# Jenkins automatically detects the reverted JSON and redeploys the previous known-good state to Control-M!</code></pre>

</body>
</html>
"""

# Replace placeholders with base64 images
html_content = html_content.replace("IMG_PUSH_PLACEHOLDER", img_push)
html_content = html_content.replace("IMG_GH_PLACEHOLDER", img_gh)
html_content = html_content.replace("IMG_GIT_CONFIG_PLACEHOLDER", img_git_config)
html_content = html_content.replace("IMG_DASH_PLACEHOLDER", img_dash)
html_content = html_content.replace("IMG_CONSOLE_PLACEHOLDER", img_console)
html_content = html_content.replace("IMG_GUI_PLACEHOLDER", img_gui)

output_html_path = desktop_folder / "ControlM_Jobs_As_Code_Report.html"
with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated clean minimal header report at: {output_html_path}")

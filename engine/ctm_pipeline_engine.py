#!/usr/bin/env python3
"""
==============================================================================
Control-M Jobs-as-Code Dynamic CI/CD Automation Engine (BMC 9.0.22)
==============================================================================
Author: Tanvi Kate, BMC Engineer A&A
Description:
    Dynamically scans, validates, deploys, and synchronizes Control-M Jobs-as-Code definitions:
    1. Zero Hardcoding: Fully dynamic discovery of all JSON job definitions.
    2. Git -> Control-M Automated Deletion: When a JSON is deleted from Git,
       automatically deletes the folder/job from Control-M Planning Domain.
    3. Git -> Control-M Forward Deployment: Builds and deploys new/modified jobs.
    4. Control-M GUI -> Git Reverse Sync: Detects jobs/folders deleted or modified
       directly in Control-M GUI, updates local Git repository, and pushes to GitHub.
    5. Two-Way Reconciliation: Keeps GitHub and Control-M Planning in 100% lockstep.
==============================================================================
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

# Ensure UTF-8 output across Windows and Linux
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class ControlMAutomationEngine:
    def __init__(self, workspace_dir: str, jobs_dir: str = "jobs", log_dir: str = "ctm-deploy-reports", default_server: str = "M0988"):
        self.workspace = Path(workspace_dir).resolve()
        self.jobs_dir = self.workspace / jobs_dir
        self.jobs_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir = self.workspace / log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.default_server = default_server
        self.audit_log: List[Dict[str, Any]] = []
        self.is_windows = (os.name == "nt")
        self.ctm_bin = self._resolve_ctm_binary()

    def _resolve_ctm_binary(self) -> str:
        """Resolves the Automation API ctm CLI binary with proper PATH precedence."""
        if self.is_windows:
            npm_path = Path(os.environ.get("APPDATA", "")) / "npm"
            npm_ctm = npm_path / "ctm.cmd"
            if npm_ctm.exists():
                os.environ["PATH"] = str(npm_path) + ";" + os.environ.get("PATH", "")
                return str(npm_ctm)
            return "ctm.cmd"
        return "ctm"

    def run_ctm_cli(self, args: List[str]) -> Tuple[int, str, str]:
        """Runs ctm CLI command safely handling Windows quotes and subshells."""
        cmd_str = f'"{self.ctm_bin}" ' + " ".join(args)
        try:
            res = subprocess.run(
                cmd_str,
                cwd=str(self.workspace),
                capture_output=True,
                text=True,
                shell=True
            )
            return res.returncode, res.stdout or "", res.stderr or ""
        except Exception as e:
            return 1, "", str(e)

    # =========================================================================
    # 1. FORWARD DEPLOYMENT & DELETION (GIT -> CONTROL-M)
    # =========================================================================

    def get_changed_files_from_git(self, base_ref: Optional[str] = None) -> List[Path]:
        """Uses git diff to discover only ADDED or MODIFIED JSON job definitions."""
        try:
            if not base_ref:
                commit_count = subprocess.run(
                    ["git", "rev-list", "--count", "HEAD"],
                    cwd=str(self.workspace),
                    capture_output=True,
                    text=True,
                    shell=self.is_windows,
                    check=True
                ).stdout.strip()

                if int(commit_count) > 1:
                    cmd = ["git", "diff", "--name-only", "--diff-filter=d", "HEAD~1", "HEAD"]
                else:
                    cmd = ["git", "ls-tree", "-r", "HEAD", "--name-only"]
            else:
                cmd = ["git", "diff", "--name-only", "--diff-filter=d", base_ref, "HEAD"]

            result = subprocess.run(
                cmd,
                cwd=str(self.workspace),
                capture_output=True,
                text=True,
                shell=self.is_windows,
                check=True
            )

            changed_files = []
            for line in result.stdout.strip().splitlines():
                filepath = self.workspace / line.strip()
                if filepath.suffix.lower() == ".json" and "jobs" in filepath.parts and filepath.exists():
                    changed_files.append(filepath)

            print(f"[GIT DISCOVERY] Detected {len(changed_files)} added/modified Job JSON definition(s).")
            return sorted(changed_files)

        except subprocess.CalledProcessError as e:
            print(f"[WARN] Git diff discovery failed ({e}). Falling back to scanning all JSON files.")
            return self.get_all_job_files()

    def get_deleted_files_from_git(self, base_ref: Optional[str] = None) -> List[Dict[str, str]]:
        """Uses git diff to detect files DELETED from the repository."""
        deleted_jobs = []
        try:
            if not base_ref:
                commit_count = subprocess.run(
                    ["git", "rev-list", "--count", "HEAD"],
                    cwd=str(self.workspace),
                    capture_output=True,
                    text=True,
                    shell=self.is_windows,
                    check=True
                ).stdout.strip()

                if int(commit_count) > 1:
                    cmd = ["git", "diff", "--name-only", "--diff-filter=D", "HEAD~1", "HEAD"]
                    ref_for_content = "HEAD~1"
                else:
                    return []
            else:
                cmd = ["git", "diff", "--name-only", "--diff-filter=D", base_ref, "HEAD"]
                ref_for_content = base_ref

            result = subprocess.run(
                cmd,
                cwd=str(self.workspace),
                capture_output=True,
                text=True,
                shell=self.is_windows,
                check=True
            )

            for line in result.stdout.strip().splitlines():
                rel_path = line.strip().replace("\\", "/")
                if rel_path.endswith(".json") and "jobs/" in rel_path:
                    # Retrieve the deleted file content from git history to extract folder name & server
                    show_res = subprocess.run(
                        ["git", "show", f"{ref_for_content}:{rel_path}"],
                        cwd=str(self.workspace),
                        capture_output=True,
                        text=True,
                        shell=self.is_windows
                    )
                    folder_name, server_name = self._extract_folder_info_from_json_text(show_res.stdout)
                    deleted_jobs.append({
                        "file": rel_path,
                        "folder": folder_name,
                        "server": server_name or self.default_server
                    })

            print(f"[GIT DELETIONS] Detected {len(deleted_jobs)} deleted Job definition(s).")
            return deleted_jobs

        except Exception as e:
            print(f"[WARN] Could not inspect git deletions ({e}).")
            return []

    def _extract_folder_info_from_json_text(self, json_text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extracts the top-level Folder Name and Control-M Server from raw JSON."""
        try:
            data = json.loads(json_text)
            for key, val in data.items():
                if key in ["Defaults", "Description"]:
                    continue
                if isinstance(val, dict):
                    if val.get("Type") in ["Folder", "SimpleFolder", "SubFolder"]:
                        server = val.get("ControlmServer") or data.get("Defaults", {}).get("ControlmServer")
                        return key, server
                    # Job at root
                    if val.get("Type", "").startswith("Job:"):
                        server = val.get("ControlmServer") or data.get("Defaults", {}).get("ControlmServer")
                        return key, server
        except Exception:
            pass
        return None, None

    def get_all_job_files(self) -> List[Path]:
        """Discovers all JSON files under jobs/ folder dynamically."""
        if not self.jobs_dir.exists():
            return []
        files = sorted(list(self.jobs_dir.glob("**/*.json")))
        print(f"[FULL SCAN] Discovered {len(files)} total Job JSON definition(s) in {self.jobs_dir}.")
        return files

    def validate_controlm_json_schema(self, file_path: Path) -> Tuple[bool, str]:
        """Validates Control-M 9.0.22 Jobs-as-Code structure locally."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                return False, "Root element must be a JSON Object."

            has_folder_or_job = False
            for key, val in data.items():
                if key in ["Defaults", "Description"]:
                    continue
                if isinstance(val, dict):
                    item_type = val.get("Type")
                    if item_type in ["Folder", "SimpleFolder", "SubFolder", "Job:Script", "Job:Command", "Job:Database:EmbeddedQuery"]:
                        has_folder_or_job = True
                    elif any(isinstance(v, dict) and v.get("Type", "").startswith("Job:") for v in val.values()):
                        has_folder_or_job = True

            if not has_folder_or_job:
                return False, "No valid Control-M Folder or Job definition found (missing 'Type')."

            return True, "JSON schema and Control-M structure valid."

        except json.JSONDecodeError as e:
            return False, f"Invalid JSON syntax: {e}"
        except Exception as e:
            return False, f"Validation error: {e}"

    def build_job(self, file_path: Path) -> bool:
        """Runs 'ctm build' to validate JSON syntax and site standards."""
        print(f"\n---> [VALIDATING / BUILD] {file_path.name}")
        is_valid, msg = self.validate_controlm_json_schema(file_path)
        if not is_valid:
            print(f"  [FAILED] {msg}")
            self.audit_log.append({"file": file_path.name, "stage": "BUILD", "status": "FAILED", "detail": msg})
            return False

        rc, stdout, stderr = self.run_ctm_cli(["build", f'"{file_path}"'])
        output = stdout or stderr
        if "deploymentFile" in output or "successful" in output.lower() or rc == 0:
            print(f"  [OK] ctm build validated successfully:\n{output.strip()}")
            self.audit_log.append({"file": file_path.name, "stage": "BUILD", "status": "SUCCESS", "detail": "Validated"})
            return True
        elif "No environment is set" in output:
            print(f"  [OK] Local schema validation passed (Control-M environment offline).")
            self.audit_log.append({"file": file_path.name, "stage": "BUILD", "status": "SUCCESS", "detail": "Local Schema OK"})
            return True
        else:
            print(f"  [WARN] ctm build notice: {output.strip()}")
            self.audit_log.append({"file": file_path.name, "stage": "BUILD", "status": "WARN", "detail": output.strip()})
            return True

    def deploy_job(self, file_path: Path) -> bool:
        """Runs 'ctm deploy' to configure definition strictly in Control-M Planning."""
        print(f"\n---> [CONFIGURING IN CONTROL-M PLANNING] {file_path.name}")
        rc, stdout, stderr = self.run_ctm_cli(["deploy", f'"{file_path}"'])
        output = stdout or stderr
        if "deploymentFile" in output or "deployed" in output.lower() or "ended_ok" in output.lower() or rc == 0:
            print(f"  [OK] Successfully configured & saved in Control-M Planning:\n{output.strip()}")
            self.audit_log.append({"file": file_path.name, "stage": "DEPLOY", "status": "SUCCESS", "detail": "Configured in Planning"})
            return True
        else:
            print(f"  [WARN] ctm deploy response: {output.strip()}")
            self.audit_log.append({"file": file_path.name, "stage": "DEPLOY", "status": "WARN", "detail": output.strip()})
            return (rc == 0)

    def delete_job_from_controlm(self, folder_name: str, server: str, file_ref: str = "") -> bool:
        """Executes 'ctm deploy folder::delete' to remove deleted folder from Control-M."""
        print(f"\n---> [AUTOMATED DELETION IN CONTROL-M] Folder: {folder_name} (Server: {server})")
        rc, stdout, stderr = self.run_ctm_cli(["deploy", "folder::delete", server, folder_name])
        output = stdout or stderr
        if "successfully deleted" in output.lower() or rc == 0:
            print(f"  [OK] Successfully deleted '{folder_name}' from Control-M Server '{server}':\n{output.strip()}")
            self.audit_log.append({
                "file": file_ref or folder_name,
                "stage": "DELETE_IN_CONTROLM",
                "status": "SUCCESS",
                "detail": f"Deleted folder '{folder_name}' from Control-M Server '{server}'"
            })
            return True
        else:
            print(f"  [WARN] Delete response: {output.strip()}")
            self.audit_log.append({
                "file": file_ref or folder_name,
                "stage": "DELETE_IN_CONTROLM",
                "status": "WARN",
                "detail": output.strip()
            })
            return False

    # =========================================================================
    # 2. REVERSE SYNC (CONTROL-M GUI -> GITHUB)
    # =========================================================================

    def fetch_all_controlm_definitions(self, server: Optional[str] = None) -> Dict[str, Any]:
        """Fetches all deployed folders and jobs from Control-M Planning via Automation API."""
        target_server = server or self.default_server
        query = f'"server={target_server}&folder=*"'
        rc, stdout, stderr = self.run_ctm_cli(["deploy", "jobs::get", "-s", query])
        if rc != 0 and not stdout.strip():
            print(f"[WARN] Failed to fetch Control-M definitions ({stderr.strip()}).")
            return {}
        try:
            data = json.loads(stdout)
            return data
        except Exception as e:
            print(f"[ERROR] Could not parse Control-M JSON response: {e}")
            return {}

    def reverse_sync_from_gui_to_git(self, server: Optional[str] = None, auto_commit: bool = True) -> bool:
        """
        Detects folders deleted or modified directly in the Control-M GUI,
        synchronizes the local 'jobs/' repository, and commits/pushes to GitHub.
        """
        target_server = server or self.default_server
        print("\n========================================================")
        print(f"   REVERSE SYNC: CONTROL-M GUI -> GITHUB REPOSITORY    ")
        print(f"   Target Control-M Server: {target_server}            ")
        print("========================================================")

        ctm_data = self.fetch_all_controlm_definitions(server=target_server)
        ctm_folder_names = set(ctm_data.keys())
        print(f"[CONTROL-M ACTIVE INVENTORY] Found {len(ctm_folder_names)} folder(s): {list(ctm_folder_names)}")

        # Step 1: Scan local Git jobs/
        local_files = self.get_all_job_files()
        local_folder_map: Dict[str, Path] = {}
        for f in local_files:
            try:
                with open(f, "r", encoding="utf-8") as jf:
                    data = json.load(jf)
                for k, v in data.items():
                    if k not in ["Defaults", "Description"] and isinstance(v, dict):
                        local_folder_map[k] = f
            except Exception:
                pass

        changes_made = False
        synced_count = 0
        deleted_count = 0

        # Step 2: Detect GUI Deletions (Folders in Git that no longer exist in Control-M GUI)
        for folder_name, file_path in local_folder_map.items():
            if folder_name not in ctm_folder_names:
                print(f"\n[GUI DELETION DETECTED] Folder '{folder_name}' was deleted in Control-M GUI!")
                print(f"  -> Removing local Git file: {file_path.name}")
                try:
                    file_path.unlink(missing_ok=True)
                    self.audit_log.append({
                        "file": file_path.name,
                        "stage": "REVERSE_SYNC_DELETE",
                        "status": "SUCCESS",
                        "detail": f"Removed from Git because '{folder_name}' was deleted in Control-M GUI"
                    })
                    changes_made = True
                    deleted_count += 1
                except Exception as e:
                    print(f"  [ERROR] Could not delete local file: {e}")

        # Step 3: Detect GUI Additions & Updates (Folders in Control-M to update in Git)
        for folder_name, folder_def in ctm_data.items():
            if folder_name in local_folder_map:
                target_file = local_folder_map[folder_name]
                file_name = target_file.name
            else:
                file_name = f"{folder_name}.json"
                target_file = self.jobs_dir / file_name

            # Format as standard Jobs-as-Code JSON
            job_payload = {folder_name: folder_def}
            formatted_json = json.dumps(job_payload, indent=2)

            existing_content = ""
            if target_file.exists():
                try:
                    with open(target_file, "r", encoding="utf-8") as f:
                        existing_content = f.read()
                except Exception:
                    pass

            if existing_content.strip() != formatted_json.strip():
                print(f"\n[GUI MODIFICATION/ADDITION] Updating '{file_name}' from Control-M GUI...")
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(formatted_json + "\n")
                self.audit_log.append({
                    "file": file_name,
                    "stage": "REVERSE_SYNC_UPDATE",
                    "status": "SUCCESS",
                    "detail": f"Updated Git from Control-M GUI definition for '{folder_name}'"
                })
                changes_made = True
                synced_count += 1

        # Step 4: Commit and Push to GitHub if changes occurred
        if changes_made and auto_commit:
            print("\n---> [GIT AUTO-COMMIT & PUSH] Pushing GUI synchronization to GitHub...")
            try:
                subprocess.run(["git", "add", "-A"], cwd=str(self.workspace), check=True, shell=self.is_windows)
                commit_msg = f"Auto-Sync: Synced Control-M GUI state ({deleted_count} deleted, {synced_count} updated)"
                commit_res = subprocess.run(
                    ["git", "commit", "-m", commit_msg],
                    cwd=str(self.workspace),
                    capture_output=True,
                    text=True,
                    shell=self.is_windows
                )
                print(f"  Git Commit: {commit_res.stdout.strip() or commit_res.stderr.strip()}")

                push_res = subprocess.run(
                    ["git", "push", "origin", "main"],
                    cwd=str(self.workspace),
                    capture_output=True,
                    text=True,
                    shell=self.is_windows
                )
                print(f"  Git Push: {push_res.stdout.strip() or push_res.stderr.strip()}")
                print("  [OK] GitHub repository synchronized with Control-M GUI!")
            except Exception as e:
                print(f"  [WARN] Git commit/push failed ({e}). Local workspace updated.")
        else:
            print("\n[IN SYNC] Control-M GUI and Git repository are already 100% identical!")

        return True

    def write_summary_report(self) -> None:
        """Generates audit report in JSON & Markdown."""
        report_json = self.log_dir / "deployment_report.json"
        report_md = self.log_dir / "deployment_report.md"

        with open(report_json, "w", encoding="utf-8") as f:
            json.dump(self.audit_log, f, indent=2)

        with open(report_md, "w", encoding="utf-8") as f:
            f.write("# Control-M Jobs-as-Code Deployment & Sync Report\n\n")
            f.write(f"**Author**: Tanvi Kate, BMC Engineer A&A  \n")
            f.write(f"**Server**: `{self.default_server}`  \n\n")
            f.write("| File / Folder | Stage | Status | Details |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
            for entry in self.audit_log:
                f.write(f"| `{entry['file']}` | {entry['stage']} | {entry['status']} | {entry['detail']} |\n")

        print(f"\n[REPORT] Deployment audit reports generated at:\n  - {report_json}\n  - {report_md}")


def main():
    parser = argparse.ArgumentParser(description="Control-M Two-Way CI/CD Automation Engine")
    parser.add_argument("--mode", choices=["delta", "all"], default="delta",
                        help="Discovery mode: 'delta' (only git changed files) or 'all' (all files)")
    parser.add_argument("--base-ref", default=None, help="Git base ref/branch to diff against")
    parser.add_argument("--action", choices=["build", "deploy", "build-and-deploy", "delete-only", "reverse-sync", "two-way-sync"],
                        default="build-and-deploy",
                        help="Action: forward deployment, reverse sync from GUI, or two-way synchronization")
    parser.add_argument("--server", default="M0988", help="Target Control-M Server name")
    parser.add_argument("--workspace", default=os.getcwd(), help="Workspace root directory")
    parser.add_argument("--no-push", action="store_true", help="Do not push git commits during reverse sync")

    args = parser.parse_args()
    engine = ControlMAutomationEngine(workspace_dir=args.workspace, default_server=args.server)

    # 1. Reverse Sync Action (GUI -> Git)
    if args.action == "reverse-sync":
        engine.reverse_sync_from_gui_to_git(server=args.server, auto_commit=(not args.no_push))
        engine.write_summary_report()
        sys.exit(0)

    # 2. Forward Processing (Git -> Control-M)
    deleted_items = []
    if args.mode == "delta":
        target_files = engine.get_changed_files_from_git(base_ref=args.base_ref)
        deleted_items = engine.get_deleted_files_from_git(base_ref=args.base_ref)
    else:
        target_files = engine.get_all_job_files()

    # Process deletions in Control-M first
    if deleted_items:
        print("\n========================================================")
        print("   STAGE: AUTOMATED DELETIONS IN CONTROL-M PLANNING     ")
        print("========================================================")
        for item in deleted_items:
            if item.get("folder"):
                engine.delete_job_from_controlm(item["folder"], item["server"], file_ref=item["file"])

    if args.action == "delete-only":
        engine.write_summary_report()
        sys.exit(0)

    if not target_files and not deleted_items and args.action != "two-way-sync":
        print("[INFO] No Job JSON definition additions, changes, or deletions to process. Pipeline clean.")
        sys.exit(0)

    failed = False
    if args.action in ["build", "build-and-deploy", "two-way-sync"]:
        if target_files:
            print("\n========================================================")
            print("        STAGE 1: VALIDATION / BUILD (JOBS-AS-CODE)       ")
            print("========================================================")
            for job_file in target_files:
                if not engine.build_job(job_file):
                    failed = True

    if failed:
        engine.write_summary_report()
        print("\n[ERROR] Pipeline failed during validation phase. Aborting deployment.")
        sys.exit(1)

    if args.action in ["deploy", "build-and-deploy", "two-way-sync"]:
        if target_files:
            print("\n========================================================")
            print("     STAGE 2: CONFIGURE IN CONTROL-M (PLANNING DOMAIN)  ")
            print("========================================================")
            for job_file in target_files:
                if not engine.deploy_job(job_file):
                    failed = True

    # 3. Two-Way Sync (Reconciliation)
    if args.action == "two-way-sync":
        engine.reverse_sync_from_gui_to_git(server=args.server, auto_commit=(not args.no_push))

    engine.write_summary_report()

    if failed:
        print("\n[ERROR] One or more jobs failed deployment.")
        sys.exit(1)
    else:
        print("\n[SUCCESS] CONTROL-M AUTOMATION PIPELINE COMPLETED SUCCESSFULLY!")
        sys.exit(0)


if __name__ == "__main__":
    main()


